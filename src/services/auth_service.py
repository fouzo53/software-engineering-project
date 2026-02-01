import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
from injector import inject
from src.domain.models.user import User
from src.domain.interfaces.user_repository import IUserRepository


class AuthService:
    """Service xử lý logic authentication"""
    
    @inject
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
        self.secret_key = "your-secret-key-change-in-production"
    
    def register(self, username: str, password: str, full_name: str, role: str = "user") -> Dict:
        """
        Đăng ký user mới
        Returns: {"success": bool, "message": str, "user": User}
        """
        # Kiểm tra username đã tồn tại
        existing_user = self.user_repository.get_by_username(username)
        if existing_user:
            return {"success": False, "message": "Username already exists"}
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Tạo user mới
        new_user = User(
            username=username,
            password_hash=password_hash,
            role=role,
            full_name=full_name
        )
        
        saved_user = self.user_repository.add(new_user)
        
        return {
            "success": True,
            "message": "User registered successfully",
            "user": saved_user
        }
    
    def login(self, username: str, password: str) -> Dict:
        """
        Đăng nhập và trả về JWT token
        Returns: {"success": bool, "message": str, "token": str, "user": User}
        """
        # Tìm user
        user = self.user_repository.get_by_username(username)
        if not user:
            return {"success": False, "message": "Invalid username or password"}
        
        # Check if account is active
        if getattr(user, 'status', 'active') == 'inactive':
            return {"success": False, "message": "Tài khoản đã bị vô hiệu hóa. Vui lòng liên hệ Admin!"}
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return {"success": False, "message": "Invalid username or password"}
        
        # Tạo JWT token
        payload = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
            "exp": datetime.utcnow() + timedelta(hours=2)
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        
        return {
            "success": True,
            "message": "Login successful",
            "token": token,
            "user": user
        }
    
    def get_all_users(self):
        """
        Lấy danh sách tất cả users
        Returns: List of user dictionaries
        """
        users = self.user_repository.get_all()
        return [
            {
                "id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "role": user.role,
                "status": getattr(user, 'status', 'active')
            }
            for user in users
        ]
    
    def toggle_user_status(self, user_id: int) -> Dict:
        """
        Kích hoạt/Vô hiệu hóa tài khoản
        Returns: {"success": bool, "message": str, "new_status": str}
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return {"success": False, "message": "Không tìm thấy tài khoản"}
        
        # Toggle status
        current_status = getattr(user, 'status', 'active')
        new_status = 'inactive' if current_status == 'active' else 'active'
        
        # Update user status
        updated_user = self.user_repository.update_status(user_id, new_status)
        
        return {
            "success": True,
            "message": f"Đã {'vô hiệu hóa' if new_status == 'inactive' else 'kích hoạt'} tài khoản",
            "new_status": new_status,
            "user": {
                "id": updated_user.id,
                "username": updated_user.username,
                "status": new_status
            }
        }
