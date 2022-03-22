from typing import Optional, Any, Type

from rest_framework import serializers
from rest_framework.fields import empty

from apps.orders.models import OrderDetail
from domain.vatidate.validate import Validate


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
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

