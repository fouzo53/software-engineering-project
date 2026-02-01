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


class AIService:
    """Service sử dụng Google Generative AI (Gemini) để parse text thành order"""
    
    def __init__(self):
        # Configure API key từ .env
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    def parse_order_text(self, text: str) -> Dict:
        """
        Phân tích câu lệnh bán hàng bằng AI
        Input: "Bán 5 bao xi măng cho anh Nam nợ nhé"
        Output: {
            "success": bool,
            "draft_id": int,
            "items": [...],
            "customer": {...},
            "payment_method": "DEBT/CASH"
        }
        """
        try:
            # Bước 1: Dùng AI để parse text
            prompt = f"""
            Phân tích câu lệnh bán hàng sau và trích xuất thông tin:
            "{text}"
            
            Trả về JSON format chính xác:
            {{
                "items": [
                    {{"product_name": "tên sản phẩm", "quantity": số_lượng}}
                ],
                "customer_name": "tên khách hàng (nếu có)",
                "payment_method": "DEBT hoặc CASH (nếu có từ 'nợ', 'trả sau' thì DEBT, ngược lại CASH)"
            }}
            
            Lưu ý:
            - Nếu không có tên khách hàng, để customer_name là null
            - Nếu không có phương thức thanh toán rõ ràng, mặc định là CASH
            - Chỉ trả về JSON, không giải thích gì thêm
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:].strip()
            
            parsed = json.loads(response_text)
            
            # Bước 2: Tìm sản phẩm trong database
            items_with_ids = []
            total_amount = 0.0
            
            for item in parsed.get("items", []):
                product_name = item.get("product_name", "")
                quantity = item.get("quantity", 0)
                
                # Tìm product gần đúng nhất
                product = ProductModel.query.filter(
                    ProductModel.name.ilike(f"%{product_name}%")
                ).first()
                
                if product:
                    items_with_ids.append({
                        "product_id": product.id,
                        "product_name": product.name,
                        "quantity": quantity,
                        "price": product.price,
                        "subtotal": product.price * quantity
                    })
                    total_amount += product.price * quantity
                else:
                    items_with_ids.append({
                        "product_id": None,
                        "product_name": product_name,
                        "quantity": quantity,
                        "price": 0,
                        "subtotal": 0,
                        "error": "Không tìm thấy sản phẩm trong kho"
                    })
            
            # Bước 3: Tìm khách hàng trong database
            customer_name = parsed.get("customer_name")
            customer_info = None
            
            if customer_name:
                customer = CustomerModel.query.filter(
                    CustomerModel.name.ilike(f"%{customer_name}%")
                ).first()
                
                if customer:
                    customer_info = {
                        "customer_id": customer.id,
                        "customer_name": customer.name,
                        "phone": customer.phone,
                        "debt_amount": customer.debt_amount
                    }
                else:
                    customer_info = {
                        "customer_id": None,
                        "customer_name": customer_name,
                        "found": False,
                        "message": "Khách hàng chưa có trong hệ thống"
                    }
            
            # Bước 4: Lưu draft order vào database
            payment_method = parsed.get("payment_method", "CASH").upper()
            
            draft = DraftOrderModel(
                text_input=text,
                parsed_data=json.dumps(parsed, ensure_ascii=False),
                customer_id=customer_info.get("customer_id") if customer_info else None,
                customer_name=customer_name,
                payment_method=payment_method,
                total_amount=total_amount,
                status='draft'
            )
            
            db.session.add(draft)
            db.session.commit()
            
            return {
                "success": True,
                "draft_id": draft.id,
                "items": items_with_ids,
                "customer": customer_info,
                "payment_method": payment_method,
                "total_amount": total_amount,
                "message": "Đã phân tích thành công. Kiểm tra và xác nhận đơn hàng."
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi khi phân tích: {str(e)}"
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
