from src.infrastructure.databases.database import db


class CategoryModel(db.Model):
    """SQLAlchemy model cho Category table"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    def __repr__(self):
        return f'<CategoryModel {self.name}>'
