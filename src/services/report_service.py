from typing import List, Dict
from datetime import datetime
from sqlalchemy import text
from src.infrastructure.databases.database import db


class ReportService:
    """Service xử lý logic báo cáo"""
    
    def get_daily_revenue(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Lấy báo cáo doanh thu theo ngày bằng raw SQL
        start_date, end_date: format 'YYYY-MM-DD'
        Returns: [{"date": "YYYY-MM-DD", "revenue": float, "order_count": int}, ...]
        """
        query = text("""
            SELECT 
                DATE(created_at) as date,
                SUM(total_amount) as revenue,
                COUNT(*) as order_count
            FROM orders
            WHERE DATE(created_at) BETWEEN :start_date AND :end_date
            GROUP BY DATE(created_at)
            ORDER BY date ASC
        """)
        
        result = db.session.execute(
            query,
            {"start_date": start_date, "end_date": end_date}
        )
        
        return [
            {
                "date": row.date.strftime("%Y-%m-%d"),
                "revenue": float(row.revenue),
                "order_count": row.order_count
            }
            for row in result
        ]
