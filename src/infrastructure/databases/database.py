from flask_sqlalchemy import SQLAlchemy

# Khởi tạo SQLAlchemy instance
db = SQLAlchemy()


def init_db(app):
    """
    Initialize database với Flask app
    Gọi hàm này trong create_app để kết nối database
    """
    db.init_app(app)
    
    with app.app_context():
        # Import tất cả models để SQLAlchemy có thể tạo tables
        from src.infrastructure.models.user_model import UserModel
        from src.infrastructure.models.category_model import CategoryModel
        from src.infrastructure.models.product_model import ProductModel
        from src.infrastructure.models.order_model import OrderModel, OrderDetailModel
        from src.infrastructure.models.customer_model import CustomerModel, DebtTransactionModel
        from src.infrastructure.models.config_model import ConfigModel
        from src.infrastructure.models.draft_order_model import DraftOrderModel
        
        # Tạo tất cả tables nếu chưa tồn tại
        db.create_all()
        print("✅ Database tables created successfully!")
