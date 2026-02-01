from typing import Optional, List
from src.domain.interfaces.user_repository import IUserRepository
from src.domain.models.user import User
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.databases.database import db


class UserRepositoryImpl(IUserRepository):
    """Concrete implementation của User Repository"""
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Lấy user theo username"""
        user_model = UserModel.query.filter_by(username=username).first()
        if not user_model:
            return None
        
        return User(
            id=user_model.id,
            username=user_model.username,
            password_hash=user_model.password_hash,
            role=user_model.role,
            full_name=user_model.full_name,
            status=user_model.status,
            subscription=user_model.subscription
        )
    
    def add(self, user: User) -> User:
        """Thêm user mới"""
        user_model = UserModel(
            username=user.username,
            password_hash=user.password_hash,
            role=user.role,
            full_name=user.full_name,
            status=user.status,
            subscription=user.subscription
        )
        db.session.add(user_model)
        db.session.commit()
        
        user.id = user_model.id
        return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Lấy user theo ID"""
        user_model = UserModel.query.get(user_id)
        if not user_model:
            return None
        
        return User(
            id=user_model.id,
            username=user_model.username,
            password_hash=user_model.password_hash,
            role=user_model.role,
            full_name=user_model.full_name,
            status=user_model.status,
            subscription=user_model.subscription
        )
    
    def get_all_employees(self) -> List[User]:
        """Lấy danh sách tất cả nhân viên (role=employee)"""
        user_models = UserModel.query.filter_by(role='employee').all()
        
        return [
            User(
                id=u.id,
                username=u.username,
                password_hash=u.password_hash,
                role=u.role,
                full_name=u.full_name,
                status=u.status,
                subscription=u.subscription
            )
            for u in user_models
        ]
    
    def update_status(self, user_id: int, status: str) -> Optional[User]:
        """Cập nhật trạng thái user (active/inactive)"""
        user_model = UserModel.query.get(user_id)
        if not user_model:
            return None
        
        user_model.status = status
        db.session.commit()
        
        return User(
            id=user_model.id,
            username=user_model.username,
            password_hash=user_model.password_hash,
            role=user_model.role,
            full_name=user_model.full_name,
            status=user_model.status,
            subscription=user_model.subscription
        )
    
    def delete(self, user_id: int) -> bool:
        """Xóa user"""
        user_model = UserModel.query.get(user_id)
        if not user_model:
            return False
        
        db.session.delete(user_model)
        db.session.commit()
        return True
    
    def get_all_owners(self) -> List[User]:
        """Lấy danh sách tất cả chủ hộ (role=owner)"""
        user_models = UserModel.query.filter_by(role='owner').all()
        
        return [
            User(
                id=u.id,
                username=u.username,
                password_hash=u.password_hash,
                role=u.role,
                full_name=u.full_name,
                status=u.status,
                subscription=u.subscription
            )
            for u in user_models
        ]
    
    def update_subscription(self, user_id: int, subscription: str) -> bool:
        """Cập nhật gói cước cho owner"""
        user_model = UserModel.query.get(user_id)
        if not user_model:
            return False
        
        user_model.subscription = subscription
        db.session.commit()
        return True
    
    def count_all_users(self) -> int:
        """Đếm tổng số users trong hệ thống"""
        return UserModel.query.count()
    
    def get_all(self) -> List[User]:
        """Lấy danh sách tất cả users"""
        user_models = UserModel.query.all()
        
        return [
            User(
                id=u.id,
                username=u.username,
                password_hash=u.password_hash,
                role=u.role,
                full_name=u.full_name,
                status=u.status,
                subscription=u.subscription
            )
            for u in user_models
        ]
