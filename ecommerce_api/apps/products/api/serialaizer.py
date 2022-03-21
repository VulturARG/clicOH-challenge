from typing import Any, Optional, Type

from rest_framework import serializers
from rest_framework.fields import empty

from apps.products.models import Product
from domain.vatidate.validate import Validate


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(
            self,
            instance: Optional[Any] = None,
            data: Type[empty] = empty,
            own_validate: Validate = None,
            **kwargs: Any,
    ) -> None:

        super().__init__(instance=instance, data=data, **kwargs)
        self.own_validate = own_validate

    def validate_price(self, value):
        if self.own_validate.is_less_than_zero(value):
            raise serializers.ValidationError("Price cannot be negative")
        return value

    def validate_stock(self, value):
        if self.own_validate.is_less_than_zero(value):
            raise serializers.ValidationError("Stock cannot be negative")
        return value

