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

    def export_tax_report(self, start_date: str, end_date: str) -> Dict:
        """
        Xuất báo cáo thuế (giả lập đơn giản cho hộ kinh doanh)
        """
        # 1. Thống kê tổng quan
        summary_query = text("""
            SELECT 
                COUNT(id) as total_orders,
                SUM(total_amount) as total_revenue
            FROM orders
            WHERE DATE(created_at) BETWEEN :start_date AND :end_date
        """)
        
        summary = db.session.execute(
            summary_query, 
            {"start_date": start_date, "end_date": end_date}
        ).fetchone()

        total_orders = summary.total_orders or 0
        total_revenue = float(summary.total_revenue or 0)
        
        # Giả sử thuế khoán hoặc VAT 1.5% cho hộ kinh doanh thương mại (ví dụ thực tế VN)
        # Hoặc 10% VAT thông thường. Ở đây để config cứng là 10% cho demo.
        tax_rate = 0.10 
        total_tax = total_revenue * tax_rate

        # 2. Chi tiết theo ngày
        daily_query = text("""
            SELECT 
                DATE(created_at) as date,
                COUNT(id) as daily_orders,
                SUM(total_amount) as daily_revenue
            FROM orders
            WHERE DATE(created_at) BETWEEN :start_date AND :end_date
            GROUP BY DATE(created_at)
            ORDER BY date ASC
        """)
        
        daily_result = db.session.execute(
            daily_query,
            {"start_date": start_date, "end_date": end_date}
        )
        
        details = []
        for row in daily_result:
            revenue = float(row.daily_revenue)
            details.append({
                "date": row.date.strftime("%Y-%m-%d"),
                "orders": row.daily_orders,
                "revenue": revenue,
                "tax_amount": revenue * tax_rate
            })

        return {
            "period": {
                "start": start_date,
                "end": end_date
            },
            "summary": {
                "total_orders": total_orders,
                "total_revenue": total_revenue,
                "tax_rate": tax_rate,
                "total_tax_amount": total_tax
            },
            "details": details,
            "generated_at": datetime.now().isoformat()
        }

    def get_revenue_ledger(self, start_date: str, end_date: str) -> Dict:
        """
        Sổ chi tiết doanh thu bán hàng hóa, dịch vụ (Mẫu số S1-HKD)
        Tổng hợp từ bảng ledger_entries (S1)
        """
        # Sử dụng SQL để join lấy thông tin khách hàng từ reference_id (Format HD{id})
        # Sử dụng SQL để join lấy thông tin khách hàng từ reference_id (Format HD{id})
        # MySQL/PostgreSQL compatible: CONCAT('HD', o.id)
        # Note: We detected that the user is using PyMySQL, so we must use MySQL syntax.
        # SQLite uses ||, but MySQL uses CONCAT (unless PIPES_AS_CONCAT is on).
        query = text("""
            SELECT 
                l.transaction_date,
                l.reference_id as voucher_no,
                l.amount as revenue,
                l.description,
                c.name as customer_name,
                c.address as customer_address
            FROM ledger_entries l
            LEFT JOIN orders o ON l.reference_id = CONCAT('HD', o.id)
            LEFT JOIN customers c ON o.customer_id = c.id
            WHERE l.ledger_type = 'S1'
            AND DATE(l.transaction_date) BETWEEN :start_date AND :end_date
            ORDER BY l.transaction_date ASC
        """)
        
        result = db.session.execute(
            query,
            {"start_date": start_date, "end_date": end_date}
        )
        
        rows = []
        total_revenue = 0.0
        
        for row in result:
            revenue = float(row.revenue)
            total_revenue += revenue
            
            # Format date
            date_str = row.transaction_date.strftime("%d/%m/%Y") if row.transaction_date else ""
            
            rows.append({
                "date": date_str,
                "voucher_no": row.voucher_no,
                "voucher_date": date_str,
                "customer_name": row.customer_name or "Khách lẻ",
                "customer_address": row.customer_address or "",
                "product_revenue": revenue,
                "service_revenue": 0.0,
                "total_revenue": revenue,
                "description": row.description
            })
            
        return {
            "template": "S1-HKD",
            "name": "Sổ chi tiết doanh thu bán hàng hóa, dịch vụ",
            "period": {"start": start_date, "end": end_date},
            "rows": rows,
            "total_revenue": total_revenue,
            "generated_at": datetime.now().isoformat()
        }

    def get_cash_book(self, start_date: str, end_date: str) -> Dict:
        """
        Sổ quỹ tiền mặt (Mẫu số S4-HKD/S6)
        Tổng hợp từ bảng ledger_entries (S6)
        """
        query = text("""
            SELECT 
                transaction_date,
                reference_id as voucher_no,
                description,
                amount,
                transaction_type
            FROM ledger_entries
            WHERE ledger_type = 'S6'
            AND DATE(transaction_date) BETWEEN :start_date AND :end_date
            ORDER BY transaction_date ASC
        """)
        
        result = db.session.execute(
            query, 
            {"start_date": start_date, "end_date": end_date}
        ).fetchall()
        
        # Calculate opening balance (Giả lập hoặc lấy từ truy vấn trước đó)
        # Thực tế cần query tổng thu - chi trước start_date
        opening_query = text("""
            SELECT 
                SUM(CASE WHEN transaction_type = 'RECEIPT' THEN amount ELSE 0 END) -
                SUM(CASE WHEN transaction_type = 'PAYMENT' THEN amount ELSE 0 END) as balance
            FROM ledger_entries
            WHERE ledger_type = 'S6'
            AND DATE(transaction_date) < :start_date
        """)
        opening_res = db.session.execute(opening_query, {"start_date": start_date}).fetchone()
        opening_balance = float(opening_res.balance or 0) if opening_res else 0.0
        
        current_balance = opening_balance
        formatted_rows = []
        total_receipt = 0.0
        total_payment = 0.0
        
        for row in result:
            amount = float(row.amount)
            is_receipt = row.transaction_type == 'RECEIPT'
            
            receipt_amt = amount if is_receipt else 0.0
            payment_amt = amount if not is_receipt else 0.0
            
            current_balance += (receipt_amt - payment_amt)
            total_receipt += receipt_amt
            total_payment += payment_amt
            
            formatted_rows.append({
                "date": row.transaction_date.strftime("%d/%m/%Y") if row.transaction_date else "",
                "voucher_no": row.voucher_no,
                "description": row.description,
                "receipt_amount": receipt_amt,
                "payment_amount": payment_amt,
                "balance": current_balance
            })
            
        return {
            "template": "S4-HKD",
            "name": "Sổ quỹ tiền mặt",
            "period": {"start": start_date, "end": end_date},
            "opening_balance": opening_balance,
            "closing_balance": current_balance,
            "total_receipt": total_receipt,
            "total_payment": total_payment,
            "rows": formatted_rows,
            "generated_at": datetime.now().isoformat()
        }
