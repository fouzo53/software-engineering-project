from flask import Blueprint, request, g
from src.api.middleware import token_required, owner_required, staff_required
from src.services.customer_service import CustomerService
from src.api.schemas.customer_schema import (
    CustomerSchema, CustomerCreateSchema, CustomerUpdateSchema,
    DebtTransactionSchema, DebtTransactionCreateSchema
)
from src.api.responses import success_response, error_response
from flasgger import swag_from

customer_bp = Blueprint('customer', __name__)


@customer_bp.route('/api/customers', methods=['POST'])
@token_required
def create_customer(customer_service: CustomerService):
    """
    Thêm khách hàng mới
    ---
    tags:
      - Customer
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - phone
            - address
          properties:
            name:
              type: string
              description: Tên khách hàng
              example: Nguyễn Văn A
            phone:
              type: string
              description: Số điện thoại
              example: "0123456789"
            address:
              type: string
              description: Địa chỉ
              example: Hà Nội
    responses:
      201:
        description: Thêm khách hàng thành công
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            data:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                phone:
                  type: string
                address:
                  type: string
                debt_amount:
                  type: number
                created_at:
                  type: string
      400:
        description: Dữ liệu không hợp lệ
    """
    try:
        # Validate input
        schema = CustomerCreateSchema()
        data = schema.load(request.get_json())
        
        # Create customer
        result = customer_service.create_customer(
            name=data['name'],
            phone=data['phone'],
            address=data['address']
        )
        
        return success_response(data=result, message="Thêm khách hàng thành công", status_code=201)
    except ValueError as e:
        return error_response(message=str(e), status_code=400)
    except Exception as e:
        return error_response(message=f"Lỗi: {str(e)}", status_code=500)


@customer_bp.route('/api/customers', methods=['GET'])
@token_required
def get_all_customers(customer_service: CustomerService):
    """
    Lấy danh sách khách hàng
    ---
    tags:
      - Customer
    security:
      - Bearer: []
    parameters:
      - in: query
        name: search
        type: string
        required: false
        description: Tìm kiếm theo tên hoặc số điện thoại
        example: Nguyễn
    responses:
      200:
        description: Lấy danh sách khách hàng thành công
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  phone:
                    type: string
                  address:
                    type: string
                  debt_amount:
                    type: number
                  created_at:
                    type: string
    """
    try:
        search = request.args.get('search', None)
        customers = customer_service.get_all_customers(search=search)
        
        return success_response(data=customers, message="Lấy danh sách khách hàng thành công")
    except Exception as e:
        return error_response(message=f"Lỗi: {str(e)}", status_code=500)


@customer_bp.route('/api/customers/<int:id>', methods=['GET'])
@token_required
def get_customer_by_id(id: int, customer_service: CustomerService):
    """
    Xem chi tiết khách hàng và tổng dư nợ hiện tại
    ---
    tags:
      - Customer
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID khách hàng
        example: 1
    responses:
      200:
        description: Lấy thông tin khách hàng thành công
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            data:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                phone:
                  type: string
                address:
                  type: string
                debt_amount:
                  type: number
                  description: Tổng dư nợ hiện tại
                created_at:
                  type: string
      404:
        description: Không tìm thấy khách hàng
    """
    try:
        customer = customer_service.get_customer_by_id(id)
        return success_response(data=customer, message="Lấy thông tin khách hàng thành công")
    except ValueError as e:
        return error_response(message=str(e), status_code=404)
    except Exception as e:
        return error_response(message=f"Lỗi: {str(e)}", status_code=500)


@customer_bp.route('/api/customers/<int:id>', methods=['PUT'])
@owner_required
def update_customer(id: int, customer_service: CustomerService):
    """
    Cập nhật thông tin khách hàng
    ---
    tags:
      - Customer
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID khách hàng
        example: 1
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - phone
            - address
          properties:
            name:
              type: string
              description: Tên khách hàng
              example: Nguyễn Văn B
            phone:
              type: string
              description: Số điện thoại
              example: "0987654321"
            address:
              type: string
              description: Địa chỉ
              example: Hồ Chí Minh
    responses:
      200:
        description: Cập nhật thông tin thành công
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            data:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                phone:
                  type: string
                address:
                  type: string
                debt_amount:
                  type: number
                created_at:
                  type: string
      404:
        description: Không tìm thấy khách hàng
    """
    try:
        # Validate input
        schema = CustomerUpdateSchema()
        data = schema.load(request.get_json())
        
        # Update customer
        result = customer_service.update_customer(
            customer_id=id,
            name=data['name'],
            phone=data['phone'],
            address=data['address']
        )
        
        return success_response(data=result, message="Cập nhật thông tin khách hàng thành công")
    except ValueError as e:
        return error_response(message=str(e), status_code=404)
    except Exception as e:
        return error_response(message=f"Lỗi: {str(e)}", status_code=500)


