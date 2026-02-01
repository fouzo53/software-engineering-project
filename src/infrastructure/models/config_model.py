from src.infrastructure.databases.database import db
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime


class ConfigModel(db.Model):
    """Model để lưu cấu hình hệ thống dạng JSON"""
    __tablename__ = 'system_configs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    config_key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    config_value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ConfigModel {self.config_key}>'
