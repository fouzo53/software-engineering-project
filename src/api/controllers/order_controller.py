from flask import Blueprint, request, jsonify, g
from src.api.middleware import token_required
from marshmallow import ValidationError
from src.api.schemas.order_schema import CreateOrderSchema
from src.services.order_service import OrderService

order_bp = Blueprint('order', __name__, url_prefix='/api/orders')


@order_bp.route('', methods=['POST'])
@token_required
def create_order(order_service: OrderService):
    """
    Tạo đơn hàng mới
    ---
    tags:
      - Order
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - items
            - customer_id
          properties:
            customer_id:
              type: integer
              description: ID của khách hàng
              example: 1
            payment_method:
              type: string
              description: Phương thức thanh toán (CASH/DEBT)
              example: CASH
              default: CASH
            items:
              type: array
              items:
                type: object
                required:
                  - product_id
                  - quantity
                properties:
                  product_id:
                    type: integer
                    example: 1
                  quantity:
                    type: integer
                    example: 2
    responses:
      201:
        description: Tạo đơn hàng thành công
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            order:
              type: object
              properties:
                id:
                  type: integer
                user_id:
                  type: integer
                total_amount:
                  type: number
                details:
                  type: array
                  items:
                    type: object
                    properties:
                      product_id:
                        type: integer
                      quantity:
                        type: integer
                      price:
                        type: number
      400:
        description: Lỗi dữ liệu hoặc không đủ hàng tồn kho
    """
    try:
        # Validate input
        schema = CreateOrderSchema()
        json_data = request.get_json()
        print(f"[DEBUG] Order request data: {json_data}")
        data = schema.load(json_data)
        
        # Get user_id từ JWT token
        user_id = request.current_user.get('user_id')

        # Check subscription limit
        from src.infrastructure.models.user_model import UserModel
        from src.infrastructure.models.order_model import OrderModel
        from src.services.subscription_service import SubscriptionService
        from datetime import datetime, timedelta
        
        user = UserModel.query.get(user_id)
        # Assuming current month orders
        first_day_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        current_month_orders = OrderModel.query.filter(OrderModel.created_at >= first_day_of_month).count()
        
        subscription_service = SubscriptionService()
        if not subscription_service.check_limit(user, 'orders_per_month', current_month_orders):
            return jsonify({"error": "Đã đạt giới hạn số lượng đơn hàng trong tháng. Vui lòng nâng cấp gói dịch vụ!"}), 403

        # Create order
        result = order_service.create_order(
            user_id=user_id, 
            items=data['items'],
            customer_id=data['customer_id'],
            payment_method=data.get('payment_method', 'CASH')
        )
        
        print(f"[DEBUG] Order result: {result}")
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify({"error": result['message']}), 400
            
    except ValidationError as e:
        print(f"[DEBUG] Validation error: {e.messages}")
        return jsonify({"error": e.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@order_bp.route('', methods=['GET'])
@token_required
def get_orders(order_service: OrderService):
    """
    Lấy danh sách đơn hàng
    ---
    tags:
      - Order
    security:
      - Bearer: []
    parameters:
      - in: query
        name: page
        type: integer
        default: 1
      - in: query
        name: per_page
        type: integer
        default: 10
    responses:
      200:
        description: Danh sách đơn hàng
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    result = order_service.get_orders(page, per_page)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify({"error": result['message']}), 500


@order_bp.route('/<int:id>/print', methods=['GET'])
@token_required
def print_order(id: int, order_service: OrderService):
    """
    Lấy mẫu in hóa đơn
    ---
    tags:
      - Order
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID đơn hàng
        example: 1
    responses:
      200:
        description: Lấy mẫu in hóa đơn thành công
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            html:
              type: string
              description: HTML string của hóa đơn (chứa tên shop, khách, danh sách hàng, tổng tiền)
              example: "<html>...</html>"
            message:
              type: string
              example: "Lấy mẫu in thành công"
      404:
        description: Không tìm thấy đơn hàng
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            html:
              type: string
              nullable: true
            message:
              type: string
              example: "Không tìm thấy đơn hàng"
      500:
        description: Lỗi máy chủ
    """
    result = order_service.get_order_print_html(id)
    
    status_code = 200 if result['success'] else (404 if 'không tìm thấy' in result['message'] else 500)
    
    return jsonify(result), status_code
