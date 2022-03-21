from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.users.models import User


class UserTestCase(APITestCase):
    list_url = reverse("api-user")
    detail_url = reverse("api-user-detail", args=["1"])

    def setUp(self):
        self.user = User.objects.create_user(
            name="John",
            last_name="Wick",
            email="wick@example.com",
            username="wick",
            password="jf897453!"
        )

    def test_bad_path(self):
        response = self.client.get("/bad_path/", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_an_existing_user(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "wick")

    def test_create_user(self):
        data = {
            "name": "Peter",
            "last_name": "Parker",
            "email": "peter@example.com",
            "username": "peter",
            "password": "jf897453!",
        }

        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "peter")

    def test_create_user_with_invalid_email(self):
        data = {
            "name": "Peter",
            "last_name": "Parker",
            "email": "peter",
            "username": "peter",
            "password": "jdf897453!",
        }

        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user(self):
        data = {
            "name": "Peter",
            "last_name": "Pan",
            "email": "peter@pepe.com",
            "username": "peter",
            "password": "jhg897453!",
        }

        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["last_name"], "Pan")

    def test_delete_an_existing_user(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "User deleted")
        
        