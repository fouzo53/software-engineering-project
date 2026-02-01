from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    id: Optional[int]
    name: str
    price: float
    stock: int
    category_id: int
    cost_price: float = 0.0
    image_url: Optional[str] = None
