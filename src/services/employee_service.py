from typing import List, Dict
from injector import inject
import bcrypt
from src.domain.interfaces.user_repository import IUserRepository
from src.domain.models.user import User


class EmployeeService:
    """Service xử lý logic nghiệp vụ cho Employee"""
    
    @inject
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def create_employee(self, username: str, password: str, full_name: str) -> Dict:
        """
        Tạo tài khoản nhân viên mới (chỉ owner mới được gọi)
        Returns: {"success": bool, "message": str, "employee": dict}
        """
        # Kiểm tra username đã tồn tại chưa
        existing_user = self.user_repository.get_by_username(username)
        if existing_user:
            return {"success": False, "message": "Tên đăng nhập đã tồn tại"}
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Tạo employee mới với role 'employee'
        new_employee = User(
            username=username,
            password_hash=password_hash,
            role='employee',
            full_name=full_name,
            status='active'
        )
        
        saved_employee = self.user_repository.add(new_employee)
        
        return {
            "success": True,
            "message": "Tạo tài khoản nhân viên thành công",
            "employee": self._user_to_dict(saved_employee)
        }
    
    def get_all_employees(self) -> List[Dict]:
        """
        Lấy danh sách tất cả nhân viên
        Returns: List[dict]
        """
        employees = self.user_repository.get_all_employees()
        return [self._user_to_dict(emp) for emp in employees]
    
    def update_employee_status(self, employee_id: int, status: str) -> Dict:
        """
        Khóa/Mở khóa tài khoản nhân viên
        Returns: {"success": bool, "message": str}
        """
        # Kiểm tra employee có tồn tại không
        employee = self.user_repository.get_by_id(employee_id)
        if not employee:
            return {"success": False, "message": "Không tìm thấy nhân viên"}
        
        # Kiểm tra có phải employee không (không được khóa owner)
        if employee.role != 'employee':
            return {"success": False, "message": "Chỉ có thể khóa tài khoản nhân viên"}
        
        # Cập nhật status
        success = self.user_repository.update_status(employee_id, status)
        
        if success:
            status_text = "khóa" if status == 'inactive' else "mở khóa"
            return {"success": True, "message": f"Đã {status_text} tài khoản nhân viên"}
        else:
            return {"success": False, "message": "Cập nhật trạng thái thất bại"}
    
    def delete_employee(self, employee_id: int) -> Dict:
        """
        Xóa nhân viên
        Returns: {"success": bool, "message": str}
        """
        # Kiểm tra employee có tồn tại không
        employee = self.user_repository.get_by_id(employee_id)
        if not employee:
            return {"success": False, "message": "Không tìm thấy nhân viên"}
        
        # Kiểm tra có phải employee không (không được xóa owner)
        if employee.role != 'employee':
            return {"success": False, "message": "Chỉ có thể xóa tài khoản nhân viên"}
        
        # Xóa employee
        success = self.user_repository.delete(employee_id)
        
        if success:
            return {"success": True, "message": "Đã xóa nhân viên"}
        else:
            return {"success": False, "message": "Xóa nhân viên thất bại"}
    
    def _user_to_dict(self, user: User) -> Dict:
        """Convert User entity to dict"""
        return {
            'id': user.id,
            'username': user.username,
            'full_name': user.full_name,
            'role': user.role,
            'status': user.status
        }
