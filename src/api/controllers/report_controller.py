from flask import Blueprint, request, jsonify, g
from src.api.middleware import owner_required
from src.services.report_service import ReportService

report_bp = Blueprint('report', __name__, url_prefix='/api/reports')


@report_bp.route('/revenue', methods=['GET'])
@owner_required
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
    # Check role (only owner can view reports)
    # Handled by @owner_required decorator
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date are required"}), 400
    
    result = report_service.get_daily_revenue(start_date, end_date)
    
    return jsonify(result), 200


@report_bp.route('/tax', methods=['GET'])
@owner_required
def export_tax_report(report_service: ReportService):
    """
    Xuất báo cáo thuế
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
      - in: query
        name: end_date
        type: string
        required: true
        description: End date (YYYY-MM-DD)
    responses:
      200:
        description: Báo cáo thuế chi tiết
        schema:
          type: object
          properties:
            summary:
              type: object
              properties:
                total_orders:
                  type: integer
                total_revenue:
                  type: number
                total_tax_amount:
                  type: number
            details:
              type: array
              items:
                type: object
      400:
        description: Thiếu tham số
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date are required"}), 400
    
    try:
        result = report_service.export_tax_report(start_date, end_date)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@report_bp.route('/ledger/revenue', methods=['GET'])
@owner_required
def get_revenue_ledger_report(report_service: ReportService):
    """
    Sổ chi tiết doanh thu (S1-HKD)
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
      - in: query
        name: end_date
        type: string
        required: true
        description: End date (YYYY-MM-DD)
    responses:
      200:
        description: Sổ chi tiết doanh thu theo mẫu S1-HKD
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date are required"}), 400
        
    try:
        result = report_service.get_revenue_ledger(start_date, end_date)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@report_bp.route('/ledger/cash', methods=['GET'])
@owner_required
def get_cash_book_report(report_service: ReportService):
    """
    Sổ quỹ tiền mặt (S4-HKD)
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
      - in: query
        name: end_date
        type: string
        required: true
        description: End date (YYYY-MM-DD)
    responses:
      200:
        description: Sổ quỹ tiền mặt theo mẫu S4-HKD
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date are required"}), 400
        
    try:
        result = report_service.get_cash_book(start_date, end_date)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
