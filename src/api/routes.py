from flask import Blueprint

api = Blueprint("api", __name__)

@api.route("/health", methods=["GET"])
def health_check():
    return {"status": "OK"}, 200

from src.api.health_check import health_bp
from src.api.controllers.auth_controller import auth_bp
from src.api.controllers.customer_controller import customer_bp
from src.api.controllers.product_controller import product_bp
from src.api.controllers.order_controller import order_bp
from src.api.controllers.employee_controller import employee_bp
from src.api.controllers.todo_controller import todo_bp
from src.api.controllers.category_controller import category_bp

def register_routes(app):
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(todo_bp)
    app.register_blueprint(category_bp)