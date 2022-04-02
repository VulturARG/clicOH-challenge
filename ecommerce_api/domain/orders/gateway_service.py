from requests import Response

from domain.gateway.gateway import Gateway


class DollarValue:
    """Get dollar blue value of a product"""

    TIMEOUT = 10

    def __init__(self, dollarsi_gateway: Gateway):
        self._dollarsi_gateway = dollarsi_gateway

    def get_dollar_blue_values(self) -> Response:
        """Get the dollar blue value."""

        return self._dollarsi_gateway.post(timeout=self.TIMEOUT)


