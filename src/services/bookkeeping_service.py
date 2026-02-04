
from typing import List, Dict, Optional
from datetime import datetime
from src.infrastructure.databases.database import db
from src.infrastructure.models.accounting_model import LedgerEntryModel, InventoryLogModel
from src.infrastructure.models.product_model import ProductModel
from injector import inject

class BookkeepingService:
    @inject
    def __init__(self):
        pass

    def record_sale(self, order_id: int, total_amount: float, items: List[Dict], payment_method: str):
        """
        Ghi sổ khi bán hàng (Auto-Bookkeeping):
        1. S1-HKD: Doanh thu (Phân loại theo nhóm ngành nghề -> Category)
        2. S2-HKD: Xuất kho
        3. S6-HKD: Thu tiền mặt (Nếu Payment = CASH)
        4. S7-HKD: Tiền gửi ngân hàng (Nếu Payment = TRANSFER/BANK)
        """
        ref_id = f"HD{order_id}"
        txn_date = datetime.now()
        
        # --- 1. Ghi S1 - Sổ chi tiết doanh thu ---
        # Logic: Phân tách doanh thu theo nhóm thuế dựa trên Category của sản phẩm.
        # Ở đây tạm thời gom nhóm dựa trên giả định. Thực tế cần join với Category để lấy tax_group.
        
        # Group doanh thu theo danh mục (để tách dòng nếu cần, nhưng S1 thường ghi tổng daily hoặc per invoice)
        # Ở mức đơn giản: Ghi 1 dòng cho cả hóa đơn vào nhóm ngành nghề chính
        
        s1_entry = LedgerEntryModel(
            transaction_date=txn_date,
            reference_id=ref_id,
            description=f"Doanh thu bán hàng hóa", # Cần chi tiết?
            ledger_type="S1", 
            amount=total_amount,
            # Mặc định nhóm 1: Phân phối, cung cấp hàng hóa (Thuế 1.5%)
            # Cần logic phức tạp hơn nếu bán cả Dịch vụ (Thuế 7%) trong cùng 1 đơn
            tax_group="1. Phân phối, cung cấp hàng hóa" 
        )
        db.session.add(s1_entry)
        
        # --- 2. Ghi S2 - Sổ kho (Xuất kho) ---
        for item in items:
            product_id = item['product_id']
            qty = item['quantity']
            
            product = ProductModel.query.get(product_id)
            if product:
                # Tồn cuối = Tồn hiện tại (đã trừ trong OrderService)
                balance_qty = product.stock 
                
                s2_entry = InventoryLogModel(
                    transaction_date=txn_date,
                    reference_id=ref_id,
                    product_id=product_id,
                    description="Xuất bán",
                    
                    # Xuất
                    export_qty=qty,
                    # Thông tư 88 không bắt buộc ghi giá vốn xuất kho mỗi lần, 
                    # nhưng hệ thống cần để tính lãi/lỗ nội bộ.
                    export_price=product.cost_price, 
                    
                    # Tồn
                    balance_qty=balance_qty,
                    balance_value=balance_qty * product.cost_price
                )
                db.session.add(s2_entry)

        # --- 3 & 4. Ghi S6 (Tiền mặt) hoặc S7 (Ngân hàng) ---
        if payment_method == "CASH":
            s6_entry = LedgerEntryModel(
                transaction_date=txn_date,
                reference_id=f"PT-{ref_id}", # Phiếu thu
                description=f"Thu tiền bán hàng theo hóa đơn {ref_id}",
                ledger_type="S6",
                amount=total_amount,
                transaction_type="RECEIPT"
            )
            db.session.add(s6_entry)
            
        elif payment_method in ["TRANSFER", "BANK", "QR_CODE"]:
            s7_entry = LedgerEntryModel(
                transaction_date=txn_date,
                reference_id=f"GBC-{ref_id}", # Giấy báo có
                description=f"Thu chuyển khoản theo hóa đơn {ref_id}",
                ledger_type="S7",
                amount=total_amount,
                transaction_type="RECEIPT" # Báo Có (Tăng tiền gửi)
            )
            db.session.add(s7_entry)
        
        # DEBT (Công nợ) chưa ghi vào S6/S7 ngay, 
        # sẽ ghi khi nào khách trả nợ (Collect Debt) -> Cần feature riêng.
            
        db.session.commit()

    def record_import(self, product_id: int, quantity: int, price: float, total_cost: float):
        """
        Ghi sổ khi nhập hàng (Auto-Bookkeeping):
        1. S2-HKD: Nhập kho
        2. S6/S7: Chi tiền (nếu trả ngay)
        """
        txn_date = datetime.now()
        ref_id = f"PN{int(txn_date.timestamp())}" # Mã phiếu nhập

        # --- 1. Ghi S2 - Sổ kho (Nhập) ---
        product = ProductModel.query.get(product_id)
        balance_qty = product.stock if product else 0 # Tồn sau khi nhập (Service gốc đã + rồi)
        
        s2_entry = InventoryLogModel(
            transaction_date=txn_date,
            reference_id=ref_id,
            product_id=product_id,
            description="Nhập mua hàng hóa",
            
            # Nhập
            import_qty=quantity,
            import_price=price,
            
            # Tồn
            balance_qty=balance_qty,
            balance_value=balance_qty * (product.cost_price if product else price) 
        )
        db.session.add(s2_entry)
        
        # --- 2. Ghi S6/S7 - Chi tiền ---
        # Mặc định đơn giản hóa là chi Tiền mặt. 
        # Thực tế cần tham số `payment_method` cho hàm import này.
        s6_entry = LedgerEntryModel(
            transaction_date=txn_date,
            reference_id=f"PC-{ref_id}", # Phiếu chi
            description=f"Chi tiền mua hàng hóa ({product.name if product else ''})",
            ledger_type="S6",
            amount=total_cost,
            transaction_type="PAYMENT"
        )
        db.session.add(s6_entry)
        
        db.session.commit()

    def get_ledger(self, ledger_type: str, start_date: str, end_date: str):
        query = LedgerEntryModel.query.filter(
            LedgerEntryModel.ledger_type == ledger_type,
            LedgerEntryModel.transaction_date >= start_date,
            LedgerEntryModel.transaction_date <= end_date
        )
        return query.all()
