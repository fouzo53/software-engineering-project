from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from src.domain.models.product import Product


class IProductRepository(ABC):
    @abstractmethod
    def add(self, product: Product) -> Product:
        raise NotImplementedError("Method add must be implemented")

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        raise NotImplementedError("Method get_by_id must be implemented")

    @abstractmethod
    def list_paginated(self, page: int, per_page: int) -> Tuple[List[Product], int]:
        raise NotImplementedError("Method list_paginated must be implemented")

    @abstractmethod
    def update(self, product: Product) -> Optional[Product]:
        raise NotImplementedError("Method update must be implemented")

    @abstractmethod
    def update_stock(self, product_id: int, stock: int, commit: bool = True) -> Optional[Product]:
        raise NotImplementedError("Method update_stock must be implemented")

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        raise NotImplementedError("Method delete must be implemented")

    @abstractmethod
    def get_low_stock(self, threshold: int = 10) -> List[Product]:
        raise NotImplementedError("Method get_low_stock must be implemented")

    @abstractmethod
    def import_stock(self, product_id: int, quantity: int, cost_price: float) -> Optional[Product]:
        raise NotImplementedError("Method import_stock must be implemented")
