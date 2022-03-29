from __future__ import annotations

from typing import List, Optional, Dict

from rest_framework.serializers import ListSerializer
from rest_framework.utils.serializer_helpers import ReturnDict

from domain.orders.base import (
    Order as OrderDomain,
    OrderDetail as OrderDetailDomain,
    Product,
)

from domain.orders.repository import OrderRepository


class DRFOrderRepository(OrderRepository):

    def __init__(
        self,
        orders: ListSerializer | ReturnDict,
        order_details: Optional[ListSerializer | ReturnDict] = None,
        products: Optional[ListSerializer | ReturnDict] = None,
    ) -> None:

        self._orders = orders
        self._order_details = order_details
        self._products = products

    def get_orders(self) -> List[OrderDomain]:
        """Get all orders."""

        if isinstance(self._order_details, ReturnDict):
            return [self._get_orders(self._orders)]

        return [
            self._get_orders(order)
            for order in self._orders
        ]

    def get_orders_details(self) -> List[OrderDetailDomain]:
        """Get all order details."""

        if self._order_details is None:
            return []

        if isinstance(self._order_details, ReturnDict):
            return [self.get_order_detail_domain(self._order_details)]

        return [
            self.get_order_detail_domain(order_detail)
            for order_detail in self._order_details
        ]

    def get_products(self) -> Dict[str, Product]:
        """Get all products."""

        if self._products is None:
            return {}

        if isinstance(self._order_details, ReturnDict):
            return {dict(self._products)["id"]: self._get_product(self._products)}

        return {
            dict(product)["id"]: self._get_product(product)
            for product in self._products
        }

    def _get_orders(self, order: ReturnDict) -> OrderDomain:
        """Get order domain class."""

        return OrderDomain(
            id=dict(order)["id"],
            date_time=dict(order)["date_time"],
        )

    def get_order_detail_domain(self, order_detail: ReturnDict) -> OrderDetailDomain:
        """Get order detail domain class."""

        return OrderDetailDomain(
            id=dict(order_detail)["id"],
            order_id=dict(order_detail)["order"].id,
            product_id=dict(order_detail)["product"].id,
            quantity=dict(order_detail)["quantity"],
        )

    def _get_product(self, product: ReturnDict) -> Product:
        """Get product domain class."""

        return Product(
            id=dict(product)["id"],
            name=dict(product)["name"],
            description=dict(product)["description"],
            price=dict(product)["price"],
            stock=dict(product)["stock"],
        )
