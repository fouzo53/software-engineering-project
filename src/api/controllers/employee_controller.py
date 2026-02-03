from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.api.schemas.employee_schema import EmployeeCreateSchema, EmployeeSchema, EmployeeStatusSchema
from src.services.employee_service import EmployeeService
from src.api.middleware import owner_required

employee_bp = Blueprint('employee', __name__, url_prefix='/api/employees')


@employee_bp.route('', methods=['POST'])
@owner_required
def create_employee(employee_service: EmployeeService):
    """
    Tạo tài khoản nhân viên mới (Chỉ Owner)
    ---
    tags:
      - Employee
    security:
      - Bearer: []
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer JWT token (Chỉ Owner)
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
              description: Tên đăng nhập
              example: nhanvien01
            password:
              type: string
              description: Mật khẩu (tối thiểu 6 ký tự)
              example: password123
            full_name:
              type: string
              description: Họ và tên
              example: Nguyễn Văn A
    responses:
      201:
        description: Tạo tài khoản nhân viên thành công
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            employee:
              type: object
              properties:
                id:
                  type: integer
                username:
                  type: string
                full_name:
                  type: string
                role:
                  type: string
                  example: employee
                status:
                  type: string
                  example: active
      400:
        description: Dữ liệu không hợp lệ
      403:
        description: Không có quyền truy cập
    """
    try:
        # Validate input
        schema = EmployeeCreateSchema()
        data = schema.load(request.get_json())
        
        # Check subscription limit
        from src.infrastructure.models.user_model import UserModel
        from src.services.subscription_service import SubscriptionService
        
        user_id = request.current_user['user_id']
        user = UserModel.query.get(user_id)
        
        current_employees_count = UserModel.query.filter_by(role='employee').count()
        subscription_service = SubscriptionService()
        
        if not subscription_service.check_limit(user, 'employees', current_employees_count):
            return jsonify({"error": "Đã đạt giới hạn số lượng nhân viên của gói hiện tại. Vui lòng nâng cấp!"}), 403

        # Create employee
        result = employee_service.create_employee(
            username=data['username'],
            password=data['password'],
            full_name=data['full_name']
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify({'error': result['message']}), 400
            
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400


@employee_bp.route('', methods=['GET'])
@owner_required
def get_all_employees(employee_service: EmployeeService):
    """
    Danh sách nhân viên của cửa hàng (Chỉ Owner)
    ---
    tags:
      - Employee
    security:
      - Bearer: []
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer JWT token (Chỉ Owner)
    responses:
      200:
        description: Lấy danh sách nhân viên thành công
        schema:
          type: object
          properties:
            message:
              type: string
              example: Có 5 nhân viên
            employees:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  username:
                    type: string
                  full_name:
                    type: string
                  role:
                    type: string
                    example: employee
                  status:
                    type: string
                    enum: [active, inactive]
      403:
        description: Không có quyền truy cập
    """
    employees = employee_service.get_all_employees()
    
    schema = EmployeeSchema(many=True)
    return jsonify({
        'message': f'Có {len(employees)} nhân viên',
        'employees': schema.dump(employees)
    }), 200


@employee_bp.route('/<int:id>/status', methods=['PUT'])
@owner_required
def update_employee_status(id: int, employee_service: EmployeeService):
    """
    Khóa/Mở khóa tài khoản nhân viên (Chỉ Owner)
    ---
    tags:
      - Employee
    security:
      - Bearer: []
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer JWT token (Chỉ Owner)
      - in: path
        name: id
        type: integer
        required: true
        description: ID nhân viên
        example: 1
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - status
          properties:
            status:
              type: string
              enum: [active, inactive]
              description: Trạng thái tài khoản (active - hoạt động, inactive - khóa)
              example: inactive
    responses:
      200:
        description: Cập nhật trạng thái thành công
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
      404:
        description: Không tìm thấy nhân viên
      403:
        description: Không có quyền truy cập
    """
    try:
        # Validate input
        schema = EmployeeStatusSchema()
        data = schema.load(request.get_json())
        
        # Update status
        result = employee_service.update_employee_status(id, data['status'])
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify({'error': result['message']}), 404
            
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400


@employee_bp.route('/<int:id>', methods=['DELETE'])
@owner_required
def delete_employee(id: int, employee_service: EmployeeService):
    """
    Xóa nhân viên (Chỉ Owner)
    ---
    tags:
      - Employee
    security:
      - Bearer: []
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer JWT token (Chỉ Owner)
      - in: path
        name: id
        type: integer
        required: true
        description: ID nhân viên cần xóa
        example: 1
    responses:
      200:
        description: Xóa nhân viên thành công
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
      404:
        description: Không tìm thấy nhân viên
      403:
        description: Không có quyền truy cập
    """
    result = employee_service.delete_employee(id)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify({'error': result['message']}), 404
