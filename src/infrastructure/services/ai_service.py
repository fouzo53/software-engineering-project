import google.generativeai as genai
import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from src.infrastructure.models.draft_order_model import DraftOrderModel
from src.infrastructure.models.product_model import ProductModel
from src.infrastructure.models.customer_model import CustomerModel
from src.infrastructure.models.order_model import OrderModel, OrderDetailModel
from src.infrastructure.databases.database import db
from src.infrastructure.services.stt_service import stt_service


class AIService:
    """Service sử dụng Google Generative AI (Gemini) để parse text thành order"""
    
    def __init__(self):
        # Configure API key từ .env
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-flash-latest")
    
    def parse_order_text(self, text: str) -> Dict:
        """
        Phân tích câu lệnh bán hàng bằng AI theo chuẩn contract @docs/ai-draft-order-contract.md
        """
        try:
            # Bước 1: Dùng AI để parse text với prompt chi tiết hơn
            prompt = f"""
            Bạn là điều phối viên bán hàng thông minh. Hãy phân tích lệnh sau từ nhân viên:
            "{text}"
            
            Hãy bóc tách thông tin và trả về JSON chuẩn sau:
            {{
                "customer": {{
                    "name": "tên khách",
                    "confidence": 0.0-1.0
                }},
                "items": [
                    {{
                        "product_name": "tên SP",
                        "quantity": số_lượng,
                        "unit": "đơn vị (bao/viên/kg...)",
                        "confidence": 0.0-1.0
                    }}
                ],
                "payment": {{
                    "type": "CASH" hoặc "DEBT",
                    "confidence": 0.0-1.0
                }},
                "overall_confidence": 0.0-1.0,
                "issues": ["mô tả các vấn đề nếu có"],
                "warnings": ["cảnh báo cho người dùng"]
            }}
            
            Quy tắc:
            - Nếu không rõ khách, name = null.
            - Nếu có từ "nợ", "ghi sổ", "trả sau" -> payment.type = "DEBT".
            - Mặc định payment.type = "CASH".
            - Chỉ trả về JSON nguyên bản.
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:].strip()
            
            parsed = json.loads(response_text)
            
            # Bước 2: Khớp dữ liệu với Database
            final_items = []
            total_amount = 0.0
            
            for item in parsed.get("items", []):
                p_name = item.get("product_name", "")
                qty = item.get("quantity", 0)
                
                # Tìm product gần đúng
                product = ProductModel.query.filter(
                    ProductModel.name.ilike(f"%{p_name}%")
                ).first()
                
                item_node = {
                    "product": {
                        "match_type": "exact" if product else "none",
                        "product_id": product.id if product else None,
                        "name": product.name if product else p_name,
                        "confidence": item.get("confidence", 0.5)
                    },
                    "quantity": qty,
                    "unit": item.get("unit", "cái"),
                    "unit_confidence": 0.9,
                    "notes": None
                }
                
                if product:
                    price = product.price or product.selling_price or 0
                    total_amount += price * qty
                else:
                    item_node["notes"] = "Không tìm thấy sản phẩm trong kho"
                
                final_items.append(item_node)
            
            # Bước 3: Tìm khách hàng
            customer_name = parsed.get("customer", {}).get("name")
            customer_node = None
            if customer_name:
                customer = CustomerModel.query.filter(
                    CustomerModel.name.ilike(f"%{customer_name}%")
                ).first()
                customer_node = {
                    "match_type": "exact" if customer else "none",
                    "customer_id": customer.id if customer else None,
                    "name": customer.name if customer else customer_name,
                    "confidence": parsed.get("customer", {}).get("confidence", 0.5)
                }
            
            # Bước 4: Lưu Draft Order
            payment_type = parsed.get("payment", {}).get("type", "CASH")
            
            draft = DraftOrderModel(
                text_input=text,
                parsed_data=json.dumps(parsed, ensure_ascii=False),
                customer_id=customer_node.get("customer_id") if customer_node else None,
                customer_name=customer_name,
                payment_method=payment_type,
                total_amount=total_amount,
                status='draft'
            )
            
            db.session.add(draft)
            db.session.commit()
            
            # Trả về theo chuẩn Contract
            return {
                "success": True,
                "status": "ok" if parsed.get("overall_confidence", 0) > 0.6 else "needs_review",
                "draft_id": draft.id,
                "transcript": {
                    "original_text": text,
                    "normalized_text": text,
                    "source": "user_input"
                },
                "draft_order": {
                    "customer": customer_node,
                    "items": final_items,
                    "payment": {
                        "type": payment_type.lower(),
                        "confidence": parsed.get("payment", {}).get("confidence", 0.5)
                    },
                    "total_amount": total_amount
                },
                "confidence": parsed.get("overall_confidence", 0.5),
                "issues": parsed.get("issues", []),
                "warnings": parsed.get("warnings", []),
                "message": "Đã phân tích thành công."
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi parse AI: {str(e)}"
            }

    def parse_audio_order(self, audio_path: str) -> Dict:
        """
        Chuyển audio -> text và parse thành order
        """
        try:
            # 1. Chuyển voice sang text
            text = stt_service.transcribe(audio_path)
            if not text:
                return {
                    "success": False,
                    "message": "Không thể chuyển đổi âm thanh sang văn bản"
                }
            
            # 2. Parse text thành order
            result = self.parse_order_text(text)
            
            # Thêm transcript vào kết quả
            result["transcript"] = text
            return result
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi xử lý audio: {str(e)}"
            }
    
    def confirm_draft_order(self, draft_id: int) -> Dict:
        """
        Xác nhận chuyển đơn nháp thành đơn thật
        Returns: {"success": bool, "order_id": int, "message": str}
        """
        try:
            # Lấy draft order
            draft = DraftOrderModel.query.get(draft_id)
            
            if not draft:
                return {"success": False, "message": "Không tìm thấy đơn nháp"}
            
            if draft.status == 'confirmed':
                return {
                    "success": False,
                    "message": f"Đơn nháp đã được xác nhận rồi (Order ID: {draft.order_id})"
                }
            
            # Parse lại data
            parsed_data = json.loads(draft.parsed_data)
            items = parsed_data.get("items", [])
            
            # Kiểm tra và tạo order thật
            order_details = []
            total = 0.0
            
            for item in items:
                product_name = item.get("product_name", "")
                quantity = item.get("quantity", 0)
                
                # Tìm product
                product = ProductModel.query.filter(
                    ProductModel.name.ilike(f"%{product_name}%")
                ).first()
                
                if not product:
                    return {
                        "success": False,
                        "message": f"Không tìm thấy sản phẩm '{product_name}' trong kho"
                    }
                
                if product.stock < quantity:
                    return {
                        "success": False,
                        "message": f"Sản phẩm '{product.name}' không đủ hàng (Còn {product.stock})"
                    }
                
                order_details.append({
                    "product_id": product.id,
                    "quantity": quantity,
                    "price": product.price
                })
                total += product.price * quantity
            
            # Tạo Order
            new_order = OrderModel(
                customer_id=draft.customer_id,
                total=total,
                payment_method=draft.payment_method or 'CASH',
                status='completed'
            )
            
            db.session.add(new_order)
            db.session.flush()  # Get order ID
            
            # Tạo OrderDetails và trừ stock
            for detail in order_details:
                order_detail = OrderDetailModel(
                    order_id=new_order.id,
                    product_id=detail['product_id'],
                    quantity=detail['quantity'],
                    price=detail['price']
                )
                db.session.add(order_detail)
                
                # Trừ stock
                product = ProductModel.query.get(detail['product_id'])
                product.stock -= detail['quantity']
            
            # Nếu thanh toán nợ và có customer, cộng nợ
            if draft.payment_method == 'DEBT' and draft.customer_id:
                customer = CustomerModel.query.get(draft.customer_id)
                if customer:
                    customer.debt_amount += total
            
            # Cập nhật draft
            draft.status = 'confirmed'
            draft.confirmed_at = datetime.utcnow()
            draft.order_id = new_order.id
            
            db.session.commit()
            
            return {
                "success": True,
                "order_id": new_order.id,
                "total": total,
                "payment_method": draft.payment_method,
                "message": "Đã tạo đơn hàng thành công!"
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                "success": False,
                "message": f"Lỗi khi tạo đơn hàng: {str(e)}"
            }
    
    def parse_text_to_order(self, text: str) -> Dict:
        """Legacy method - giữ lại để backward compatible"""
        try:
            prompt = f"""
            Phân tích đoạn text sau và trích xuất thông tin đơn hàng:
            "{text}"
            
            Trả về JSON format:
            {{
                "items": [
                    {{"product_name": "tên sản phẩm", "quantity": số_lượng}}
                ]
            }}
            
            Chỉ trả về JSON, không giải thích gì thêm.
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:].strip()
            
            result = json.loads(response_text)
            
            return {
                "success": True,
                "items": result.get("items", [])
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to parse text: {str(e)}"
            }
