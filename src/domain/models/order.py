from dataclasses import dataclass
from typing import Optional, List


@dataclass
class OrderDetail:
    product_id: int
    quantity: int
    price: float


@dataclass
class Order:
    id: Optional[int]
    user_id: int
    total_amount: float
    customer_id: Optional[int] = None
    payment_method: str = 'CASH'
    details: Optional[List[OrderDetail]] = None
