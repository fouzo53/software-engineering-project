from typing import List, Dict, Optional
from injector import inject
import json
from datetime import datetime, timedelta
from src.domain.interfaces.user_repository import IUserRepository
from src.infrastructure.models.order_model import OrderModel
from src.infrastructure.models.config_model import ConfigModel
from src.infrastructure.databases.database import db


class AdminService:
    """Service xử lý logic nghiệp vụ cho Admin"""
    
    @inject
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def get_all_owners(self) -> List[Dict]:
        """
        Lấy danh sách các hộ kinh doanh (owners)
        Returns: List[dict]
        """
        owners = self.user_repository.get_all_owners()
        
        return [
            {
                'id': owner.id,
                'username': owner.username,
                'full_name': owner.full_name,
                'status': owner.status,
                'subscription': owner.subscription
            }
            for owner in owners
        ]
    
    def update_owner_subscription(self, owner_id: int, subscription: str) -> Dict:
        """
        Cập nhật gói cước cho chủ hộ
        Returns: {"success": bool, "message": str}
        """
        # Kiểm tra owner có tồn tại không
        owner = self.user_repository.get_by_id(owner_id)
        if not owner:
            return {"success": False, "message": "Không tìm thấy chủ hộ"}
        
        # Kiểm tra có phải owner không
        if owner.role != 'owner':
            return {"success": False, "message": "Chỉ có thể cập nhật gói cước cho chủ hộ"}
        
        # Cập nhật subscription
        success = self.user_repository.update_subscription(owner_id, subscription)
        
        if success:
            return {
                "success": True,
                "message": f"Đã cập nhật gói cước thành {subscription.upper()}"
            }
        else:
            return {"success": False, "message": "Cập nhật gói cước thất bại"}
    
    def get_platform_stats(self) -> Dict:
        """
        Lấy thống kê toàn sàn
        Returns: dict với total_users, total_orders_this_month
        """
        # Tổng số users
        total_users = self.user_repository.count_all_users()
        
        # Tổng đơn hàng trong tháng
        now = datetime.utcnow()
        first_day_of_month = datetime(now.year, now.month, 1)
        
        total_orders_this_month = OrderModel.query.filter(
            OrderModel.created_at >= first_day_of_month
        ).count()
        
        return {
            'total_users': total_users,
            'total_orders_this_month': total_orders_this_month,
            'month': now.strftime('%Y-%m'),
            'stats_date': now.isoformat()
        }
    
    def update_report_config(self, config_data: Dict) -> Dict:
        """
        Cập nhật mẫu báo cáo tài chính (lưu config dạng JSON)
        Returns: {"success": bool, "message": str, "config": dict}
        """
        try:
            config_key = 'financial_report_template'
            config_json = json.dumps(config_data, ensure_ascii=False)
            
            # Kiểm tra config đã tồn tại chưa
            existing_config = ConfigModel.query.filter_by(config_key=config_key).first()
            
            if existing_config:
                # Cập nhật config cũ
                existing_config.config_value = config_json
                existing_config.updated_at = datetime.utcnow()
            else:
                # Tạo config mới
                new_config = ConfigModel(
                    config_key=config_key,
                    config_value=config_json,
                    description='Mẫu báo cáo tài chính'
                )
                db.session.add(new_config)
            
            db.session.commit()
            
            return {
                "success": True,
                "message": "Đã cập nhật mẫu báo cáo tài chính",
                "config": config_data
            }
        except Exception as e:
            db.session.rollback()
            return {
                "success": False,
                "message": f"Lỗi khi cập nhật config: {str(e)}"
            }
    
    def get_report_config(self) -> Optional[Dict]:
        """
        Lấy mẫu báo cáo tài chính hiện tại
        Returns: dict hoặc None
        """
        config = ConfigModel.query.filter_by(config_key='financial_report_template').first()
        
        if config:
            try:
                return json.loads(config.config_value)
            except:
                return None
        
        return None
