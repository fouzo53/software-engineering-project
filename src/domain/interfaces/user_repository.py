from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.models.user import User


class IUserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError("Method get_by_username must be implemented")

    @abstractmethod
    def add(self, user: User) -> User:
        raise NotImplementedError("Method add must be implemented")
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError("Method get_by_id must be implemented")
    
    @abstractmethod
    def get_all_employees(self) -> List[User]:
        raise NotImplementedError("Method get_all_employees must be implemented")
    
    @abstractmethod
    def update_status(self, user_id: int, status: str) -> bool:
        raise NotImplementedError("Method update_status must be implemented")
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        raise NotImplementedError("Method delete must be implemented")
    
    @abstractmethod
    def get_all_owners(self) -> List[User]:
        raise NotImplementedError("Method get_all_owners must be implemented")
    
    @abstractmethod
    def update_subscription(self, user_id: int, subscription: str) -> bool:
        raise NotImplementedError("Method update_subscription must be implemented")
    
    @abstractmethod
    def count_all_users(self) -> int:
        raise NotImplementedError("Method count_all_users must be implemented")
    
    @abstractmethod
    def get_all(self) -> List[User]:
        raise NotImplementedError("Method get_all must be implemented")
