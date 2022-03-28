from typing import List, Dict, Any

from domain.orders.base import OrderDetail
from domain.orders.exceptions import ProductNotUniqueError, NotEnoughStockError, \
    QuantityEqualOrLessThanZeroError
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
        orders_details = self._repository.get_orders_details()
        for order in self._repository.get_orders():
            order_detail = [
                detail for detail in orders_details
                if detail.order_id == order.id
            ]
            orders.append(
                {
                    "id": order.id,
                    "date_time": order.date_time,
                    "order_detail": self._order_detail_to_dict(order_detail)
                }
            )

        return orders

    def add_products_to_order(
            self,
            new_products: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create a new order_id."""

        if not new_products:
            return {}

        if not self.are_products_unique(new_products):
            raise ProductNotUniqueError()

        products = self._repository.get_products()

        updated_products = {}
        for product in new_products:
            product_id = product['product_id']
            product_class = list(products[product_id - 1].values())[0]

            old_stock = product_class.stock
            new_stock = old_stock - product['quantity']
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

