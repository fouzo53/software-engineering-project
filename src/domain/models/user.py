from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    username: str
    password_hash: str
    role: str
    full_name: str
    id: Optional[int] = None
    status: str = 'active'
    subscription: str = 'basic'
