from src.infrastructure.databases.database import db


class ProductModel(db.Model):
    """SQLAlchemy model cho Product table"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True) # Dùng cho AI Search
    price = db.Column(db.Float, nullable=False)
    cost_price = db.Column(db.Float, nullable=False, default=0.0)
    stock = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    unit = db.Column(db.String(50), nullable=False, default='cái')
    
    # Relationship
    category = db.relationship('CategoryModel', backref='products')
    
    def __repr__(self):
        return f'<ProductModel {self.name}>'
