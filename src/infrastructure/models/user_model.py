from src.infrastructure.databases.database import db


class UserModel(db.Model):
    """SQLAlchemy model cho User table"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    full_name = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='active')
    subscription = db.Column(db.String(20), nullable=False, default='basic')
    
    def __repr__(self):
        return f'<UserModel {self.username}>'
