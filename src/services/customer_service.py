from typing import List, Optional, Dict
from injector import inject
from src.domain.interfaces.customer_repository import ICustomerRepository
from src.domain.models.customer import Customer, DebtTransaction


class CustomerService:
    """Service xử lý logic nghiệp vụ cho Customer"""
    
    @inject
    def __init__(self, customer_repository: ICustomerRepository):
        self.customer_repository = customer_repository
    
    def create_customer(self, name: str, phone: str, address: str) -> Dict:
        """Thêm khách hàng mới"""
        # Kiểm tra số điện thoại đã tồn tại chưa
        existing = self.customer_repository.find_all(search=phone)
        if existing:
            for c in existing:
                if c.phone == phone:
                    raise ValueError("Số điện thoại đã tồn tại")
        
        customer = Customer(
            name=name,
            phone=phone,
            address=address
        )
        
        result = self.customer_repository.create(customer)
        return self._customer_to_dict(result)
    
    def get_all_customers(self, search: Optional[str] = None) -> List[Dict]:
        """Lấy danh sách khách hàng với tìm kiếm"""
        customers = self.customer_repository.find_all(search)
        return [self._customer_to_dict(c) for c in customers]
    
    def get_customer_by_id(self, customer_id: int) -> Dict:
        """Lấy chi tiết khách hàng theo ID"""
        customer = self.customer_repository.find_by_id(customer_id)
        if not customer:
            raise ValueError(f"Không tìm thấy khách hàng với ID {customer_id}")
        
        return self._customer_to_dict(customer)
    
    def update_customer(self, customer_id: int, name: str, phone: str, address: str) -> Dict:
        """Cập nhật thông tin khách hàng"""
        customer = self.customer_repository.find_by_id(customer_id)
        if not customer:
            raise ValueError(f"Không tìm thấy khách hàng với ID {customer_id}")
        
        # Kiểm tra số điện thoại mới có trùng với khách khác không
        if phone != customer.phone:
            existing = self.customer_repository.find_all(search=phone)
            for c in existing:
                if c.phone == phone and c.id != customer_id:
                    raise ValueError("Số điện thoại đã được sử dụng bởi khách hàng khác")
        
        customer.name = name
        customer.phone = phone
        customer.address = address
        
        result = self.customer_repository.update(customer)
        return self._customer_to_dict(result)
    
    def delete_customer(self, customer_id: int) -> bool:
        """Xóa khách hàng"""
        return self.customer_repository.delete(customer_id)
    
    def add_debt(self, customer_id: int, amount: float, note: Optional[str] = None) -> Dict:
        """Thêm khoản nợ cho khách hàng"""
        customer = self.customer_repository.find_by_id(customer_id)
        if not customer:
            raise ValueError(f"Không tìm thấy khách hàng với ID {customer_id}")
        
        if amount <= 0:
            raise ValueError("Số tiền phải lớn hơn 0")
        
        transaction = DebtTransaction(
            customer_id=customer_id,
            transaction_type='debt',
            amount=amount,
            note=note
        )
        
        result = self.customer_repository.add_debt_transaction(transaction)
        return self._transaction_to_dict(result)
    
    def add_payment(self, customer_id: int, amount: float, note: Optional[str] = None) -> Dict:
        """Thêm khoản trả nợ của khách hàng"""
        customer = self.customer_repository.find_by_id(customer_id)
        if not customer:
            raise ValueError(f"Không tìm thấy khách hàng với ID {customer_id}")
        
        if amount <= 0:
            raise ValueError("Số tiền phải lớn hơn 0")
        
        if amount > customer.debt_amount:
            raise ValueError("Số tiền trả không được lớn hơn tổng nợ hiện tại")
        
        transaction = DebtTransaction(
            customer_id=customer_id,
            transaction_type='payment',
            amount=amount,
            note=note
        )
        
        result = self.customer_repository.add_debt_transaction(transaction)
        return self._transaction_to_dict(result)
    
    def get_debt_history(self, customer_id: int) -> List[Dict]:
        """Lấy lịch sử ghi nợ/trả nợ"""
        customer = self.customer_repository.find_by_id(customer_id)
        if not customer:
            raise ValueError(f"Không tìm thấy khách hàng với ID {customer_id}")
        
        transactions = self.customer_repository.get_debt_history(customer_id)
        return [self._transaction_to_dict(t) for t in transactions]
    
    def _customer_to_dict(self, customer: Customer) -> Dict:
        """Convert Customer entity to dict"""
        return {
            'id': customer.id,
            'name': customer.name,
            'phone': customer.phone,
            'address': customer.address,
            'debt_amount': customer.debt_amount,
            'created_at': customer.created_at.isoformat() if customer.created_at else None
        }
    
    def _transaction_to_dict(self, transaction: DebtTransaction) -> Dict:
        """Convert DebtTransaction entity to dict"""
        return {
            'id': transaction.id,
            'customer_id': transaction.customer_id,
            'transaction_type': transaction.transaction_type,
            'amount': transaction.amount,
            'note': transaction.note,
            'created_at': transaction.created_at.isoformat() if transaction.created_at else None
        }
