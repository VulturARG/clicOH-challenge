from __future__ import annotations

from typing import Any, Optional, Dict, List

from django.db import models

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer
from rest_framework.utils.serializer_helpers import ReturnDict

from apps.orders.api.order_repository import DRFOrderRepository
from apps.orders.api.serializers.order_detail_serializers import (
    OrderDetailSerializer,
    OrderRetrieveDetailSerializer
)
from apps.orders.api.serializers.order_serializers import OrderSerializer, OrderRetrieveSerializer
from apps.orders.models import OrderDetail, Order
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
        order_details_serializer = OrderDetailSerializer(self._get_order_detail(), many=True)

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
            order_details=self._order_details_serializer_data(pk=pk),
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
        order_model = order_serializer.save()
        order_detail = request.data.get('order_detail')
        try:
            updated_products = self._get_updated_products(order_serializer.data, order_detail)
        except OrderException as error:
            return Response(
                {'message': 'error', 'error': error.MESSAGE},
                status=status.HTTP_400_BAD_REQUEST
            )
        self._save(order_model, order_detail, updated_products)
        return Response({'message': 'order created'}, status=status.HTTP_201_CREATED)

    def update(self, request: Any, pk: Optional[int] = None, *args, **kwargs) -> Response:
        """Update an order"""

        order = self.get_queryset(pk)
        if order is None:
            return Response({'message': 'order not found'}, status=status.HTTP_404_NOT_FOUND)

        order_serializer = self.serializer_class(data=request.data, own_validate=self.own_validate)
        if not order_serializer.is_valid():
            return Response(
                {'message': 'error', 'error': order_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        order_model = order_serializer.save()
        order_detail = self._order_details_for_update_or_delete(pk)
        try:
            updated_products = self._get_updated_products(order_serializer.data, order_detail)
        except OrderException as error:
            return Response(
                {'message': 'error', 'error': error.MESSAGE},
                status=status.HTTP_400_BAD_REQUEST
            )
        self._save(order_model, order_detail, updated_products)
        return Response({'message': 'order updated'}, status=status.HTTP_200_OK)

    def destroy(self, request: Any, pk: Optional[int] = None, *args, **kwargs) -> Response:
        """Delete an order"""

        order = self.get_queryset(pk)
        if order is None:
            return Response({'message': 'order not found'}, status=status.HTTP_404_NOT_FOUND)

        order_serializer = self.serializer_class(data=request.data, own_validate=self.own_validate)
        if not order_serializer.is_valid():
            return Response(
                {'message': 'error', 'error': order_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        order_detail = self._order_details_for_update_or_delete(pk)
        try:
            updated_products = self._get_updated_products(
                order_serializer_data=order_serializer.data,
                order_detail=order_detail,
                delete=True
            )
        except OrderException as error:
            return Response(
                {'message': 'error', 'error': error.MESSAGE},
                status=status.HTTP_400_BAD_REQUEST
            )
        self._save_products(updated_products)
        order_model = self.get_object()
        self.perform_destroy(order_model)
        return Response({'message': 'order deleted'}, status=status.HTTP_200_OK)

    @action(detail=True)
    def get_total(self, request, pk=None) -> Response:
        """Get total of an order"""

    @action(detail=True)
    def get_total_usd(self, request, pk=None) -> Response:
        """Get total of an order in USD"""

    def _get_order_detail(self, pk: Optional[int] = None) -> Any:
        """Get order detail in an order"""

        if pk is None:
            return OrderDetail.objects.all()
        return OrderDetail.objects.filter(order=pk)

    def _order_details_serializer_data(self, pk: Optional[int] = None) -> Optional[ListSerializer]:
        """Get order details in serializer data"""

        order_details = self._get_order_detail(pk)

        if order_details is None:
            return None

        order_details_serializer = OrderRetrieveDetailSerializer(order_details, many=True)
        return order_details_serializer.data

    def _get_queryset_products(self, pk: Optional[int] = None) -> Any:
        """Get products from order."""
        if pk is None:
            return Product.objects.all()
        return Product.objects.filter(order=pk).first()

    def _order_details_products(self, pk: Optional[int] = None) -> Optional[ListSerializer]:
        """Get all products in an order."""
        products = self._get_queryset_products(pk)

        if products is None:
            return None

        products_serializer = ProductListSerializer(products, many=True)
        return products_serializer.data

    def _get_updated_products(
            self,
            order_serializer_data: ListSerializer | ReturnDict,
            order_detail: List[Dict[str, Any]],
            delete: Optional[bool] = False
    ) -> Dict[str, Any]:
        """Get updated stocks in products."""

        order_repository = DRFOrderRepository(
            orders=order_serializer_data,
            products=self._order_details_products(),
        )
        service = OrderService(order_repository)
        return service.get_new_stock_of_the_products(order_detail, delete)

    def _save(
            self,
            order_model: Order,
            order_detail: List[Dict[str, Any]],
            updated_products: Dict[str, Any]
    ) -> None:
        """Save order, order detail and update stock of products."""

        product_instances = self._save_products(updated_products)

        updated_details = {}
        for detail in order_detail:
            updated_details["order"] = order_model
            updated_details["product"] = product_instances[detail["product_id"] - 1]
            updated_details["quantity"] = detail["quantity"]
            order_detail_instance = OrderDetail(**updated_details)
            order_detail_instance.save()

    def _save_products(self, updated_products) -> List[Product]:
        product_instances = []
        for product in updated_products.values():
            product_instance = Product(**product)
            product_instance.save()
            product_instances.append(product_instance)
        return product_instances

    def _delete(
            self,
            order_model: Order,
            order_detail: List[Dict[str, Any]],
            updated_products: Dict[str, Any]
    ) -> None:
        """Delete order, order detail and update stock of products."""

    def _order_details_for_update_or_delete(self, pk: int) -> List[Dict[str, Any]]:
        order_detail = []
        for detail in self._order_details_serializer_data(pk):
            order_detail.append(
                {
                    "id": detail["id"],
                    "order": detail["order"],
                    "product_id": detail["product"],
                    "quantity": detail["quantity"],
                }
            )
        return order_detail

