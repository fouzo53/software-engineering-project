"""
Security Headers Middleware
Adds important security headers to all responses
"""

from flask import Flask


def add_security_headers(app: Flask):
    """
    Add security headers to all responses
    Protects against common web vulnerabilities
    """
    
    @app.after_request
    def set_security_headers(response):
        # Prevent clickjacking attacks
        response.headers['X-Frame-Options'] = 'DENY'
        
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Enable XSS protection in older browsers
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer Policy - don't send referrer to external sites
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy - restrict browser features
        response.headers['Permissions-Policy'] = (
            'geolocation=(), '
            'microphone=(), '
            'camera=(), '
            'payment=(), '
            'usb=(), '
            'magnetometer=(), '
            'gyroscope=(), '
            'accelerometer=()'
        )
        
        # Strict Transport Security (only in production)
        # response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # Content Security Policy (permissive by default, tighten as needed)
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' https:; "
            "frame-ancestors 'none'"
        )
        
        return response
