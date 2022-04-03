from django.contrib import admin

from apps.orders.models import Order, OrderDetail

admin.site.register(Order)
admin.site.register(OrderDetail)

