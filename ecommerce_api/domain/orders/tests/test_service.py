import unittest
from datetime import datetime
from unittest.mock import Mock

from domain.orders.base import Order, Product, OrderDetail
from domain.orders.exceptions import (
    ProductNotUniqueError,
    NotEnoughStockError,
    ThereAreNoProductsError,
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

        self.order_details_plus = [
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
            OrderDetail(
                id=None,
                order_id=2,
                product_id=2,
                quantity=2,
            )
        ]

        self.order_details_create = [
            OrderDetail(
                id=None,
                order_id=None,
                product_id=1,
                quantity=1,
            ),
            OrderDetail(
                id=None,
                order_id=None,
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
                "order_id": None,
                "product_id": 1,
                "quantity": 1,
            },
            {
                "id": None,
                "order_id": None,
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

        self.product_deleted = {
            "1": {
                "id": 1,
                "name": "Product 1",
                "description": "Product 1 description",
                "price": 10.0,
                "stock": 11
            },
            "2": {
                "id": 2,
                "name": "Product 2",
                "description": "Product 2 description",
                "price": 20.0,
                "stock": 22
            }
        }

        self.mock_repository = Mock(spec=OrderRepository)
        self.service = OrderService(self.mock_repository)

    def test_get_order_details(self):
        # values returned by the repository
        self.mock_repository.get_orders_details.return_value = self.order_details_plus

        actual = self.service.get_order_details(self.orders[0])
        self.assertEqual(self.order_details, actual)

    def test_get_order_list(self):

        self.mock_repository = Mock(spec=OrderRepository)
        self.service = OrderService(self.mock_repository)

        # values returned by the repository
        self.mock_repository.get_orders.return_value = self.orders
        self.mock_repository.get_orders_details.return_value = self.order_details

        actual = self.service.get_orders()
        self.assertEqual(self.expected_order_with_products, actual)

    def test_get_order_list_order_detail_empty(self):

        # values returned by the repository
        self.mock_repository.get_orders.return_value = self.orders
        self.mock_repository.get_orders_details.return_value = []

        actual = self.service.get_orders()
        self.assertEqual(self.expected_order_without_products, actual)

    def test_are_products_unique(self):
        # values returned by the repository
        self.mock_repository.get_orders.return_value = self.orders
        self.mock_repository.get_orders_details.return_value = self.order_details
        self.mock_repository.get_products.return_value = self.products

        actual = self.service.are_products_unique(self.new_products)
        self.assertTrue(actual)

    def test_are_products_not_unique(self):
        # values returned by the repository
        self.mock_repository.get_orders.return_value = self.orders
        self.mock_repository.get_orders_details.return_value = self.order_details
        self.mock_repository.get_products.return_value = self.products

        actual = self.service.are_products_unique(self.new_products_are_equal)
        self.assertFalse(actual)

    def test_get_new_stock_of_the_products_with_not_products(self):
        # values returned by the repository
        self.mock_repository.get_orders.return_value = self.orders
        self.mock_repository.get_orders_details.return_value = self.order_details
        self.mock_repository.get_products.return_value = self.products

        actual = self.service.get_new_stock_of_the_products([])
        self.assertEqual({}, actual)

    def test_get_new_stock_of_the_products_with_not_enough_stock(self):
        # values returned by the repository
        self.mock_repository.get_products.return_value = self.products

        self.new_products[0]['quantity'] = 11

        with self.assertRaises(NotEnoughStockError):
            self.service.get_new_stock_of_the_products(self.new_products)

    def test_get_new_stock_of_the_products_with_products_not_unique(self):
        # values returned by the repository
        self.mock_repository.get_products.return_value = self.products

        with self.assertRaises(ProductNotUniqueError):
            self.service.get_new_stock_of_the_products(self.new_products_are_equal)

    def test_get_new_stock_of_the_products_with_not_product(self):
        # values returned by the repository
        self.mock_repository.get_products.return_value = {}

        with self.assertRaises(ThereAreNoProductsError):
            self.service.get_new_stock_of_the_products(self.new_products)

    def test_get_new_stock_of_the_products_one_order_detail(self):
        # values returned by the repository
        self.mock_repository.get_orders.return_value = self.orders
        self.mock_repository.get_orders_details.return_value = self.order_details_create
        self.mock_repository.get_products.return_value = self.products

        actual = self.service.get_new_stock_of_the_products([self.new_products[0]])
        self.assertEqual(self.product_indexed["1"], actual["1"])

    def test_get_new_stock_of_the_products_two_order_detail(self):
        # values returned by the repository
        self.mock_repository.get_orders.return_value = self.orders
        self.mock_repository.get_orders_details.return_value = self.order_details_create
        self.mock_repository.get_products.return_value = self.products

        actual = self.service.get_new_stock_of_the_products(self.new_products)
        self.assertEqual(self.product_indexed, actual)

    def test_get_new_stock_of_the_products_delete_true(self):
        # values returned by the repository
        self.mock_repository.get_orders.return_value = self.orders
        self.mock_repository.get_orders_details.return_value = self.order_details_create
        self.mock_repository.get_products.return_value = self.products

        actual = self.service.get_new_stock_of_the_products(self.new_products, True)
        self.assertEqual(self.product_deleted, actual)

    def test_get_total(self):

        # values returned by the repository
        self.mock_repository.get_orders.return_value = self.orders
        self.mock_repository.get_orders_details.return_value = self.order_details
        self.mock_repository.get_products.return_value = self.products

        actual = self.service.get_total(1)
        self.assertEqual(50.0, actual)
