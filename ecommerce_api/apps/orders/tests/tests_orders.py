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

    def test_list_orders(self):
        response = self.client.get(path=self.list_url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(len(response.data[0]['order_detail']), 2)

    def test_list_one_order(self):
        response = self.client.get(path=self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("one", response.data)
        self.assertEqual(len(response.data[0]['order_detail']), 2)

    # def test_create_order(self):
    #     """
    #     Registrar/Editar una orden (inclusive sus detalles).
    #
    #     Debe actualizar el stock del producto
    #
    #     Al crear o editar una orden validar q haya suficiente stock del producto, en caso no contar
    #     con stock se debe retornar un error de validación
    #
    #     Validar que no se repitan productos en el mismo pedido
    #     """
    #     self.assertTrue(False)
    #
    # def test_update_order(self):
    #     """
    #     Registrar/Editar una orden (inclusive sus detalles).
    #
    #     Debe actualizar el stock del producto
    #
    #     Al crear o editar una orden validar q haya suficiente stock del producto, en caso no contar
    #     con stock se debe retornar un error de validación
    #     """
    #     self.assertTrue(False)
    #
    # def test_update_order_with_bad_pk(self):
    #     self.assertTrue(False)
    #
    # def test_delete_order(self):
    #     """Eliminar una orden. Restaura stock del producto"""
    #     self.assertTrue(False)
    #
    # def test_delete_order_with_bad_pk(self):
    #     self.assertTrue(False)
    #
    # def test_get_total(self):
    #     self.assertTrue(False)
    #
    # def test_get_total_usd(self):
    #     self.assertTrue(False)

