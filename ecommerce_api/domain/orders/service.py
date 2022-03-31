from typing import List, Dict, Any, Optional

from domain.orders.base import OrderDetail, Order
from domain.orders.exceptions import (
    ProductNotUniqueError,
    NotEnoughStockError,
    QuantityEqualOrLessThanZeroError,
    ThereAreNoProductsError
)
from domain.orders.repository import OrderRepository


class OrderService:
    """Manage orders."""

    KEY = 'product_id'

    def __init__(self, repository: OrderRepository) -> None:
        """Initialize the OrderService."""

        self._repository = repository

    def get_orders(self) -> List[Dict]:
        """Return all orders."""
        orders = []
        for order in self._repository.get_orders():
            order_detail = self.get_order_details(order)
            orders.append(
                {
                    "id": order.id,
                    "date_time": order.date_time,
                    "order_detail": self._order_detail_to_dict(order_detail)
                }
            )
        return orders

    def get_order_details(self, order: Order) -> List[OrderDetail]:
        orders_details = self._repository.get_orders_details()
        return [
            detail for detail in orders_details
            if detail.order_id == order.id
        ]

    def get_new_stock_of_the_products(
            self,
            new_products: List[Dict[str, Any]],
            delete: Optional[bool] = False
    ) -> Dict[str, Any]:
        """Create a new order."""

        factor = -1 if delete else 1

        if not new_products:
            return {}

        if not self.are_products_unique(new_products):
            raise ProductNotUniqueError()

        products = self._repository.get_products()
        if len(products) == 0:
            raise ThereAreNoProductsError()

        updated_products = {}
        for product in new_products:
            product_id = product['product_id']
            product_class = products[product_id]

            old_stock = product_class.stock
            new_stock = old_stock - product['quantity'] * factor
            if new_stock < 0:
                raise NotEnoughStockError()

            if product['quantity'] <= 0:
                raise QuantityEqualOrLessThanZeroError()

            updated_products[str(product_id)] = {
                "id": product_id,
                "name": product_class.name,
                "description": product_class.description,
                "price": product_class.price,
                "stock": new_stock
            }

        return updated_products

    def are_products_unique(self, order_detail: List[Dict[str, Any]]) -> bool:
        """Check if the products are unique."""
        
        order_detail_key_values = [value[self.KEY] for value in order_detail]
        order_detail_key_values_unique = set(order_detail_key_values)
        return len(order_detail_key_values) == len(order_detail_key_values_unique)

    def _order_detail_to_dict(self, order_detail: List[OrderDetail]) -> List[Dict]:
        """Convert a list of OrderDetail to a dict."""
        return [dict(detail) for detail in order_detail]

