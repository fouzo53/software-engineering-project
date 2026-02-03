from flask import Blueprint, request, jsonify
from src.api.middleware import token_required
from src.services.notification_service import NotificationService

notification_bp = Blueprint('notification', __name__, url_prefix='/api/notifications')

@notification_bp.route('', methods=['GET'])
@token_required
def get_notifications(notification_service: NotificationService):
    """
    Lấy danh sách thông báo
    ---
    tags:
      - Notification
    security:
      - Bearer: []
    parameters:
      - in: query
        name: unread_only
        type: boolean
        default: false
    """
    user_id = request.current_user.get('user_id')
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    
    notifications = notification_service.get_notifications(user_id, unread_only)
    return jsonify(notifications), 200

@notification_bp.route('/<int:id>/read', methods=['PUT'])
@token_required
def mark_read(id: int, notification_service: NotificationService):
    """
    Đánh dấu đã đọc thông báo
    ---
    tags:
      - Notification
    security:
      - Bearer: []
    """
    user_id = request.current_user.get('user_id')
    result = notification_service.mark_read(id, user_id)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify({"error": result['message']}), 404

@notification_bp.route('/read-all', methods=['PUT'])
@token_required
def mark_all_read(notification_service: NotificationService):
    """
    Đánh dấu đã đọc tất cả
    ---
    tags:
      - Notification
    security:
      - Bearer: []
    """
    user_id = request.current_user.get('user_id')
    result = notification_service.mark_all_read(user_id)
    return jsonify(result), 200
