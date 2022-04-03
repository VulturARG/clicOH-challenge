import unittest
import requests_mock

from domain.gateway import ServerConfiguration
from domain.gateway.dolarsi_gateway import DollarURLGateway
from domain.gateway.exceptions import GatewayUnauthorized, GatewayEndpointNotFound


class TestServerGateway(unittest.TestCase):
    """Test ServerGateway class.

    Using https://requests-mock.readthedocs.io/en/latest/
    """

    def setUp(self) -> None:
        server_configuration = ServerConfiguration(
            api_root_url="http://good_url", user="user", password="password",
        )
        self.dollar_server_gateway = DollarURLGateway(server_configuration)

    def test_get_status_code_200(self):
        with requests_mock.Mocker() as rm:
            rm.get("http://good_url", status_code=200)

            response = self.dollar_server_gateway.get(None)
            self.assertEqual(response.status_code, 200)

    def test_get_status_code_401(self):
        with requests_mock.Mocker() as rm:
            rm.get("http://good_url", status_code=401)

            with self.assertRaises(GatewayUnauthorized) as context:
                self.dollar_server_gateway.get(None)

    def test_get_status_code_404(self):
        with requests_mock.Mocker() as rm:
            rm.get("http://good_url", status_code=404)

            with self.assertRaises(GatewayEndpointNotFound) as context:
                self.dollar_server_gateway.get(None)

    def test_post_status_code_200(self):
        with requests_mock.Mocker() as rm:
            rm.post("http://good_url", status_code=200)

            response = self.dollar_server_gateway.post(None)
            self.assertEqual(response.status_code, 200)

    def test_post_status_code_401(self):
        with requests_mock.Mocker() as rm:
            rm.post("http://good_url", status_code=401)

            with self.assertRaises(GatewayUnauthorized):
                self.dollar_server_gateway.post(None)

    def test_post_status_code_404(self):
        with requests_mock.Mocker() as rm:
            rm.post("http://good_url", status_code=404)

            with self.assertRaises(GatewayEndpointNotFound):
                self.dollar_server_gateway.post(None)

    def test_delete_status_code_200(self):
        with requests_mock.Mocker() as rm:
            rm.delete("http://good_url", status_code=200)

            response = self.dollar_server_gateway.delete(None)
            self.assertEqual(response.status_code, 200)

    def test_delete_status_code_401(self):
        with requests_mock.Mocker() as rm:
            rm.delete("http://good_url", status_code=401)

            with self.assertRaises(GatewayUnauthorized):
                self.dollar_server_gateway.delete(None)

    def test_delete_status_code_404(self):
        with requests_mock.Mocker() as rm:
            rm.delete("http://good_url", status_code=404)

            with self.assertRaises(GatewayEndpointNotFound):
                self.dollar_server_gateway.delete(None)
