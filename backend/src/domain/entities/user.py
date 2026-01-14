# file: backend/src/domain/entities/user.py

from dataclasses import dataclass
from enum import Enum

# 1. Định nghĩa Enum Role (Theo yêu cầu nhiệm vụ [BE-03] & Đề bài BizFlow)
class UserRole(Enum):
    EMPLOYEE = "employee"
    OWNER = "owner"
    ADMIN = "admin"

# 2. Định nghĩa Class User (Map đúng theo bảng Database bạn gửi)
@dataclass
class User:
    # Id: bigint -> Dùng int
    id: int
    
    # Username: varchar -> Dùng str
    username: str
    
    # Password_hash: varchar -> Dùng str
    password_hash: str
    
    # Full_name: varchar -> Dùng str
    full_name: str
    
    # Is_active: tinyint (1:active, 0:inactive) -> Dùng bool (True/False)
    is_active: bool
    
    # Role: (Không có trong bảng DB bạn gửi, nhưng Nhiệm vụ bắt buộc phải có)
    role: UserRole

    # --- Các hàm logic bổ trợ (Helper methods) ---
    
    def is_admin(self) -> bool:
        """Kiểm tra có phải Admin không"""
        return self.role == UserRole.ADMIN

    def is_owner(self) -> bool:
        """Kiểm tra có phải Owner không"""
        return self.role == UserRole.OWNER

    def is_employee(self) -> bool:
        """Kiểm tra có phải Employee không"""
        return self.role == UserRole.EMPLOYEE

    def is_deactivated(self) -> bool:
        """Kiểm tra xem tài khoản có bị khóa không"""
        return not self.is_active