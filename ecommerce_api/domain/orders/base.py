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
    order_id: int
    product_id: int
    quantity: int
    id: Optional[int] = None

    def __iter__(self):
        yield 'id', self.id
        yield 'order_id', self.order_id
        yield 'product_id', self.product_id
        yield 'quantity', self.quantity


@dataclass(frozen=True, eq=True)
class Order:
    id: int
    date_time: datetime
