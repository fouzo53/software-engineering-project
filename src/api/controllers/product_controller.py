from flask import Blueprint, request, jsonify, g
from src.api.middleware import token_required, owner_required
from marshmallow import ValidationError
from src.api.schemas.product_schema import ProductSchema, ProductImportSchema
from src.services.product_service import ProductService

product_bp = Blueprint('product', __name__, url_prefix='/api/products')


@product_bp.route('', methods=['POST'])
@owner_required
def create_product(product_service: ProductService):
    """
    Tạo sản phẩm mới (Chỉ Owner)
    ---
    tags:
      - Product
    security:
      - Bearer: []
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer JWT token
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - price
            - stock
            - category_id
          properties:
            name:
              type: string
              example: "Product A"
            price:
              type: number
              example: 100000
            stock:
              type: integer
              example: 50
            category_id:
              type: integer
              example: 1
    responses:
      201:
        description: Tạo sản phẩm thành công
      400:
        description: Lỗi dữ liệu đầu vào
      403:
        description: Không có quyền truy cập (chỉ Owner)
    """
    try:
        # Validate input
        schema = ProductSchema()
        data = schema.load(request.get_json())
        
        # Check subscription limit
        from src.infrastructure.models.user_model import UserModel
        from src.infrastructure.models.product_model import ProductModel
        from src.services.subscription_service import SubscriptionService
        
        user_id = request.current_user['user_id']
        user = UserModel.query.get(user_id)
        
        current_count = ProductModel.query.count()
        subscription_service = SubscriptionService()
        
        if not subscription_service.check_limit(user, 'products', current_count):
            return jsonify({"error": "Đã đạt giới hạn số lượng sản phẩm của gói hiện tại (Basic: 50). Vui lòng nâng cấp!"}), 403

        # Create product
        result = product_service.create_product(
            name=data['name'],
            price=data['price'],
            stock=data['stock'],
            category_id=data['category_id']
        )
        
        if result['success']:
            return jsonify(schema.dump(result['product'])), 201
        else:
            return jsonify({"error": result['message']}), 400
            
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400


@product_bp.route('', methods=['GET'])
@token_required
def get_products(product_service: ProductService):
    """
    Lấy danh sách sản phẩm
    ---
    tags:
      - Product
    parameters:
      - in: query
        name: page
        type: integer
        default: 1
        description: Page number
      - in: query
        name: per_page
        type: integer
        default: 10
        description: Items per page
    responses:
      200:
        description: Danh sách sản phẩm
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              price:
                type: number
              stock:
                type: integer
              category_id:
                type: integer
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    products = product_service.get_list(page=page, per_page=per_page)
    
    schema = ProductSchema(many=True)
    return jsonify({"data": schema.dump(products)}), 200


@product_bp.route('/import', methods=['POST'])
@owner_required
def import_stock(product_service: ProductService):
    """
    Nhập hàng vào kho
    ---
    tags:
      - Product
    security:
      - Bearer: []
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer JWT token (Owner only)
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - product_id
            - quantity
            - cost_price
          properties:
            product_id:
              type: integer
              description: ID sản phẩm cần nhập hàng
              example: 1
            quantity:
              type: integer
              description: Số lượng nhập
              example: 100
            cost_price:
              type: number
              description: Giá vốn mới (sẽ tính giá vốn trung bình)
              example: 50000
    responses:
      200:
        description: Nhập hàng thành công
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            product:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                price:
                  type: number
                cost_price:
                  type: number
                  description: Giá vốn trung bình sau khi nhập
                stock:
                  type: integer
                  description: Số lượng tồn kho sau khi nhập
                category_id:
                  type: integer
      400:
        description: Dữ liệu không hợp lệ
      403:
        description: Không có quyền (chỉ Owner)
      404:
        description: Không tìm thấy sản phẩm
    """
    try:
        
        # Validate input
        schema = ProductImportSchema()
        data = schema.load(request.get_json())
        
        # Import stock
        result = product_service.import_stock(
            product_id=data['product_id'],
            quantity=data['quantity'],
            cost_price=data['cost_price']
        )
        
        if result['success']:
            product_schema = ProductSchema()
            return jsonify({
                'success': True,
                'message': result['message'],
                'product': product_schema.dump(result['product'])
            }), 200
        else:
            return jsonify({'error': result['message']}), 404
            
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400


@product_bp.route('/low-stock', methods=['GET'])
@owner_required
def get_low_stock(product_service: ProductService):
    """
    Lấy danh sách sản phẩm sắp hết hàng
    ---
    tags:
      - Product
    security:
      - Bearer: []
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer JWT token
      - in: query
        name: threshold
        type: integer
        required: false
        default: 10
        description: Ngưỡng cảnh báo hết hàng (mặc định là 10)
        example: 10
    responses:
      200:
        description: Danh sách sản phẩm sắp hết hàng
        schema:
          type: object
          properties:
            message:
              type: string
              example: Có 3 sản phẩm sắp hết hàng
            products:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  price:
                    type: number
                  cost_price:
                    type: number
                  stock:
                    type: integer
                    description: Số lượng tồn kho hiện tại
                  category_id:
                    type: integer
    """
    threshold = request.args.get('threshold', 10, type=int)
    
    products = product_service.get_low_stock_products(threshold=threshold)
    
    schema = ProductSchema(many=True)
    return jsonify({
        'message': f'Có {len(products)} sản phẩm sắp hết hàng',
        'products': schema.dump(products)
    }), 200
