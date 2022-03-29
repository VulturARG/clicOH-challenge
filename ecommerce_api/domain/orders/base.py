from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True, eq=True)
class Product:
    id: int
    name: str
    description: str
    price: float
    stock: int


@dataclass(frozen=True, eq=True)
class OrderDetail:
    product_id: int
    quantity: int
    id: Optional[int] = None
    order_id: Optional[int] = None

    def __iter__(self):
        yield 'id', self.id
        yield 'order', self.order_id
        yield 'product', self.product_id
        yield 'quantity', self.quantity


@dataclass(frozen=True, eq=True)
class Order:
    id: int
    date_time: datetime
