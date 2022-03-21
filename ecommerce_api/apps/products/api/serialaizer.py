from rest_framework import serializers

from apps.products.models import Product
from domain.vatidate.validate import Validate


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self):
        super().__init__()
        self.own_validate = Validate()

    def validate_price(self, value):
        if self.own_validate.is_less_than_zero(value):
            raise serializers.ValidationError("Price cannot be negative")
        return value

    def validate_stock(self, value):
        if self.own_validate.is_less_than_zero(value):
            raise serializers.ValidationError("Stock cannot be negative")
        return value

