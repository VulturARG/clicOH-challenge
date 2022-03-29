import unittest
from datetime import datetime
from unittest.mock import Mock

from domain.orders.base import Order, Product, OrderDetail
from domain.orders.exceptions import (
    ProductNotUniqueError, NotEnoughStockError, ThereAreNoProductsError
)
from domain.orders.repository import OrderRepository
from domain.orders.service import OrderService


class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.products = {
            1: Product(
                id=1,
                name="Product 1",
                description="Product 1 description",
                price=10.0,
                stock=10
            ),
            2: Product(
                id=2,
                name="Product 2",
                description="Product 2 description",
                price=20.0,
                stock=20
            ),
            3: Product(
                id=3,
                name="Product 3",
                description="Product 3 description",
                price=10.0,
                stock=10
            )
        }

        self.order_details = [
            OrderDetail(
                id=None,
                order_id=1,
                product_id=1,
                quantity=1,
            ),
            OrderDetail(
                id=None,
                order_id=1,
                product_id=2,
                quantity=2,
            ),
        ]

        self.orders = [
            Order(
                id=1,
                date_time=datetime.now(),
            )
        ]

        self.new_products = [
            {
                "id": None,
                "order_id": 1,
                "product_id": 1,
                "quantity": 1,
            },
            {
                "id": None,
                "order_id": 1,
                "product_id": 2,
                "quantity": 2,
            },
        ]

        self.new_products_are_equal = [
            {
                "id": None,
                "order_id": 1,
                "product_id": 1,
                "quantity": 1,
            },
            {
                "id": None,
                "order_id": 1,
                "product_id": 1,
                "quantity": 2,
            },
        ]

        self.expected_order_without_products = [
            {
                "id": 1,
                "date_time": self.orders[0].date_time,
                "order_detail": []
            }
        ]

        self.expected_order_with_products = [
            {
                "id": 1,
                "date_time": self.orders[0].date_time,
                "order_detail": self.new_products
            }
        ]

        self.product_indexed = {
                "1": {
                    "id": 1,
                    "name": "Product 1",
                    "description": "Product 1 description",
                    "price": 10.0,
                    "stock": 9
                },
                "2": {
                    "id": 2,
                    "name": "Product 2",
                    "description": "Product 2 description",
                    "price": 20.0,
                    "stock": 18
                }
            }

    def test_get_order_list(self):

        mock_repository = Mock(spec=OrderRepository)
        service = OrderService(mock_repository)

        # values returned by the repository
        mock_repository.get_orders.return_value = self.orders
        mock_repository.get_orders_details.return_value = self.order_details

        actual = service.get_orders()
        self.assertEqual(self.expected_order_with_products, actual)

    def test_get_order_list_order_detail_empty(self):

        mock_repository = Mock(spec=OrderRepository)
        service = OrderService(mock_repository)

        # values returned by the repository
        mock_repository.get_orders.return_value = self.orders
        mock_repository.get_orders_details.return_value = []

        actual = service.get_orders()
        self.assertEqual(self.expected_order_without_products, actual)

    def test_are_products_unique(self):
        mock_repository = Mock(spec=OrderRepository)
        service = OrderService(mock_repository)

        # values returned by the repository
        mock_repository.get_orders.return_value = self.orders
        mock_repository.get_orders_details.return_value = self.order_details
        mock_repository.get_products.return_value = self.products

        actual = service.are_products_unique(self.new_products)
        self.assertTrue(actual)

    def test_are_products_not_unique(self):
        mock_repository = Mock(spec=OrderRepository)
        service = OrderService(mock_repository)

        # values returned by the repository
        mock_repository.get_orders.return_value = self.orders
        mock_repository.get_orders_details.return_value = self.order_details
        mock_repository.get_products.return_value = self.products

        actual = service.are_products_unique(self.new_products_are_equal)
        self.assertFalse(actual)

    def test_create_an_order_with_not_products(self):
        mock_repository = Mock(spec=OrderRepository)
        service = OrderService(mock_repository)

        # values returned by the repository
        mock_repository.get_orders.return_value = self.orders
        mock_repository.get_orders_details.return_value = self.order_details
        mock_repository.get_products.return_value = self.products

        actual = service.get_new_stock_of_the_products([])
        self.assertEqual({}, actual)

    def test_create_an_order_with_not_enough_stock(self):
        mock_repository = Mock(spec=OrderRepository)
        service = OrderService(mock_repository)

        # values returned by the repository
        mock_repository.get_products.return_value = self.products

        self.new_products[0]['quantity'] = 11

        with self.assertRaises(NotEnoughStockError):
            service.get_new_stock_of_the_products(self.new_products)

    def test_create_an_order_with_products_not_unique(self):
        mock_repository = Mock(spec=OrderRepository)
        service = OrderService(mock_repository)

        # values returned by the repository
        mock_repository.get_products.return_value = self.products

        with self.assertRaises(ProductNotUniqueError):
            service.get_new_stock_of_the_products(self.new_products_are_equal)

    def test_create_an_order_with_not_product(self):
        mock_repository = Mock(spec=OrderRepository)
        service = OrderService(mock_repository)

        # values returned by the repository
        mock_repository.get_products.return_value = {}

        with self.assertRaises(ThereAreNoProductsError):
            service.get_new_stock_of_the_products(self.new_products)

    def test_create_an_order(self):
        mock_repository = Mock(spec=OrderRepository)
        service = OrderService(mock_repository)

        # values returned by the repository
        mock_repository.get_orders.return_value = self.orders
        mock_repository.get_orders_details.return_value = self.order_details
        mock_repository.get_products.return_value = self.products

        actual = service.get_new_stock_of_the_products(self.new_products)
        self.assertEqual(self.product_indexed, actual)



