
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
        Ghi sổ khi bán hàng:
        1. S1: Doanh thu
        2. S2: Xuất kho
        3. S6/S7: Thu tiền
        """
        ref_id = f"HD{order_id}"
        txn_date = datetime.now()
        
        # 1. Ghi S1 - Sổ doanh thu
        # Giả sử tất cả sản phẩm đều thuộc nhóm "Phân phối, cung cấp hàng hóa" (Thuế suất 1.5%)
        # Trong thực tế cần check category của từng item để phân nhóm
        s1_entry = LedgerEntryModel(
            transaction_date=txn_date,
            reference_id=ref_id,
            description=f"Doanh thu bán hàng đơn {ref_id}",
            ledger_type="S1",
            amount=total_amount,
            tax_group="Phân phối, cung cấp hàng hóa"
        )
        db.session.add(s1_entry)
        
        # 2. Ghi S2 - Sổ kho (Xuất kho)
        for item in items:
            product_id = item['product_id']
            qty = item['quantity']
            # Cần lấy giá vốn và tồn kho hiện tại (đã trừ trong ProductService, giờ ghi log)
            product = ProductModel.query.get(product_id)
            if product:
                # Tồn kho trong product đã được cập nhật TRƯỚC khi gọi hàm này (trong OrderService)
                # Nên balance_qty chính là product.stock hiện tại
                balance_qty = product.stock 
                
                s2_entry = InventoryLogModel(
                    transaction_date=txn_date,
                    reference_id=ref_id,
                    product_id=product_id,
                    description="Xuất bán hàng",
                    export_qty=qty,
                    export_price=product.cost_price, # Giá vốn
                    balance_qty=balance_qty,
                    balance_value=balance_qty * product.cost_price
                )
                db.session.add(s2_entry)

        # 3. Ghi S6 (Tiền mặt) hoặc S7 (Ngân hàng)
        if payment_method == "CASH":
            s6_entry = LedgerEntryModel(
                transaction_date=txn_date,
                reference_id=f"PT{order_id}", # Phiếu thu
                description=f"Thu tiền bán hàng đơn {ref_id}",
                ledger_type="S6",
                amount=total_amount,
                transaction_type="RECEIPT"
            )
            db.session.add(s6_entry)
        elif payment_method in ["TRANSFER", "BANK", "ZRJ_PAY"]: # Ví dụ
            s7_entry = LedgerEntryModel(
                transaction_date=txn_date,
                reference_id=f"GBC{order_id}", # Giấy báo có
                description=f"Nhận chuyển khoản đơn {ref_id}",
                ledger_type="S7",
                amount=total_amount,
                transaction_type="RECEIPT"
            )
            db.session.add(s7_entry)
            
        db.session.commit()

    def record_import(self, product_id: int, quantity: int, price: float, total_cost: float):
        """
        Ghi sổ khi nhập hàng:
        1. S2: Nhập kho
        2. S6/S7: Chi tiền (Giả sử trả ngay)
        """
        txn_date = datetime.now()
        ref_id = f"PN{int(txn_date.timestamp())}" # Mã phiếu nhập tạm

        # 1. Ghi S2 - Sổ kho
        product = ProductModel.query.get(product_id)
        balance_qty = product.stock if product else 0
        
        s2_entry = InventoryLogModel(
            transaction_date=txn_date,
            reference_id=ref_id,
            product_id=product_id,
            description="Nhập mua hàng",
            import_qty=quantity,
            import_price=price,
            balance_qty=balance_qty,
            balance_value=balance_qty * price # Ước tính
        )
        db.session.add(s2_entry)
        
        # 2. Ghi S6 - Chi tiền mặt (Mặc định chi tiền mặt nhập hàng)
        # Trong thực tế nên có tham số payment_method cho nhập hàng
        s6_entry = LedgerEntryModel(
            transaction_date=txn_date,
            reference_id=f"PC{ref_id}", # Phiếu chi
            description=f"Chi tiền nhập hàng {product.name if product else ''}",
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
