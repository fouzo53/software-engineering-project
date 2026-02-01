"""
Request/Response Logging Middleware
Logs all API requests for debugging and monitoring
"""

import logging
from flask import Flask, request, g
from datetime import datetime
import time
import jwt
from src.config import Config

# Configure logger
logger = logging.getLogger('api_requests')


def setup_request_logging(app: Flask):
    """
    Setup request/response logging for the Flask application
    Logs method, path, status, response time, and IP address
    """
    
    @app.before_request
    def log_request_start():
        """Log incoming request details and extract JWT user"""
        g.start_time = time.time()
        g.request_id = request.headers.get('X-Request-ID', 'N/A')
        g.user = {}  # Default empty user
        
        # Extract JWT token and set g.user
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
                g.user = {
                    'user_id': payload.get('user_id'),
                    'username': payload.get('username'),
                    'role': payload.get('role')
                }
            except jwt.ExpiredSignatureError:
                g.user = {}
            except jwt.InvalidTokenError:
                g.user = {}
        
        logger.info(
            f"[{g.request_id}] {request.method} {request.path} - "
            f"IP: {request.remote_addr} - "
            f"User-Agent: {request.user_agent}"
        )
    
    @app.after_request
    def log_request_end(response):
        """Log response details"""
        if hasattr(g, 'start_time'):
            elapsed_time = time.time() - g.start_time
            request_id = getattr(g, 'request_id', 'N/A')
            
            log_level = logging.WARNING if response.status_code >= 400 else logging.INFO
            
            logger.log(
                log_level,
                f"[{request_id}] {request.method} {request.path} - "
                f"Status: {response.status_code} - "
                f"Time: {elapsed_time:.3f}s"
            )
        
        return response