@customer_bp.route('/api/customers/<int:id>/debt-history', methods=['GET'])
@token_required
def get_debt_history(id: int, customer_service: CustomerService):
    """
    Xem lịch sử ghi nợ/trả nợ của khách hàng
    ---
    tags:
      - Customer
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID khách hàng
        example: 1
    responses:
      200:
        description: Lấy lịch sử ghi nợ/trả nợ thành công
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  customer_id:
                    type: integer
                  transaction_type:
                    type: string
                    enum: [debt, payment]
                    description: Loại giao dịch (debt - ghi nợ, payment - trả nợ)
                  amount:
                    type: number
                  note:
                    type: string
                  created_at:
                    type: string
      404:
        description: Không tìm thấy khách hàng
    """
    try:
        history = customer_service.get_debt_history(id)
        return success_response(data=history, message="Lấy lịch sử ghi nợ/trả nợ thành công")
    except ValueError as e:
        return error_response(message=str(e), status_code=404)
    except Exception as e:
        return error_response(message=f"Lỗi: {str(e)}", status_code=500)


@customer_bp.route('/api/customers/<int:id>/debt', methods=['POST'])
@staff_required
def add_debt(id: int, customer_service: CustomerService):
    """
    Thêm khoản nợ cho khách hàng
    ---
    tags:
      - Customer
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID khách hàng
        example: 1
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - amount
          properties:
            amount:
              type: number
              description: Số tiền nợ
              example: 100000
            note:
              type: string
              description: Ghi chú
              example: Mua hàng ngày 31/01
    responses:
      201:
        description: Thêm khoản nợ thành công
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            data:
              type: object
              properties:
                id:
                  type: integer
                customer_id:
                  type: integer
                transaction_type:
                  type: string
                amount:
                  type: number
                note:
                  type: string
                created_at:
                  type: string
      404:
        description: Không tìm thấy khách hàng
    """
    try:
        # Validate input
        schema = DebtTransactionCreateSchema()
        data = schema.load(request.get_json())
        
        # Add debt
        result = customer_service.add_debt(
            customer_id=id,
            amount=data['amount'],
            note=data.get('note')
        )
        
        return success_response(data=result, message="Thêm khoản nợ thành công", status_code=201)
    except ValueError as e:
        return error_response(message=str(e), status_code=400)
    except Exception as e:
        return error_response(message=f"Lỗi: {str(e)}", status_code=500)


@customer_bp.route('/api/customers/<int:id>/payment', methods=['POST'])
@token_required
def add_payment(id: int, customer_service: CustomerService):
    """
    Thêm khoản trả nợ của khách hàng
    ---
    tags:
      - Customer
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID khách hàng
        example: 1
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - amount
          properties:
            amount:
              type: number
              description: Số tiền trả
              example: 50000
            note:
              type: string
              description: Ghi chú
              example: Trả nợ ngày 31/01
    responses:
      201:
        description: Thêm khoản trả nợ thành công
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            data:
              type: object
              properties:
                id:
                  type: integer
                customer_id:
                  type: integer
                transaction_type:
                  type: string
                amount:
                  type: number
                note:
                  type: string
                created_at:
                  type: string
      404:
        description: Không tìm thấy khách hàng
    """
    try:
        # Validate input
        schema = DebtTransactionCreateSchema()
        data = schema.load(request.get_json())
        
        # Add payment
        result = customer_service.add_payment(
            customer_id=id,
            amount=data['amount'],
            note=data.get('note')
        )
        
        return success_response(data=result, message="Thêm khoản trả nợ thành công", status_code=201)
    except ValueError as e:
        return error_response(message=str(e), status_code=400)
    except Exception as e:
        return error_response(message=f"Lỗi: {str(e)}", status_code=500)
