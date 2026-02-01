from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.customer import Customer, DebtTransaction


class ICustomerRepository(ABC):
    """Interface cho Customer Repository"""
    
    @abstractmethod
    def create(self, customer: Customer) -> Customer:
        """Thêm khách hàng mới"""
        pass
    
    @abstractmethod
    def find_all(self, search: Optional[str] = None) -> List[Customer]:
        """Lấy danh sách khách hàng, có thể tìm kiếm theo tên/SĐT"""
        pass
    
    @abstractmethod
    def find_by_id(self, customer_id: int) -> Optional[Customer]:
        """Tìm khách hàng theo ID"""
        pass
    
    @abstractmethod
    def update(self, customer: Customer) -> Customer:
        """Cập nhật thông tin khách hàng"""
        pass
    
    @abstractmethod
    def delete(self, customer_id: int) -> bool:
        """Xóa khách hàng"""
        pass
    
    @abstractmethod
    def add_debt_transaction(self, transaction: DebtTransaction) -> DebtTransaction:
        """Thêm giao dịch nợ/trả nợ"""
        pass
    
    @abstractmethod
    def get_debt_history(self, customer_id: int) -> List[DebtTransaction]:
        """Lấy lịch sử ghi nợ/trả nợ của khách hàng"""
        pass
    
    @abstractmethod
    def update_debt_amount(self, customer_id: int, amount: float) -> None:
        """Cập nhật tổng dư nợ của khách hàng"""
        pass
