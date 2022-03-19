from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, RequestsClient

from apps.users.api.api import UserApiView
from apps.users.models import User


class UserTestCase(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            email="name@example.com",
            name="Anne",
            last_name="Bowles",
            username="anne",
            password="jhgdf897453!",
        )

        self.user2 = User.objects.create_user(
            email="name2@example.com",
            name="Peter",
            last_name="West",
            username="peter",
            password="jhgdf897999!",
        )

    def test_create_user(self):

        self.assertEqual(self.user.username, "anne")

    def test_non_existing_user_1(self):
        """Test an existing user."""

        factory = APIRequestFactory()
        view = UserApiView.as_view()
        request = factory.get("/users/1", format="json")
        force_authenticate(request, user=None)
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_user_list(self):

        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bad_path(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/v1/badpath/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_an_existing_user(self):

        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/v1/users/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_non_existing_user(self):
    #
    #     client = RequestsClient()
    #     response = client.get('http://127.0.0.1:8000/v1/users/2')
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_user_list(self):
    #     """Test the user list endpoint."""
    #
    #     factory = APIRequestFactory()
    #     view = UserApiView.as_view()
    #     request = factory.get("/users/", format="json")
    #     force_authenticate(request, user=self.user)
    #     response = view(request)
    #     self.assertEqual(response.status_code, 200)
    #

