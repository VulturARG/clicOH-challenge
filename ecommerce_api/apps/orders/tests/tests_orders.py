from rest_framework import status
from rest_framework.test import APITestCase

from apps.orders.models import Order, OrderDetail
from apps.products.models import Product


class OrderTestCase(APITestCase):
    list_url = "/v1/orders/"
    detail_url = "/v1/orders/1/"
    bad_detail_url = "/v1/orders/0/"

    def setUp(self):
        product_1 = Product(
            **{
                "name": 'Product 1',
                "description": 'Product 1 description',
                "price": '100.00',
                "stock": '10',
            }
        )
        product_1.save()

        product_2 = Product(
            **{
                "name": 'Product 2',
                "description": 'Product 2 description',
                "price": '200.00',
                "stock": '20',
            }
        )
        product_2.save()

        order_1 = Order(
            **{
                "id": 1,
                "date_time": "2020-01-01T00:00:00Z",
            }
        )
        order_1.save()

        order_2 = Order(
            **{
                "id": 2,
                "date_time": "2022-01-01T00:00:00Z",
            }
        )
        order_2.save()

        order_detail_1 = OrderDetail(
            **{
                "id": 1,
                "product": product_1,
                "quantity": 1,
                "order": order_1,
            }
        )
        order_detail_1.save()

        order_detail_2 = OrderDetail(
            **{
                "id": 2,
                "product": product_2,
                "quantity": 2,
                "order": order_1,
            }
        )
        order_detail_2.save()

        order_detail_3 = OrderDetail(
            **{
                "id": 3,
                "product": product_1,
                "quantity": 3,
                "order": order_2,
            }
        )
        order_detail_3.save()

    def test_list_orders(self):
        response = self.client.get(path=self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(len(response.data[0]['order_detail']), 2)
        self.assertEqual(len(response.data[1]['order_detail']), 1)
        self.assertEqual(response.data[0]['order_detail'][0]['product_id'], 1)

    def test_list_one_order(self):
        response = self.client.get(path=self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[0]['order_detail']), 2)
        self.assertEqual(len(response.data[0]['order_detail']), 2)
        self.assertEqual(response.data[0]['order_detail'][0]['product_id'], 1)

    def test_create_order(self):
        order_detail = {
            "order_detail": [
                {"product_id": 1, "quantity": 1},
                {"product_id": 2, "quantity": 1}
            ]
        }
        response = self.client.post(path=self.list_url, data=order_detail, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual({'message': 'order created'}, response.data)

    # def test_update_order(self):
    #     order_detail = {
    #         "order_detail": [
    #             {"product_id": 1, "quantity": 3},
    #             {"product_id": 2, "quantity": 1}
    #         ]
    #     }
    #     response = self.client.put(path=self.detail_url, data=order_detail, format="json")
    #     print(response.data)
    #     self.assertTrue(False)

    def test_update_order_with_bad_pk(self):
        response = self.client.put(path=self.detail_url, data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order(self):
        """Eliminar una orden. Restaura stock del producto"""
        response = self.client.get(path=self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({'message': 'order deleted'}, response.data)

        response = self.client.get(path=self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual({'message': 'order not found'}, response.data)

    def test_delete_order_with_bad_pk(self):
        response = self.client.delete(self.bad_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_get_total(self):
    #     self.assertTrue(False)
    #
    # def test_get_total_usd(self):
    #     self.assertTrue(False)

