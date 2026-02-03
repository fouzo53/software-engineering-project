
from typing import Dict, List

class SubscriptionService:
    PLANS = {
        "free": {
            "name": "Free",
            "price": 0,
            "limits": {
                "products": 20,
                "employees": 1,
                "orders_per_month": 50
            },
            "features": [
                "POS Cơ bản (Tạo đơn, in hóa đơn)",
                "Báo cáo doanh thu ngày"
            ]
        },
        "basic": {
            "name": "Basic",
            "price": 100000,
            "limits": {
                "products": 200,
                "employees": 3,
                "orders_per_month": 500
            },
            "features": [
                "Quản lý kho hàng & Tồn kho",
                "Tự động ghi sổ (TT 88/2021/TT-BTC)",
                "Báo cáo tài chính chi tiết",
                "Hỗ trợ kỹ thuật tiêu chuẩn"
            ]
        },
        "pro": {
            "name": "Pro",
            "price": 300000,
            "limits": {
                "products": 5000,
                "employees": 10,
                "orders_per_month": 10000
            },
            "features": [
                "Trợ lý ảo AI (Tạo đơn bằng giọng nói)",
                "Phân tích tài chính chuyên sâu",
                "Quản lý đa nhân viên & Phân quyền",
                "Không giới hạn tính năng",
                "Hỗ trợ ưu tiên 24/7"
            ]
        }
    }

    def get_plans(self) -> Dict[str, Dict]:
        return self.PLANS

    def check_limit(self, user, limit_type: str, current_usage: int) -> bool:
        """
        Check if user has reached their subscription limit
        user: UserModel instance
        limit_type: 'products', 'employees', 'orders_per_month'
        current_usage: current count
        """
        # Default to 'free' if no subscription or invalid subscription
        plan_key = user.subscription if user.subscription in self.PLANS else "free"
        plan = self.PLANS.get(plan_key)
        
        limit = plan["limits"].get(limit_type, 0)
        
        return current_usage < limit

    def upgrade_subscription(self, user, plan_key: str):
        if plan_key not in self.PLANS:
            raise ValueError("Invalid plan")
        
        user.subscription = plan_key
        return True
