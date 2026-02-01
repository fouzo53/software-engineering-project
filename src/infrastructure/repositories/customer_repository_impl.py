from typing import List, Optional
from src.domain.interfaces.customer_repository import ICustomerRepository
from src.domain.models.customer import Customer, DebtTransaction
from src.infrastructure.models.customer_model import CustomerModel, DebtTransactionModel
from src.infrastructure.databases.database import db


class CustomerRepositoryImpl(ICustomerRepository):
    """Implementation của Customer Repository"""
    
    def create(self, customer: Customer) -> Customer:
        """Thêm khách hàng mới"""
        customer_model = CustomerModel(
            name=customer.name,
            phone=customer.phone,
            address=customer.address,
            debt_amount=customer.debt_amount
        )
        
        db.session.add(customer_model)
        db.session.commit()
        
        return self._model_to_entity(customer_model)
    
    def find_all(self, search: Optional[str] = None) -> List[Customer]:
        """Lấy danh sách khách hàng, có thể tìm kiếm theo tên/SĐT"""
        query = CustomerModel.query
        
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                (CustomerModel.name.like(search_pattern)) | 
                (CustomerModel.phone.like(search_pattern))
            )
        
        customers = query.all()
        return [self._model_to_entity(c) for c in customers]
    
    def find_by_id(self, customer_id: int) -> Optional[Customer]:
        """Tìm khách hàng theo ID"""
        customer_model = CustomerModel.query.get(customer_id)
        if not customer_model:
            return None
        return self._model_to_entity(customer_model)
    
    def update(self, customer: Customer) -> Customer:
        """Cập nhật thông tin khách hàng"""
        customer_model = CustomerModel.query.get(customer.id)
        if not customer_model:
            raise ValueError(f"Customer with id {customer.id} not found")
        
        customer_model.name = customer.name
        customer_model.phone = customer.phone
        customer_model.address = customer.address
        
        db.session.commit()
        return self._model_to_entity(customer_model)
    
    def delete(self, customer_id: int) -> bool:
        """Xóa khách hàng"""
        customer_model = CustomerModel.query.get(customer_id)
        if not customer_model:
            return False
        
        db.session.delete(customer_model)
        db.session.commit()
        return True
    
    def add_debt_transaction(self, transaction: DebtTransaction) -> DebtTransaction:
        """Thêm giao dịch nợ/trả nợ"""
        transaction_model = DebtTransactionModel(
            customer_id=transaction.customer_id,
            transaction_type=transaction.transaction_type,
            amount=transaction.amount,
            note=transaction.note
        )
        
        db.session.add(transaction_model)
        
        # Cập nhật tổng nợ của khách hàng
        customer = CustomerModel.query.get(transaction.customer_id)
        if customer:
            if transaction.transaction_type == 'debt':
                customer.debt_amount += transaction.amount
            elif transaction.transaction_type == 'payment':
                customer.debt_amount -= transaction.amount
        
        db.session.commit()
        
        return self._transaction_model_to_entity(transaction_model)
    
    def get_debt_history(self, customer_id: int) -> List[DebtTransaction]:
        """Lấy lịch sử ghi nợ/trả nợ của khách hàng"""
        transactions = DebtTransactionModel.query.filter_by(
            customer_id=customer_id
        ).order_by(DebtTransactionModel.created_at.desc()).all()
        
        return [self._transaction_model_to_entity(t) for t in transactions]
    
    def update_debt_amount(self, customer_id: int, amount: float) -> None:
        """Cập nhật tổng dư nợ của khách hàng"""
        customer = CustomerModel.query.get(customer_id)
        if customer:
            customer.debt_amount = amount
            db.session.commit()
    
    def _model_to_entity(self, model: CustomerModel) -> Customer:
        """Convert CustomerModel sang Customer entity"""
        return Customer(
            id=model.id,
            name=model.name,
            phone=model.phone,
            address=model.address,
            debt_amount=model.debt_amount,
            created_at=model.created_at
        )
    
    def _transaction_model_to_entity(self, model: DebtTransactionModel) -> DebtTransaction:
        """Convert DebtTransactionModel sang DebtTransaction entity"""
        return DebtTransaction(
            id=model.id,
            customer_id=model.customer_id,
            transaction_type=model.transaction_type,
            amount=model.amount,
            note=model.note,
            created_at=model.created_at
        )
