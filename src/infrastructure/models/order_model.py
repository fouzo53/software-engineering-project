from datetime import datetime
from src.infrastructure.databases.database import db


class OrderModel(db.Model):
    """SQLAlchemy model cho Order table"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), default='CASH')  # CASH or DEBT
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    details = db.relationship('OrderDetailModel', backref='order', lazy=True)
    customer = db.relationship('CustomerModel', backref='orders', lazy=True)
    
    def __repr__(self):
        return f'<OrderModel {self.id}>'


class OrderDetailModel(db.Model):
    """SQLAlchemy model cho OrderDetail table"""
    __tablename__ = 'order_details'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<OrderDetailModel order={self.order_id} product={self.product_id}>'
