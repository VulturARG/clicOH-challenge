from typing import Optional


class OrderException(Exception):
    """Base class for all exceptions in this module."""

    MESSAGE: Optional[str] = None


class ProductNotUniqueError(OrderException):
    MESSAGE = "there are more than one product type per order"

    def __init__(self) -> None:
        super().__init__(self.MESSAGE)


class ProductInstanceError(OrderException):
    MESSAGE = "product instance not valid"

    def __init__(self) -> None:
        super().__init__(self.MESSAGE)


class NotEnoughStockError(OrderException):
    MESSAGE = "not enough stock"

    def __init__(self) -> None:
        super().__init__(self.MESSAGE)


class QuantityEqualOrLessThanZeroError(OrderException):
    MESSAGE = "quantity must be greater than zero"

    def __init__(self) -> None:
        super().__init__(self.MESSAGE)


class ThereAreNoProductsError(OrderException):
    MESSAGE = "there are no products"

    def __init__(self) -> None:
        super().__init__(self.MESSAGE)


class OrderDetailInstanceError(OrderException):
    MESSAGE = "order detail instance not valid"

    def __init__(self) -> None:
        super().__init__(self.MESSAGE)


class DollarBluePriceNotFoundError(OrderException):
    MESSAGE = "dollar blue price not found"

    def __init__(self) -> None:
        super().__init__(self.MESSAGE)

