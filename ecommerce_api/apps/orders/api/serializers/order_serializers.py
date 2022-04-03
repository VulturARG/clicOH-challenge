from typing import Optional, Any, Type

from rest_framework import serializers
from rest_framework.fields import empty

from apps.orders.models import Order
from domain.validate.validate import Validate


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
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


class OrderRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

