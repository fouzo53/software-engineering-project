from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.api.schemas.admin_schema import (
    OwnerSchema, SubscriptionUpdateSchema, 
    PlatformStatsSchema, ReportConfigSchema
)
from src.services.admin_service import AdminService
from src.api.middleware import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')


@admin_bp.route('/owners', methods=['GET'])
@admin_required
def get_all_owners(admin_service: AdminService):
    """
    Xem danh sách các Hộ kinh doanh đang hoạt động (Chỉ Admin)
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer JWT token (Chỉ Admin)
    responses:
      200:
        description: Danh sách chủ hộ kinh doanh
        schema:
          type: object
          properties:
            message:
              type: string
              example: Có 10 hộ kinh doanh
            owners:
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
                  status:
                    type: string
                    enum: [active, inactive]
                  subscription:
                    type: string
                    enum: [basic, pro]
      403:
        description: Không có quyền truy cập
    """
    owners = admin_service.get_all_owners()
    
    schema = OwnerSchema(many=True)
    return jsonify({
        'message': f'Có {len(owners)} hộ kinh doanh',
        'owners': schema.dump(owners)
    }), 200


@admin_bp.route('/owners/<int:id>/subscription', methods=['PUT'])
@admin_required
def update_owner_subscription(id: int, admin_service: AdminService):
    """
    Cập nhật gói cước (Basic/Pro) cho chủ hộ (Chỉ Admin)
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer JWT token (Chỉ Admin)
      - in: path
        name: id
        type: integer
        required: true
        description: ID chủ hộ
        example: 1
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - subscription
          properties:
            subscription:
              type: string
              enum: [basic, pro]
              description: Gói cước (basic - Cơ bản, pro - Nâng cao)
              example: pro
    responses:
      200:
        description: Cập nhật gói cước thành công
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
      404:
        description: Không tìm thấy chủ hộ
      403:
        description: Không có quyền truy cập
    """
    try:
        # Validate input
        schema = SubscriptionUpdateSchema()
        data = schema.load(request.get_json())
        
        # Update subscription
        result = admin_service.update_owner_subscription(id, data['subscription'])
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify({'error': result['message']}), 404
            
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400


@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_platform_stats(admin_service: AdminService):
    """
    Xem thống kê toàn sàn (Chỉ Admin)
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer JWT token (Chỉ Admin)
    responses:
      200:
        description: Thống kê toàn sàn
        schema:
          type: object
          properties:
            total_users:
              type: integer
              description: Tổng số users trong hệ thống
              example: 150
            total_orders_this_month:
              type: integer
              description: Tổng đơn hàng trong tháng hiện tại
              example: 320
            month:
              type: string
              description: Tháng thống kê (YYYY-MM)
              example: "2026-01"
            stats_date:
              type: string
              description: Thời điểm lấy thống kê
              example: "2026-01-31T10:30:00"
      403:
        description: Không có quyền truy cập
    """
    stats = admin_service.get_platform_stats()
    
    schema = PlatformStatsSchema()
    return jsonify(schema.dump(stats)), 200


@admin_bp.route('/config/reports', methods=['POST'])
@admin_required
def update_report_config(admin_service: AdminService):
    """
    Cập nhật mẫu báo cáo tài chính (Chỉ Admin)
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer JWT token (Chỉ Admin)
      - in: body
        name: body
        required: true
        schema:
          type: object
          description: Cấu hình báo cáo dạng JSON (Tùy chỉnh theo nhu cầu)
          properties:
            report_format:
              type: string
              description: Định dạng báo cáo
              example: pdf
            columns:
              type: array
              description: Các cột hiển thị trong báo cáo
              items:
                type: string
              example: ["Ngày", "Doanh thu", "Chi phí", "Lợi nhuận"]
            filters:
              type: object
              description: Bộ lọc mặc định
              properties:
                date_range:
                  type: string
                  example: last_30_days
            header:
              type: string
              description: Tiêu đề báo cáo
              example: BÁO CÁO TÀI CHÍNH THÁNG
            footer:
              type: string
              description: Chân trang báo cáo
              example: "Người lập báo cáo: {username}"
    responses:
      200:
        description: Cập nhật config thành công
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            config:
              type: object
              description: Config vừa được lưu
      400:
        description: Dữ liệu không hợp lệ
      403:
        description: Không có quyền truy cập
    """
    try:
        config_data = request.get_json()
        
        if not config_data or not isinstance(config_data, dict):
            return jsonify({'error': 'Config phải là object JSON hợp lệ'}), 400
        
        # Update config
        result = admin_service.update_report_config(config_data)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify({'error': result['message']}), 400
            
    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 400


@admin_bp.route('/config/reports', methods=['GET'])
@admin_required
def get_report_config(admin_service: AdminService):
    """
    Xem mẫu báo cáo tài chính hiện tại (Chỉ Admin)
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer JWT token (Chỉ Admin)
    responses:
      200:
        description: Cấu hình báo cáo hiện tại
        schema:
          type: object
          properties:
            config:
              type: object
              description: Cấu hình báo cáo dạng JSON
      404:
        description: Chưa có cấu hình báo cáo
      403:
        description: Không có quyền truy cập
    """
    config = admin_service.get_report_config()
    
    if config:
        return jsonify({'config': config}), 200
    else:
        return jsonify({'error': 'Chưa có cấu hình báo cáo'}), 404
