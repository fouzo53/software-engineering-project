from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.category import Category


class ICategoryRepository(ABC):
    @abstractmethod
    def add(self, category: Category) -> Category:
        raise NotImplementedError("Method add must be implemented")

    @abstractmethod
    def get_by_id(self, category_id: int) -> Optional[Category]:
        raise NotImplementedError("Method get_by_id must be implemented")

    @abstractmethod
    def list(self) -> List[Category]:
        raise NotImplementedError("Method list must be implemented")

    @abstractmethod
    def update(self, category: Category) -> Optional[Category]:
        raise NotImplementedError("Method update must be implemented")

    @abstractmethod
    def delete(self, category_id: int) -> bool:
        raise NotImplementedError("Method delete must be implemented")
