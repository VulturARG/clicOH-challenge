from rest_framework import status
from rest_framework.test import APITestCase

from apps.products.api.viewsets import ProductAPIViewSet
from apps.products.models import Product


class ProductsTestCase(APITestCase):
    list_url = "/v1/products/"
    detail_url = "/v1/products/1/"
    bad_detail_url = "/v1/products/0/"

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
            product_instance = Product(**product)
            product_instance.save()

    def test_product_list(self):
        response = self.client.get(path=self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_an_existing_product(self):
        response = self.client.get(path=self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Product 1")

    def test_a_non_existing_product(self):
        response = self.client.get(path=self.bad_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_product(self):
        data = {
            "name": 'Product 3',
            "description": 'Product 3 description',
            "price": '300.00',
            "stock": '30',
        }

        response = self.client.post(path=self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "product created")

    def test_update_product(self):
        response = self.client.put(
            path=self.detail_url, data=self.product_data[0], format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "updated product")

    def test_update_with_bad_pk(self):
        response = self.client.put(
            path=self.bad_detail_url, data=self.product_data[0], format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "bad index")

    def test_delete_an_existing_product(self):
        response = self.client.get(path=self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Product 1")

        response = self.client.delete(
            path=self.detail_url, data=self.product_data[0], format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "deleted product")

        response = self.client.get(path=self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_a_non_existing_product(self):
        response = self.client.delete(
            path=self.bad_detail_url, data=self.product_data[0], format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "bad index")


