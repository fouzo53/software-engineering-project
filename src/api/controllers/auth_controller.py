from flask import Blueprint, request, jsonify, g
from marshmallow import ValidationError
from src.api.schemas.user_schema import LoginSchema, RegisterSchema, LoginResponseSchema, RegisterResponseSchema
from src.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login(auth_service: AuthService):
    """
    Đăng nhập hệ thống
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: "admin"
            password:
              type: string
              example: "password123"
    responses:
      200:
        description: Đăng nhập thành công
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            token:
              type: string
            user:
              type: object
              properties:
                id:
                  type: integer
                username:
                  type: string
                role:
                  type: string
                full_name:
                  type: string
      400:
        description: Lỗi dữ liệu đầu vào
      401:
        description: Tên đăng nhập hoặc mật khẩu không đúng
    """
    try:
        # Validate input
        schema = LoginSchema()
        data = schema.load(request.get_json())
        
        # Login
        result = auth_service.login(data['username'], data['password'])
        
        if result['success']:
            response_schema = LoginResponseSchema()
            return jsonify(response_schema.dump(result)), 200
        else:
            return jsonify({"error": result['message']}), 401
            
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400


@auth_bp.route('/register', methods=['POST'])
def register(auth_service: AuthService):
    """
    Đăng ký tài khoản mới
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
            - full_name
          properties:
            username:
              type: string
              example: "newuser"
            password:
              type: string
              example: "password123"
            full_name:
              type: string
              example: "Nguyen Van A"
            role:
              type: string
              example: "user"
              default: "user"
    responses:
      201:
        description: Đăng ký tài khoản thành công
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            user:
              type: object
              properties:
                id:
                  type: integer
                username:
                  type: string
                role:
                  type: string
                full_name:
                  type: string
      400:
        description: Lỗi dữ liệu hoặc tên đăng nhập đã tồn tại
      403:
        description: Chỉ Admin mới được tạo tài khoản
    """
    try:
        # Check if user is admin or owner (admin and owner can create accounts)
        if not g.user or g.user.get('role') not in ['admin', 'owner']:
            return jsonify({"error": "Chỉ Admin/Owner mới được tạo tài khoản!"}), 403
        
        # Validate input
        schema = RegisterSchema()
        data = schema.load(request.get_json())
        
        # Register
        result = auth_service.register(
            username=data['username'],
            password=data['password'],
            full_name=data['full_name'],
            role=data.get('role', 'user')
        )
        
        if result['success']:
            response_schema = RegisterResponseSchema()
            return jsonify(response_schema.dump(result)), 201
        else:
            return jsonify({"error": result['message']}), 400
            
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400


@auth_bp.route('/users', methods=['GET'])
def get_users(auth_service: AuthService):
    """
    Lấy danh sách người dùng (Admin hoặc Owner)
    ---
    tags:
      - Auth
    security:
      - Bearer: []
    responses:
      200:
        description: Danh sách người dùng
      403:
        description: Không có quyền truy cập
    """
    # Check if user is admin or owner
    if not g.user or g.user.get('role') not in ['admin', 'owner']:
        return jsonify({"error": "Chỉ Admin/Owner mới được xem danh sách tài khoản!"}), 403
    
    users = auth_service.get_all_users()
    return jsonify({"data": users}), 200


@auth_bp.route('/users/<int:user_id>/toggle-status', methods=['PUT'])
def toggle_user_status(user_id: int, auth_service: AuthService):
    """
    Kích hoạt/Vô hiệu hóa tài khoản (Chỉ Admin Platform)
    ---
    tags:
      - Auth
    security:
      - Bearer: []
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
    responses:
      200:
        description: Cập nhật trạng thái thành công
      403:
        description: Không có quyền truy cập
      404:
        description: Không tìm thấy user
    """
    # Chỉ admin platform mới được vô hiệu hóa tài khoản
    if not g.user or g.user.get('role') != 'admin':
        return jsonify({"error": "Chỉ Admin Platform mới được vô hiệu hóa tài khoản!"}), 403
    
    result = auth_service.toggle_user_status(user_id)
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify({"error": result['message']}), 404
