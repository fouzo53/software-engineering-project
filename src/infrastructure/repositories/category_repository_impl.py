from typing import List, Optional
from src.domain.interfaces.category_repository import ICategoryRepository
from src.domain.models.category import Category
from src.infrastructure.models.category_model import CategoryModel
from src.infrastructure.databases.database import db


class CategoryRepositoryImpl(ICategoryRepository):
    """Concrete implementation của Category Repository"""
    
    def get_by_id(self, category_id: int) -> Optional[Category]:
        """Lấy category theo ID"""
        category_model = CategoryModel.query.get(category_id)
        if not category_model:
            return None
        
        return Category(
            id=category_model.id,
            name=category_model.name
        )
    
    def list(self) -> List[Category]:
        """Lấy tất cả categories"""
        categories = CategoryModel.query.all()
        
        return [
            Category(
                id=c.id,
                name=c.name
            )
            for c in categories
        ]
    
    def get_all(self) -> List[Category]:
        """Lấy tất cả categories (alias cho list)"""
        return self.list()
    
    def add(self, category: Category) -> Category:
        """Thêm category mới"""
        category_model = CategoryModel(name=category.name)
        db.session.add(category_model)
        db.session.commit()
        
        category.id = category_model.id
        return category
    
    def update(self, category: Category) -> Optional[Category]:
        """Cập nhật category"""
        category_model = CategoryModel.query.get(category.id)
        if not category_model:
            return None
        
        category_model.name = category.name
        db.session.commit()
        
        return Category(
            id=category_model.id,
            name=category_model.name
        )
    
    def delete(self, category_id: int) -> bool:
        """Xóa category"""
        category_model = CategoryModel.query.get(category_id)
        if not category_model:
            return False
        
        db.session.delete(category_model)
        db.session.commit()
        return True
