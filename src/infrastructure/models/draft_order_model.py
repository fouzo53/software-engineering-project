from src.infrastructure.databases.database import db
from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from datetime import datetime
import json


class DraftOrderModel(db.Model):
    """Model để lưu đơn hàng nháp từ AI"""
    __tablename__ = 'draft_orders'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text_input = db.Column(db.Text, nullable=False)
    parsed_data = db.Column(db.Text, nullable=False)  # JSON string
    customer_id = db.Column(db.Integer, nullable=True)
    customer_name = db.Column(db.String(100), nullable=True)
    payment_method = db.Column(db.String(20), nullable=True)  # 'CASH' hoặc 'DEBT'
    total_amount = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='draft')  # 'draft' hoặc 'confirmed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    order_id = db.Column(db.Integer, nullable=True)  # ID của order thật sau khi confirm
    
    def to_dict(self):
        return {
            'id': self.id,
            'text_input': self.text_input,
            'parsed_data': json.loads(self.parsed_data) if self.parsed_data else {},
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'payment_method': self.payment_method,
            'total_amount': self.total_amount,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'confirmed_at': self.confirmed_at.isoformat() if self.confirmed_at else None,
            'order_id': self.order_id
        }
    
    def __repr__(self):
        return f'<DraftOrderModel {self.id}>'
