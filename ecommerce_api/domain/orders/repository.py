from abc import ABC, abstractmethod
from typing import List, Dict, Optional

from domain.orders.dataclass import Order, OrderDetail, Product


class OrderRepository(ABC):

    @abstractmethod
    def get_orders(self, pk: Optional[int] = None) -> List[Order]:
        """Get the orders."""

    @abstractmethod
    def get_orders_details(self) -> List[OrderDetail]:
        """list the orders details."""

    @abstractmethod
    def get_products(self) -> Dict[str, Product]:
        """list the orders details."""


