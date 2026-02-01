"""
CORS Configuration for Flask Application
Allows Frontend (Next.js) to call API endpoints
"""

from flask_cors import CORS


def configure_cors(app):
    """
    Configure CORS for the Flask application
    
    Allows:
    - All origins (*) for development
    - Specific origin http://localhost:3000 for Next.js frontend
    - All HTTP methods (GET, POST, PUT, DELETE, PATCH, OPTIONS)
    - Credentials (cookies, authorization headers)
    """
    
    # Development: Allow all origins
    # Production: Specify allowed origins
    cors_config = {
        "origins": [
            "http://localhost:3000",  # Next.js frontend
            "http://127.0.0.1:3000",
            "http://localhost:5173",  # Vite frontend (if any)
            "http://127.0.0.1:5173",
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        "allow_headers": [
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "Accept",
            "Origin"
        ],
        "supports_credentials": True,
        "expose_headers": ["Content-Type", "Authorization"],
        "max_age": 3600  # Cache preflight requests for 1 hour
    }
    
    CORS(app, resources={r"/api/*": cors_config})
    
    return app
