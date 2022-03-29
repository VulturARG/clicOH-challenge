import json
from typing import Any, Optional

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer

from apps.orders.api.order_repository import DRFOrderRepository
from apps.orders.api.serializers.order_detail_serializers import (
    OrderDetailSerializer,
    OrderRetrieveDetailSerializer
)
from apps.orders.api.serializers.order_serializers import OrderSerializer, OrderRetrieveSerializer
from apps.orders.models import OrderDetail
from apps.products.api.serializers import ProductListSerializer
from apps.products.models import Product
from domain.orders.exceptions import OrderException
from domain.orders.service import OrderService
from domain.vatidate.validate import Validate


class OrderListAPIViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    serializer_class_order_detail = OrderDetailSerializer
    own_validate = Validate()

    def get_queryset(self, pk: Optional[int] = None) -> Any:
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    def list(self, request: Any, *args, **kwargs) -> Response:
        """List orders"""

        orders_serializer = self.get_serializer(self.get_queryset(), many=True)
        order_details_serializer = OrderDetailSerializer(
            self._get_queryset_order_detail(),
            many=True
        )

        order_repository = DRFOrderRepository(orders_serializer.data, order_details_serializer.data)
        service = OrderService(order_repository)

        return Response(service.get_orders(), status=status.HTTP_200_OK)

    def retrieve(self, request: Any, pk: int = None, *args, **kwargs) -> Response:
        order = self.get_queryset(pk)
        if order is None:
            return Response({'message': 'order not found'}, status=status.HTTP_404_NOT_FOUND)
        orders_serializer = OrderRetrieveSerializer(order)

        order_repository = DRFOrderRepository(
            orders=orders_serializer.data,
            order_details= self._order_details_serializer_data(pk=pk),
        )
        service = OrderService(order_repository)

        return Response(service.get_orders(), status=status.HTTP_200_OK)

    def create(self, request: Any, *args, **kwargs) -> Response:
        """Create a new order"""

        order_serializer = self.serializer_class(data=request.data, own_validate=self.own_validate)
        if not order_serializer.is_valid():
            return Response(
                {'message': 'error', 'error': order_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # pepe = order_serializer.save()
        # print(pepe)

        order_detail = request.data.get('order_detail')

        order_repository = DRFOrderRepository(
            orders=order_serializer.data,
            products=self._order_details_products(),
        )
        service = OrderService(order_repository)
        try:
            updated_products = service.get_new_stock_of_the_products(order_detail)
        except OrderException as error:
            return Response(
                {'message': 'error', 'error': error.MESSAGE},
                status=status.HTTP_400_BAD_REQUEST
            )

        #
        od = OrderDetail(order_detail)
        print(od)
        print(updated_products)

        return Response(
            {
                'message': 'order created',
                # "products": serializer_class_order_detail.data if order_serializer.data else None
                "products": order_detail
            },
            status=status.HTTP_201_CREATED
        )

    # def update(self, request: Any, pk: Optional[int] = None, *args, **kwargs) -> Response:
    #     """Update an order"""
    #
    #     pass
    #
    # def destroy(self, request: Any, pk: Optional[int] = None, *args, **kwargs) -> Response:
    #     """Delete an order"""
    #
    #     pass

    @action(detail=True)
    def get_total(self, request, pk=None) -> Response:
        pass

    @action(detail=True)
    def get_total_usd(self, request, pk=None) -> Response:
        pass

    def _get_queryset_order_detail(self, pk: Optional[int] = None) -> Any:
        if pk is None:
            return OrderDetail.objects.all()
        return OrderDetail.objects.filter(order=pk).first()

    def _order_details_serializer_data(self, pk: Optional[int] = None) -> Optional[ListSerializer]:
        order_details = self._get_queryset_order_detail(pk)

        if order_details is None:
            return None

        order_details_serializer = OrderRetrieveDetailSerializer(order_details)
        return order_details_serializer.data

    def _get_queryset_products(self, pk: Optional[int] = None) -> Any:
        if pk is None:
            return Product.objects.all()
        return Product.objects.filter(order=pk).first()

    def _order_details_products(self, pk: Optional[int] = None) -> Optional[ListSerializer]:
        products = self._get_queryset_products(pk)

        if products is None:
            return None

        products_serializer = ProductListSerializer(products, many=True)
        return products_serializer.data



