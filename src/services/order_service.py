from typing import List, Dict
from injector import inject
from datetime import datetime
from src.domain.models.order import Order, OrderDetail
from src.domain.interfaces.product_repository import IProductRepository
from src.infrastructure.models.order_model import OrderModel, OrderDetailModel
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.models.product_model import ProductModel
from src.infrastructure.databases.database import db


from src.services.notification_service import NotificationService
from src.services.bookkeeping_service import BookkeepingService

class OrderService:
    """Service xử lý logic nghiệp vụ cho Order"""
    
    @inject
    def __init__(self, product_repository: IProductRepository, notification_service: NotificationService, bookkeeping_service: BookkeepingService):
        self.product_repository = product_repository
        self.notification_service = notification_service
        self.bookkeeping_service = bookkeeping_service
    
    def create_order(self, user_id: int, items: List[Dict], customer_id: int = None, payment_method: str = 'CASH') -> Dict:
        """
        Tạo order với transaction chặt chẽ
        items: [{"product_id": int, "quantity": int}, ...]
        customer_id: ID khách hàng
        payment_method: CASH hoặc DEBT
        Returns: {"success": bool, "message": str, "order": Order}
        """
        try:
            # Bắt đầu nested transaction
            with db.session.begin_nested():
                total_amount = 0.0
                order_details = []
                
                # Validate và tính total_amount
                for item in items:
                    product = self.product_repository.get_by_id(item["product_id"])
                    if not product:
                        raise Exception(f"Product {item['product_id']} not found")
                    
                    if product.stock < item["quantity"]:
                        raise Exception(f"Not enough stock for product {product.name}")
                    
                    # Cập nhật stock (chưa commit)
                    success = self.product_repository.update_stock(
                        item["product_id"], 
                        item["quantity"], 
                        commit=False
                    )
                    
                    if not success:
                        raise Exception(f"Failed to update stock for product {product.name}")
                    
                    # Tạo order detail
                    detail_amount = product.price * item["quantity"]
                    total_amount += detail_amount
                    
                    order_details.append({
                        "product_id": item["product_id"],
                        "quantity": item["quantity"],
                        "price": product.price
                    })
                
                # Tạo order
                order_model = OrderModel(
                    user_id=user_id,
                    customer_id=customer_id,
                    total_amount=total_amount,
                    payment_method=payment_method
                )
                db.session.add(order_model)
                db.session.flush()  # Lấy order.id
                
                # Nếu ghi nợ, cập nhật debt của khách hàng
                if payment_method == 'DEBT' and customer_id:
                    from src.infrastructure.models.customer_model import CustomerModel
                    customer = CustomerModel.query.get(customer_id)
                    if customer:
                        customer.debt_amount = (customer.debt_amount or 0) + total_amount
                
                # Tạo order details
                for detail in order_details:
                    detail_model = OrderDetailModel(
                        order_id=order_model.id,
                        product_id=detail["product_id"],
                        quantity=detail["quantity"],
                        price=detail["price"]
                    )
                    db.session.add(detail_model)
            
            # Commit transaction
            db.session.commit()
            
            # 3. Ghi sổ kế toán tự động (S1, S2, S6, S7)
            try:
                self.bookkeeping_service.record_sale(
                    order_id=order_model.id,
                    total_amount=total_amount,
                    items=order_details,
                    payment_method=payment_method
                )
            except Exception as bk_error:
                print(f"Failed to record bookkeeping: {bk_error}")

            # Create notification (Async ideal, but sync for now)
            try:
                self.notification_service.create_notification(
                    title="Đơn hàng mới",
                    message=f"Đơn hàng #{order_model.id} đã được tạo thành công. Tổng tiền: {order_model.total_amount:,.0f}đ",
                    user_id=user_id,
                    type="new_order"
                )
            except Exception as notify_error:
                print(f"Failed to send notification: {notify_error}")
            
            return {
                "success": True,
                "message": "Order created successfully",
                "order": Order(
                    id=order_model.id,
                    user_id=order_model.user_id,
                    total_amount=order_model.total_amount,
                    details=[
                        OrderDetail(
                            product_id=d["product_id"],
                            quantity=d["quantity"],
                            price=d["price"]
                        ) for d in order_details
                    ]
                )
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                "success": False,
                "message": f"Failed to create order: {str(e)}"
            }
    
    def get_orders(self, page: int = 1, per_page: int = 10) -> Dict:
        """
        Lấy danh sách đơn hàng phân trang
        """
        try:
            pagination = OrderModel.query.order_by(OrderModel.created_at.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            orders = []
            for order in pagination.items:
                # Get customer name
                from src.infrastructure.models.customer_model import CustomerModel
                customer = CustomerModel.query.get(order.customer_id) if order.customer_id else None
                customer_name = customer.name if customer else "Khách lẻ"
                
                # Get user name
                user = UserModel.query.get(order.user_id)
                user_name = user.full_name if user else "Unknown"

                orders.append({
                    "id": order.id,
                    "customer_name": customer_name,
                    "created_by": user_name,
                    "total_amount": order.total_amount,
                    "payment_method": order.payment_method,
                    "created_at": order.created_at.isoformat() if order.created_at else None
                })
            
            return {
                "success": True,
                "orders": orders,
                "total": pagination.total,
                "pages": pagination.pages,
                "current_page": page
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "orders": []
            }
    
    def get_order_print_html(self, order_id: int) -> Dict:
        """
        Lấy HTML hóa đơn để in
        Returns: {"success": bool, "html": str or None, "message": str}
        """
        try:
            # Lấy order từ database
            order = db.session.query(OrderModel).filter(OrderModel.id == order_id).first()
            if not order:
                return {
                    "success": False,
                    "html": None,
                    "message": "Không tìm thấy đơn hàng"
                }
            
            # Lấy thông tin user (shop owner)
            user = db.session.query(UserModel).filter(UserModel.id == order.user_id).first()
            shop_name = user.full_name if user else "BizFlow Shop"
            
            # Lấy chi tiết đơn hàng
            details = db.session.query(OrderDetailModel).filter(
                OrderDetailModel.order_id == order_id
            ).all()
            
            # Build HTML
            html = self._generate_invoice_html(order, shop_name, details)
            
            return {
                "success": True,
                "html": html,
                "message": "Lấy mẫu in thành công"
            }
            
        except Exception as e:
            return {
                "success": False,
                "html": None,
                "message": f"Lỗi: {str(e)}"
            }
    
    def _generate_invoice_html(self, order: OrderModel, shop_name: str, details: List[OrderDetailModel]) -> str:
        """
        Generate HTML hóa đơn
        """
        # Định dạng ngày
        order_date = order.created_at.strftime("%d/%m/%Y %H:%M") if order.created_at else "N/A"
        
        # Tạo danh sách hàng hóa
        items_html = ""
        for detail in details:
            product = db.session.query(ProductModel).filter(
                ProductModel.id == detail.product_id
            ).first()
            product_name = product.name if product else "Sản phẩm không xác định"
            line_total = detail.quantity * detail.price
            
            items_html += f"""
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">{product_name}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">{detail.quantity}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: right;">{detail.price:,.0f}đ</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: right;">{line_total:,.0f}đ</td>
            </tr>
            """
        
        # Format tổng tiền
        total_amount = order.total_amount
        
        # HTML template
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Hóa đơn #{order.id}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }}
                .invoice {{
                    background-color: white;
                    padding: 30px;
                    max-width: 600px;
                    margin: 0 auto;
                    border: 1px solid #ddd;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    border-bottom: 2px solid #333;
                    padding-bottom: 20px;
                    margin-bottom: 20px;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 24px;
                    color: #333;
                }}
                .header p {{
                    margin: 5px 0;
                    color: #666;
                    font-size: 14px;
                }}
                .order-info {{
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 20px;
                    font-size: 14px;
                }}
                .order-info div {{
                    flex: 1;
                }}
                .order-info .label {{
                    font-weight: bold;
                    color: #333;
                }}
                .order-info .value {{
                    color: #666;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th {{
                    background-color: #f0f0f0;
                    padding: 10px;
                    border: 1px solid #ddd;
                    text-align: left;
                    font-weight: bold;
                    font-size: 14px;
                }}
                td {{
                    padding: 8px;
                    border: 1px solid #ddd;
                    font-size: 14px;
                }}
                .summary {{
                    margin-top: 20px;
                    border-top: 2px solid #333;
                    padding-top: 15px;
                }}
                .summary-row {{
                    display: flex;
                    justify-content: flex-end;
                    margin-bottom: 10px;
                    font-size: 14px;
                }}
                .summary-row .label {{
                    font-weight: bold;
                    margin-right: 50px;
                }}
                .summary-row .value {{
                    min-width: 150px;
                    text-align: right;
                }}
                .total {{
                    display: flex;
                    justify-content: flex-end;
                    font-size: 18px;
                    font-weight: bold;
                    color: #d32f2f;
                    margin-top: 15px;
                    padding-top: 15px;
                    border-top: 2px solid #d32f2f;
                }}
                .total .label {{
                    margin-right: 50px;
                }}
                .total .value {{
                    min-width: 150px;
                    text-align: right;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    color: #999;
                    font-size: 12px;
                }}
                @media print {{
                    body {{
                        background-color: white;
                        margin: 0;
                    }}
                    .invoice {{
                        box-shadow: none;
                        border: none;
                        max-width: 100%;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="invoice">
                <div class="header">
                    <h1>HÓA ĐƠN</h1>
                    <p>Số: #{order.id}</p>
                </div>
                
                <div class="order-info">
                    <div>
                        <p><span class="label">Người mua:</span> <span class="value">{order.customer.name if order.customer else 'Khách lẻ'}</span></p>
                        <p><span class="label">Ngày:</span> <span class="value">{order_date}</span></p>
                    </div>
                    <div>
                        <p><span class="label">Cửa hàng:</span> <span class="value">{shop_name}</span></p>
                        <p><span class="label">Mã đơn hàng:</span> <span class="value">{order.id}</span></p>
                    </div>
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th>Tên sản phẩm</th>
                            <th style="text-align: center; width: 80px;">Số lượng</th>
                            <th style="text-align: right; width: 100px;">Đơn giá</th>
                            <th style="text-align: right; width: 100px;">Thành tiền</th>
                        </tr>
                    </thead>
                    <tbody>
                        {items_html}
                    </tbody>
                </table>
                
                <div class="summary">
                    <div class="summary-row">
                        <span class="label">Tổng tiền:</span>
                        <span class="value">{total_amount:,.0f}đ</span>
                    </div>
                </div>
                
                <div class="total">
                    <span class="label">TỔNG CỘNG:</span>
                    <span class="value">{total_amount:,.0f}đ</span>
                </div>
                
                <div class="footer">
                    <p>Cảm ơn bạn đã mua hàng!</p>
                    <p>In lúc: {datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
