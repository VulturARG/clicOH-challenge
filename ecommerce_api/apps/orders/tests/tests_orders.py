import unittest

from apps.products.models import Product


class OrderTestCase(unittest.TestCase):

    def setUp(self):
        self.product_data = [
            {
                "name": 'Product 1',
                "description": 'Product 1 description',
                "price": '100.00',
                "stock": '10',
            },
            {
                "name": 'Product 2',
                "description": 'Product 2 description',
                "price": '200.00',
                "stock": '20',
            }
        ]
        for product in self.product_data:
            self.product = Product(**product)
            self.product.save()

    def test_list_orders(self):
        response = self.client.get(path=self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_one_order(self):
        """Consultar una orden y sus detalles"""
        pass

    def test_create_order(self):
        """
        Registrar/Editar una orden (inclusive sus detalles).

        Debe actualizar el stock del producto

        Al crear o editar una orden validar q haya suficiente stock del producto, en caso no contar
        con stock se debe retornar un error de validación

        Validar que no se repitan productos en el mismo pedido
        """
        pass

    def test_update_order(self):
        """
        Registrar/Editar una orden (inclusive sus detalles).

        Debe actualizar el stock del producto

        Al crear o editar una orden validar q haya suficiente stock del producto, en caso no contar
        con stock se debe retornar un error de validación
        """
        pass

    def test_update_order_with_bad_pk(self):
        pass

    def test_delete_order(self):
        """Eliminar una orden. Restaura stock del producto"""
        pass

    def test_delete_order_with_bad_pk(self):
        pass

    def test_get_total(self):
        pass

    def test_get_total_usd(self):
        pass


if __name__ == '__main__':
    unittest.main()
