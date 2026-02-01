from typing import List, Dict
from injector import inject
from src.domain.models.product import Product
from src.domain.interfaces.product_repository import IProductRepository
from src.domain.interfaces.category_repository import ICategoryRepository


class ProductService:
    """Service xử lý logic nghiệp vụ cho Product"""
    
    @inject
    def __init__(self, product_repository: IProductRepository, category_repository: ICategoryRepository):
        self.product_repository = product_repository
        self.category_repository = category_repository
    
    def create_product(self, name: str, price: float, stock: int, category_id: int) -> Dict:
        """
        Tạo product mới (chỉ owner mới được tạo)
        Returns: {"success": bool, "message": str, "product": Product}
        """
        # Kiểm tra category có tồn tại không
        category = self.category_repository.get_by_id(category_id)
        if not category:
            return {"success": False, "message": "Category not found"}
        
        # Tạo product
        new_product = Product(
            name=name,
            price=price,
            stock=stock,
            category_id=category_id
        )
        
        saved_product = self.product_repository.add(new_product)
        
        return {
            "success": True,
            "message": "Product created successfully",
            "product": saved_product
        }
    
    def get_list(self, page: int = 1, per_page: int = 10) -> List[Product]:
        """Lấy danh sách products với pagination"""
        return self.product_repository.get_all(page=page, per_page=per_page)
    
    def update_stock(self, product_id: int, quantity: int) -> Dict:
        """
        Cập nhật stock (dùng khi tạo order)
        Returns: {"success": bool, "message": str}
        """
        success = self.product_repository.update_stock(product_id, quantity, commit=True)
        
        if success:
            return {"success": True, "message": "Stock updated successfully"}
        else:
            return {"success": False, "message": "Failed to update stock (not enough stock or product not found)"}
    
    def import_stock(self, product_id: int, quantity: int, cost_price: float) -> Dict:
        """
        Nhập hàng vào kho
        Cộng thêm số lượng và cập nhật giá vốn trung bình
        Returns: {"success": bool, "message": str, "product": Product}
        """
        product = self.product_repository.import_stock(product_id, quantity, cost_price)
        
        if product:
            return {
                "success": True,
                "message": "Nhập hàng thành công",
                "product": product
            }
        else:
            return {
                "success": False,
                "message": "Không tìm thấy sản phẩm"
            }
    
    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """
        Lấy danh sách sản phẩm sắp hết hàng
        Returns: List[Product]
        """
        return self.product_repository.get_low_stock(threshold)
