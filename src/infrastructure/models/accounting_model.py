
from src.infrastructure.databases.database import db
from datetime import datetime

class LedgerEntryModel(db.Model):
    """Mô hình cho sổ cái S1, S6, S7 (Doanh thu, Thu/Chi)"""
    __tablename__ = 'ledger_entries'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_date = db.Column(db.DateTime, default=datetime.now)
    reference_id = db.Column(db.String(50)) # Số hiệu chứng từ (VD: HD001, PN001)
    description = db.Column(db.String(255))
    
    # Phân loại sổ
    ledger_type = db.Column(db.String(20)) # 'S1' (Doanh thu), 'S6' (Tiền mặt), 'S7' (Ngân hàng)
    
    # Chi tiết tiền
    amount = db.Column(db.Float, default=0.0)
    
    # Phân loại thu/chi (cho S6, S7)
    transaction_type = db.Column(db.String(10)) # 'RECEIPT' (Thu), 'PAYMENT' (Chi)
    
    # Phân loại thuế (cho S1)
    tax_group = db.Column(db.String(50), nullable=True) # VD: 'Phân phối, cung cấp hàng hóa'
    
    created_at = db.Column(db.DateTime, default=datetime.now)

class InventoryLogModel(db.Model):
    """Mô hình cho sổ S2 (Chi tiết vật liệu, dụng cụ, sản phẩm, hàng hóa)"""
    __tablename__ = 'inventory_logs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_date = db.Column(db.DateTime, default=datetime.now)
    reference_id = db.Column(db.String(50)) # Số hiệu chứng từ
    
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    description = db.Column(db.String(255)) # Diễn giải (Nhập kho, Xuất bán...)
    
    # Nhập
    import_qty = db.Column(db.Integer, default=0)
    import_price = db.Column(db.Float, default=0.0)
    
    # Xuất
    export_qty = db.Column(db.Integer, default=0)
    export_price = db.Column(db.Float, default=0.0)
    
    # Tồn tại thời điểm ghi
    balance_qty = db.Column(db.Integer, default=0)
    balance_value = db.Column(db.Float, default=0.0)
    
    product = db.relationship('ProductModel')
