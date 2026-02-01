from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Customer:
    name: str
    phone: str
    address: str
    id: Optional[int] = None
    debt_amount: float = 0.0
    created_at: Optional[datetime] = None


@dataclass
class DebtTransaction:
    customer_id: int
    transaction_type: str  # 'debt' hoặc 'payment'
    amount: float
    note: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
