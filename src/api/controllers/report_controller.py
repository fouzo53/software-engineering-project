from flask import Blueprint, request, jsonify, g
from src.services.report_service import ReportService

report_bp = Blueprint('report', __name__, url_prefix='/api/reports')


@report_bp.route('/revenue', methods=['GET'])
def get_daily_revenue(report_service: ReportService):
    """
    Lấy báo cáo doanh thu theo ngày
    ---
    tags:
      - Report
    security:
      - Bearer: []
    parameters:
      - in: query
        name: start_date
        type: string
        required: true
        description: Start date (YYYY-MM-DD)
        example: "2024-01-01"
      - in: query
        name: end_date
        type: string
        required: true
        description: End date (YYYY-MM-DD)
        example: "2024-12-31"
    responses:
      200:
        description: Báo cáo doanh thu theo ngày
        schema:
          type: array
          items:
            type: object
            properties:
              date:
                type: string
                example: "2024-01-15"
              revenue:
                type: number
                example: 1500000
              order_count:
                type: integer
                example: 10
      400:
        description: Thiếu tham số bắt buộc
      403:
        description: Không có quyền (chỉ Owner)
    """
    # Check role (only owner can view reports)
    if g.user.get('role') != 'owner':
        return jsonify({"error": "Permission denied. Only owner can view reports."}), 403
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date are required"}), 400
    
    result = report_service.get_daily_revenue(start_date, end_date)
    
    return jsonify(result), 200
