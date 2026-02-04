"""
Health Check Endpoint for API Status Monitoring
Used for load balancers and uptime monitoring
"""

from flask import Blueprint, jsonify
from datetime import datetime
from src.infrastructure.databases.database import db
from sqlalchemy import text

health_bp = Blueprint('health', __name__, url_prefix='/api/health')


@health_bp.route('', methods=['GET'])
def health_check():
    """
    Kiểm tra trạng thái ứng dụng và kết nối cơ sở dữ liệu
    ---
    tags:
      - Health
    responses:
      200:
        description: Ứng dụng hoạt động bình thường
        schema:
          type: object
          properties:
            status:
              type: string
              example: healthy
            timestamp:
              type: string
              example: "2026-02-01T10:30:00"
            service:
              type: string
              example: Flask-CleanArchitecture
            version:
              type: string
              example: "1.0.0"
            database:
              type: string
              enum: [connected, disconnected]
              example: connected
      503:
        description: Dịch vụ không khả dụng
    """
    try:
        # Check database connection
        db.session.execute(text('SELECT 1'))
        db_status = 'connected'
    except Exception as e:
        db_status = 'disconnected'
    
    status_code = 200 if db_status == 'connected' else 503
    
    return jsonify({
        'status': 'healthy' if db_status == 'connected' else 'degraded',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'Flask-CleanArchitecture',
        'version': '1.0.0',
        'database': db_status
    }), status_code


@health_bp.route('/ready', methods=['GET'])
def readiness_check():
    """
    Kiểm tra xem ứng dụng đã sẵn sàng để nhận lưu lượng truy cập hay chưa
    ---
    tags:
      - Health
    responses:
      200:
        description: Ứng dụng sẵn sàng
        schema:
          type: object
          properties:
            ready:
              type: boolean
              example: true
      503:
        description: Ứng dụng chưa sẵn sàng
    """
    try:
        db.session.execute(text('SELECT 1'))
        return jsonify({'ready': True}), 200
    except Exception:
        return jsonify({'ready': False}), 503


@health_bp.route('/live', methods=['GET'])
def liveness_check():
    """
    Kiểm tra xem ứng dụng còn hoạt động hay không (lightweight check)
    ---
    tags:
      - Health
    responses:
      200:
        description: Ứng dụng còn hoạt động
        schema:
          type: object
          properties:
            alive:
              type: boolean
              example: true
    """
    return jsonify({'alive': True}), 200
