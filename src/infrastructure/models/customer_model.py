from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from src.infrastructure.databases.database import db


class CustomerModel(db.Model):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False, unique=True)
    address = Column(String(255))
    debt_amount = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    debt_transactions = relationship('DebtTransactionModel', back_populates='customer', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'address': self.address,
            'debt_amount': self.debt_amount,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class DebtTransactionModel(db.Model):
    __tablename__ = 'debt_transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    transaction_type = Column(String(20), nullable=False)  # 'debt' hoặc 'payment'
    amount = Column(Float, nullable=False)
    note = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    customer = relationship('CustomerModel', back_populates='debt_transactions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'transaction_type': self.transaction_type,
            'amount': self.amount,
            'note': self.note,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
