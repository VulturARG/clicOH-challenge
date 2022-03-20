from rest_framework import status
from rest_framework.test import RequestsClient, APITestCase

from apps.products.models import Product


class ProductsTestCase(APITestCase):
    def setUp(self):

        self.product_data = {
            "name": 'Product 1',
            "description": 'Product 1 description',
            "price": '100.00',
            "stock": '10',
        }

        self.product = Product.objects.create(
            name=self.product_data['name'],
            description=self.product_data['description'],
            price=self.product_data['price'],
            stock=self.product_data['stock'],
        )

    def test_product_list(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/v1/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bad_path(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/v1/badpath/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_an_existing_product(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/v1/products/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_create_product(self):
    #     client = RequestsClient()
    #     response = client.post('http://127.0.0.1:8000/v1/products/', json=self.product_data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Product.objects.count(), 1)

    def test_create_product(self):
        self.product.save()

        product_data = {
            "name": 'Product 1',
            "description": 'Product 1 description',
            "price": '100.00',
            "stock": '100',
        }

        client = RequestsClient()
        response = client.put('http://127.0.0.1:8000/v1/products/1', product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
