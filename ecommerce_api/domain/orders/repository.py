from abc import ABC, abstractmethod
from typing import List, Dict

from domain.orders.base import Order, OrderDetail, Product


class OrderRepository(ABC):

    @abstractmethod
    def get_orders(self) -> List[Order]:
        """Get the orders."""

    @abstractmethod
    def get_orders_details(self) -> List[OrderDetail]:
        """list the orders details."""

    @abstractmethod
    def get_products(self) -> Dict[str, Product]:
        """list the orders details."""


