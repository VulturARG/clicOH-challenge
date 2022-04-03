from typing import Optional


class GatewayException(Exception):
    """Base class for all exceptions in this module."""

    MESSAGE: Optional[str] = None


class GatewayUnauthorized(GatewayException):
    MESSAGE = "Unauthorized"

    def __init__(self) -> None:
        super().__init__(self.MESSAGE)


class GatewayEndpointNotFound(GatewayException):
    MESSAGE = "Wrong URL"

    def __init__(self) -> None:
        super().__init__(self.MESSAGE)
