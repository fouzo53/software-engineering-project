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
from src.infrastructure.databases.database import db
from injector import inject
from src.infrastructure.services.stt_service import stt_service
from src.services.notification_service import NotificationService


class AIService:
    """Service sử dụng Google Generative AI (Gemini) để parse text thành order"""
    
    @inject
    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service
        # Configure API key từ .env
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if api_key:
            genai.configure(api_key=api_key)
        # Dùng model nhẹ, phản hồi nhanh
        self.model = genai.GenerativeModel("gemini-flash-lite-latest")
    
    def parse_order_text(self, text: str) -> Dict:
        """
        Phân tích câu lệnh bán hàng bằng AI (Hỗ trợ đa đơn hàng, đa khách hàng)
        """
        try:
            print(f"[AI Service] Parsing text: {text[:50]}...")
            # Prompt nâng cao xử lý đa nhiệm
            prompt = f"""
            Bạn là trợ lý AI chuyên nghiệp cho phần mềm quản lý bán hàng vật liệu xây dựng.
            Nhiệm vụ: Phân tích câu lệnh tiếng Việt tự nhiên thành cấu trúc dữ liệu đơn hàng (Structured Orders).

            Câu lệnh input: "{text}"

            Yêu cầu xử lý:
            1.  **Phát hiện đa đơn hàng**: 
                - Nếu câu lệnh chứa yêu cầu bán cho nhiều người khác nhau (ví dụ: "Bán cho A 2 cái, bán cho B 3 cái"), hãy tách thành các đơn hàng riêng biệt trong mảng "orders".
                - Nếu bán nhiều món cho 1 người -> Gom vào 1 đơn hàng (mảng items).
            
            2.  **Trích xuất thông tin**:
                - Customer: Tên, danh xưng (anh/chị/cô/chú).
                - Items: Tên sản phẩm, số lượng, đơn vị (suy luận từ ngữ cảnh: xi măng->bao, cát->khối...).
                - Payment: Nếu có từ khóa "nợ", "ghi sổ", "trả sau" -> DEBT. Mặc định -> CASH.

            3.  **Xử lý logic phức tạp**:
                - "mỗi loại": Ví dụ "lấy gạch và cát mỗi loại 2 khối" -> tạo 2 item riêng biệt với số lượng 2.
                - "tương tự": Ví dụ "Bán cho A 1 bao xi, B cũng vậy" -> Đơn của B copy y hệt đơn A.

            OUTPUT FORMAT (JSON Valid Only):
            {{
                "orders": [
                    {{
                        "customer": {{ "name": "Tên khách", "confidence": 0.9 }},
                        "items": [
                            {{ "product_name": "Tên SP", "quantity": 1, "unit": "ĐVT" }}
                        ],
                        "payment": {{ "type": "CASH" }}
                    }}
                ],
                "confidence_score": 0.9
            }}
            """
            
            response = self.model.generate_content(prompt)
            raw_response = response.text.strip()
            
            # Trích xuất JSON bằng cách tìm dấu { đầu tiên và } cuối cùng
            start_idx = raw_response.find('{')
            end_idx = raw_response.rfind('}')
            
            if start_idx == -1 or end_idx == -1:
                 return {"success": False, "message": f"AI không trả về JSON hợp lệ. Nội dung: {raw_response[:100]}..."}
            
            json_str = raw_response[start_idx:end_idx + 1]

            try:
                parsed = json.loads(json_str)
            except json.JSONDecodeError:
                 return {"success": False, "message": f"Lỗi cấu trúc dữ liệu từ AI: {json_str[:50]}..."}
            orders_data = parsed.get("orders", [])
            
            if not orders_data:
                 # Fallback for empty
                 return {"success": False, "message": "Không tìm thấy thông tin đơn hàng trong câu nói."}

            created_drafts = []
            
            # Process each order found
            for order_data in orders_data:
                # 1. Map Items
                final_items = []
                total_amount = 0.0
                
                for item in order_data.get("items", []):
                    p_name = item.get("product_name", "")
                    qty = int(item.get("quantity", 0) or 0)
                    
                    # Search Product
                    product = ProductModel.query.filter(
                        ProductModel.name.ilike(f"%{p_name}%")
                    ).first()
                    
                    price = 0
                    if product:
                        price = product.price or product.selling_price or 0
                    
                    item_node = {
                        "product": {
                            "match_type": "exact" if product else "none",
                            "product_id": product.id if product else None,
                            "name": product.name if product else p_name,
                        },
                        "quantity": qty or 1,
                        "unit": item.get("unit", "cái"),
                        "price": price,
                        "subtotal": price * (qty or 1)
                    }
                    total_amount += item_node["subtotal"]
                    final_items.append(item_node)

                # 2. Map Customer
                customer_name = order_data.get("customer", {}).get("name", "Khách lẻ")
                customer_node = None
                if customer_name and customer_name.lower() != "khách lẻ":
                    customer = CustomerModel.query.filter(
                        CustomerModel.name.ilike(f"%{customer_name}%")
                    ).first()
                    customer_node = {
                         "match_type": "exact" if customer else "none",
                         "customer_id": customer.id if customer else None,
                         "name": customer.name if customer else customer_name
                    }

                # 3. Create Draft
                payment_type = order_data.get("payment", {}).get("type", "CASH").upper()
                
                # Create standardized Parse Result for DB
                db_parsed_data = {
                    "customer": customer_node,
                    "items": final_items,
                    "payment": {"type": payment_type, "confidence": 1.0},
                    "orders": orders_data # Keep original full context if needed
                }

                draft = DraftOrderModel(
                    text_input=text,
                    parsed_data=json.dumps(db_parsed_data, ensure_ascii=False),
                    customer_id=customer_node.get("customer_id") if customer_node else None,
                    customer_name=customer_node.get("name") if customer_node else customer_name,
                    payment_method=payment_type,
                    total_amount=total_amount,
                    status='draft'
                )
                db.session.add(draft)
                # Flush to get ID
                db.session.flush()
                created_drafts.append(draft)
            
            db.session.commit()
            
            # Prepare Response
            # Maintains backward compatibility by showing the FIRST draft details at top level
            # But provides 'all_drafts' for advanced UIs.
            primary_draft = created_drafts[0]
            primary_data = json.loads(primary_draft.parsed_data)

            return {
                "success": True,
                "message": f"Đã tìm thấy {len(created_drafts)} đơn hàng.",
                "draft_id": primary_draft.id, # Legacy support
                "draft_ids": [d.id for d in created_drafts],
                "items": primary_data.get("items"),
                "customer": primary_data.get("customer"),
                "payment_method": primary_draft.payment_method,
                "total_amount": primary_draft.total_amount,
                # New field for multiple drafts info
                "multiple_drafts": len(created_drafts) > 1,
                "all_drafts": [
                    {
                        "draft_id": d.id,
                        "customer_name": d.customer_name,
                        "total": d.total_amount,
                        "payment": d.payment_method
                    } for d in created_drafts
                ]
            }

        except Exception as e:
            db.session.rollback()
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
            
            # Thêm transcript vào kết quả với đúng format object
            result["transcript"] = {
                "original_text": text,
                "normalized_text": text,
                "source": "stt"
            }
            return result
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi xử lý audio: {str(e)}"
            }
    
    def confirm_draft_order(self, draft_id: int, user_id: int) -> Dict:
        """
        Xác nhận chuyển đơn nháp thành đơn thật
        Returns: {"success": bool, "order_id": int, "message": str}
        """
        try:
            if not user_id:
                return {"success": False, "message": "User ID is required"}

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
                user_id=user_id,
                customer_id=draft.customer_id,
                total_amount=total,
                payment_method=draft.payment_method or 'CASH',
                created_at=datetime.now()
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
            
            # Thông báo khi đơn hàng được xác nhận
            self.notification_service.create_notification(
                title="Đơn hàng mới từ AI",
                message=f"Đơn hàng AI #{new_order.id} đã được xác nhận. Tổng tiền: {int(total):,}đ",
                type="new_order",
                user_id=None # Broadcast
            )
            
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
    

