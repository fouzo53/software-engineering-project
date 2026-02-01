from typing import List, Optional, Tuple
from src.domain.interfaces.product_repository import IProductRepository
from src.domain.models.product import Product
from src.infrastructure.models.product_model import ProductModel
from src.infrastructure.databases.database import db


class ProductRepositoryImpl(IProductRepository):
    """Concrete implementation của Product Repository"""
    
    def add(self, product: Product) -> Product:
        """Thêm product mới"""
        product_model = ProductModel(
            name=product.name,
            price=product.price,
            stock=product.stock,
            category_id=product.category_id
        )
        db.session.add(product_model)
        db.session.commit()
        
        product.id = product_model.id
        return product
    
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Lấy product theo ID"""
        product_model = ProductModel.query.get(product_id)
        if not product_model:
            return None
        
        return Product(
            id=product_model.id,
            name=product_model.name,
            price=product_model.price,
            cost_price=product_model.cost_price,
            stock=product_model.stock,
            category_id=product_model.category_id,
            image_url=product_model.image_url
        )
    
    def list_paginated(self, page: int = 1, per_page: int = 10) -> Tuple[List[Product], int]:
        """Lấy tất cả products với pagination"""
        pagination = ProductModel.query.paginate(page=page, per_page=per_page, error_out=False)
        
        products = [
            Product(
                id=p.id,
                name=p.name,
                price=p.price,
                cost_price=p.cost_price,
                stock=p.stock,
                category_id=p.category_id,
                image_url=p.image_url
            )
            for p in pagination.items
        ]
        return products, pagination.total
    
    def get_all(self, page: int = 1, per_page: int = 10) -> List[Product]:
        """Lấy tất cả products với pagination"""
        products = ProductModel.query.paginate(page=page, per_page=per_page, error_out=False)
        
        return [
            Product(
                id=p.id,
                name=p.name,
                price=p.price,
                cost_price=p.cost_price,
                stock=p.stock,
                category_id=p.category_id,
                image_url=p.image_url
            )
            for p in products.items
        ]
    
    def update_stock(self, product_id: int, stock: int, commit: bool = True) -> Optional[Product]:
        """Cập nhật stock với transaction-safe"""
        product = ProductModel.query.get(product_id)
        if not product:
            return None
        
        new_stock = product.stock - stock
        if new_stock < 0:
            return None
        
        product.stock = new_stock
        
        if commit:
            db.session.commit()
        
        return Product(
            id=product.id,
            name=product.name,
            price=product.price,
            cost_price=product.cost_price,
            stock=product.stock,
            category_id=product.category_id
        )
    
    def get_low_stock(self, threshold: int = 10) -> List[Product]:
        """Lấy danh sách sản phẩm sắp hết hàng"""
        products = ProductModel.query.filter(ProductModel.stock < threshold).all()
        
        return [
            Product(
                id=p.id,
                name=p.name,
                price=p.price,
                cost_price=p.cost_price,
                stock=p.stock,
                category_id=p.category_id
            )
            for p in products
        ]
    
    def update(self, product: Product) -> Optional[Product]:
        """Cập nhật thông tin sản phẩm"""
        product_model = ProductModel.query.get(product.id)
        if not product_model:
            return None
        
        product_model.name = product.name
        product_model.price = product.price
        product_model.cost_price = product.cost_price
        product_model.stock = product.stock
        product_model.category_id = product.category_id
        
        db.session.commit()
        
        return Product(
            id=product_model.id,
            name=product_model.name,
            price=product_model.price,
            cost_price=product_model.cost_price,
            stock=product_model.stock,
            category_id=product_model.category_id
        )
    
    def delete(self, product_id: int) -> bool:
        """Xóa sản phẩm"""
        product_model = ProductModel.query.get(product_id)
        if not product_model:
            return False
        
        db.session.delete(product_model)
        db.session.commit()
        return True
    
    def import_stock(self, product_id: int, quantity: int, cost_price: float) -> Optional[Product]:
        """Nhập hàng vào kho với cập nhật giá vốn trung bình"""
        product = ProductModel.query.get(product_id)
        if not product:
            return None
        
        # Tính giá vốn trung bình mới
        # Công thức: (Giá vốn cũ * Số lượng cũ + Giá vốn mới * Số lượng nhập) / Tổng số lượng
        old_total_cost = product.cost_price * product.stock
        new_total_cost = cost_price * quantity
        new_total_stock = product.stock + quantity
        
        if new_total_stock > 0:
            product.cost_price = (old_total_cost + new_total_cost) / new_total_stock
        
        # Cộng thêm số lượng vào stock
        product.stock = new_total_stock
        
        db.session.commit()
        
        return Product(
            id=product.id,
            name=product.name,
            price=product.price,
            cost_price=product.cost_price,
            stock=product.stock,
            category_id=product.category_id
        )
