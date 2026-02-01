"""
Global Error Handler for Flask Application
Handles all exceptions and returns consistent error responses
"""

from flask import Flask, jsonify
from marshmallow import ValidationError


def register_error_handlers(app: Flask):
    """Register global error handlers for the application."""
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request"""
        return jsonify({
            'success': False,
            'error': 'Yêu cầu không hợp lệ',
            'message': str(error)
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 Unauthorized"""
        return jsonify({
            'success': False,
            'error': 'Chưa xác thực',
            'message': 'Vui lòng đăng nhập để tiếp tục'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 Forbidden"""
        return jsonify({
            'success': False,
            'error': 'Truy cập bị từ chối',
            'message': 'Bạn không có quyền truy cập tài nguyên này'
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found"""
        return jsonify({
            'success': False,
            'error': 'Không tìm thấy',
            'message': 'Endpoint hoặc tài nguyên không tồn tại'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 Method Not Allowed"""
        return jsonify({
            'success': False,
            'error': 'Phương thức không được phép',
            'message': f'Phương thức HTTP này không được hỗ trợ'
        }), 405
    
    @app.errorhandler(409)
    def conflict(error):
        """Handle 409 Conflict"""
        return jsonify({
            'success': False,
            'error': 'Xung đột dữ liệu',
            'message': str(error)
        }), 409
    
    @app.errorhandler(422)
    def unprocessable_entity(error):
        """Handle 422 Unprocessable Entity"""
        return jsonify({
            'success': False,
            'error': 'Không thể xử lý yêu cầu',
            'message': str(error)
        }), 422
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server Error"""
        return jsonify({
            'success': False,
            'error': 'Lỗi máy chủ nội bộ',
            'message': 'Đã xảy ra lỗi khi xử lý yêu cầu'
        }), 500
    
    @app.errorhandler(502)
    def bad_gateway(error):
        """Handle 502 Bad Gateway"""
        return jsonify({
            'success': False,
            'error': 'Gateway không hợp lệ',
            'message': 'Máy chủ tạm thời không khả dụng'
        }), 502
    
    @app.errorhandler(503)
    def service_unavailable(error):
        """Handle 503 Service Unavailable"""
        return jsonify({
            'success': False,
            'error': 'Dịch vụ không khả dụng',
            'message': 'Máy chủ đang bảo trì, vui lòng thử lại sau'
        }), 503
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Handle Marshmallow validation errors"""
        return jsonify({
            'success': False,
            'error': 'Lỗi xác thực dữ liệu',
            'details': error.messages
        }), 422
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle unexpected exceptions"""
        # Log the error in production
        app.logger.error(f'Unhandled exception: {str(error)}', exc_info=True)
        
        return jsonify({
            'success': False,
            'error': 'Lỗi không mong muốn',
            'message': 'Vui lòng liên hệ với quản trị viên'
        }), 500
