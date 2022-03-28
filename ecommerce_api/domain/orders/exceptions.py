from typing import Optional


class OrderException(Exception):
    """Base class for all exceptions in this module."""

    MESSAGE: Optional[str] = None


class ProductNotUniqueError(OrderException):
    MESSAGE = "there are more than one product_id type per order_id"

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
