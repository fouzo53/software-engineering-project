from functools import wraps
from flask import request, jsonify
import jwt
from src.config import Config


def token_required(f):
    """Decorator để kiểm tra JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # JWT token in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                try:
                    token = auth_header.split(" ")[1]
                except IndexError:
                    return jsonify({'error': 'Token format invalid'}), 401
            else:
                # Nếu không có "Bearer ", coi toàn bộ chuỗi là token (tiện cho việc test Swagger)
                token = auth_header
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Decode token
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = {
                'user_id': data['user_id'],
                'username': data['username'],
                'role': data['role']
            }
            request.current_user = current_user
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token is invalid'}), 401
        
        return f(*args, **kwargs)
    
    return decorated


def owner_required(f):
    """Decorator để kiểm tra role owner"""
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        if not hasattr(request, 'current_user'):
            return jsonify({'error': 'Unauthorized'}), 401
        
        if request.current_user['role'] != 'owner':
            return jsonify({'error': 'Chỉ Owner mới có quyền truy cập'}), 403
        
        return f(*args, **kwargs)
    
    return decorated


def admin_required(f):
    """Decorator để kiểm tra role admin"""
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        if not hasattr(request, 'current_user'):
            return jsonify({'error': 'Unauthorized'}), 401
        
        if request.current_user['role'] != 'admin':
            return jsonify({'error': 'Chỉ Admin mới có quyền truy cập'}), 403
        
        return f(*args, **kwargs)
    
    return decorated


def staff_required(f):
    """Decorator để kiểm tra role owner hoặc employee"""
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        if not hasattr(request, 'current_user'):
            return jsonify({'error': 'Unauthorized'}), 401
        
        if request.current_user['role'] not in ['owner', 'employee']:
            return jsonify({'error': 'Chỉ Owner hoặc Nhân viên mới có quyền truy cập'}), 403
        
        return f(*args, **kwargs)
    
    return decorated
