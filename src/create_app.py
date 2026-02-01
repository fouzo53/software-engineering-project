from flask import Flask
from flasgger import Swagger
from flask_injector import FlaskInjector
from .config import Config, SwaggerConfig
from .cors import configure_cors
from .error_handler import register_error_handlers
from .api.security_headers import add_security_headers
from .api.request_logging import setup_request_logging
from .dependency_container import configure
from .infrastructure.databases.database import init_db

from .api.controllers.auth_controller import auth_bp
from .api.controllers.product_controller import product_bp
from .api.controllers.order_controller import order_bp
from .api.controllers.ai_controller import ai_bp
from .api.controllers.report_controller import report_bp
from .api.controllers.customer_controller import customer_bp
from .api.controllers.employee_controller import employee_bp
from .api.controllers.admin_controller import admin_bp
from .api.health_check import health_bp


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Thiết lập chuỗi kết nối SQLAlchemy nếu chưa có
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        app.config["SQLALCHEMY_DATABASE_URI"] = app.config.get("DATABASE_URI")

    # Tắt track modifications để giảm overhead
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    # Configure CORS for Frontend access
    configure_cors(app)
    # Setup security headers
    add_security_headers(app)
    
    # Setup request logging
    setup_request_logging(app)
    
    # Setup error handlers
    register_error_handlers(app)
    
    Swagger(app, template=SwaggerConfig.template, config=SwaggerConfig.swagger_config)
    init_db(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(health_bp)

    # Enable dependency injection
    FlaskInjector(app=app, modules=[configure])

    return app
