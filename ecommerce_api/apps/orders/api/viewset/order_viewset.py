from __future__ import annotations

from typing import Any, Optional, Dict, List

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer
from rest_framework.utils.serializer_helpers import ReturnDict

from apps.orders.api.order_repository import DRFOrderRepository
from apps.orders.api.serializers.order_detail_serializers import (
    OrderDetailSerializer,
    OrderRetrieveDetailSerializer
)
from apps.orders.api.serializers.order_serializers import OrderSerializer, OrderRetrieveSerializer
from apps.orders.models import OrderDetail
from apps.products.api.serializers import ProductListSerializer, ProductSerializer
from apps.products.models import Product
from domain.gateway import ServerConfiguration
from domain.gateway.dolarsi_gateway import DollarURLGateway
from domain.gateway.exceptions import GatewayException
from domain.orders.exceptions import OrderException, ProductInstanceError, OrderDetailInstanceError
from domain.orders.gateway_service import DollarValue
from domain.orders.service import OrderService
from domain.validate.validate import Validate
from ecommerce_api.settings.base import (
    API_DOLLAR_SI_URL,
    API_DOLLAR_SI_USERNAME,
    API_DOLLAR_SI_PASSWORD
)


class OrderAPIViewSet(viewsets.ModelViewSet):
    """Order ViewSet"""

    serializer_class = OrderSerializer
    serializer_class_order_detail = OrderDetailSerializer
    own_validate = Validate()

    def get_queryset(self, pk: Optional[int] = None) -> Any:
        """Get order queryset."""

        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    def list(self, request: Request, *args, **kwargs) -> Response:
        """List orders"""

        orders_serializer = self.get_serializer(self.get_queryset(), many=True)
        order_details_serializer = OrderDetailSerializer(self._get_order_detail(), many=True)

        order_repository = DRFOrderRepository(orders_serializer.data, order_details_serializer.data)
        service = OrderService(order_repository)

        return Response(service.get_orders(), status=status.HTTP_200_OK)

    def retrieve(self, request: Request, pk: int = None, *args, **kwargs) -> Response:
        """Retrieve an order"""

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

    def create(self, request: Request, *args, **kwargs) -> Response:
        """Create a new order"""

        order_serializer = self.serializer_class(data=request.data, own_validate=self.own_validate)
        if not order_serializer.is_valid():
            return Response(
                {'message': 'error', 'error': order_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        order_instance = order_serializer.save()
        order_details = self._get_order_detail_from_response(request, order_instance.id)
        try:
            updated_products = self._get_updated_products(order_serializer.data, order_details)
        except OrderException as error:
            return Response(
                {'message': 'error', 'error': error.MESSAGE},
                status=status.HTTP_400_BAD_REQUEST
            )
        self._save_products(updated_products)
        self._save_order_details(order_details)
        return Response({'message': 'order created'}, status=status.HTTP_201_CREATED)

    def update(self, request: Request, pk: Optional[int] = None, *args, **kwargs) -> Response:
        """Update an order"""

        new_order_detail = request.data['order_detail'] if 'order_detail' in request.data else []

        order = self.get_queryset(pk)
        if order is None:
            return Response({'message': 'order not found'}, status=status.HTTP_404_NOT_FOUND)

        order_serializer = self.serializer_class(data=request.data, own_validate=self.own_validate)
        if not order_serializer.is_valid():
            return Response(
                {'message': 'error', 'error': order_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        order_serializer.save()
        try:
            self._update_order_details_and_products(new_order_detail, order_serializer, pk)
        except OrderException as error:
            return Response(
                {'message': 'error', 'error': error.MESSAGE},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({'message': 'order updated'}, status=status.HTTP_200_OK)

    def destroy(self, request: Request, pk: Optional[int] = None, *args, **kwargs) -> Response:
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
            self._save_products(updated_products)
        except OrderException as error:
            return Response(
                {'message': 'error', 'error': error.MESSAGE},
                status=status.HTTP_400_BAD_REQUEST
            )
        order_model = self.get_object()
        self.perform_destroy(order_model)
        return Response({'message': 'order deleted'}, status=status.HTTP_200_OK)

    @action(detail=True)
    def get_total(self, request, pk=None) -> Response:
        """Get total of an order"""

        order = self.get_queryset(pk)
        if order is None:
            return Response({'message': 'order not found'}, status=status.HTTP_404_NOT_FOUND)
        orders_serializer = OrderRetrieveSerializer(order)

        order_repository = DRFOrderRepository(
            orders=orders_serializer.data,
            order_details=self._order_details_serializer_data(pk=pk),
            products=self._order_details_products()
        )
        service = OrderService(order_repository)
        index = orders_serializer.data['id']
        return Response({'message': service.get_total(index)}, status=status.HTTP_200_OK)

    @action(detail=True)
    def get_total_usd(self, request, pk=None) -> Response:
        """Get total of an order in USD"""

        response = self.get_total(request, pk)
        if not isinstance(response.data['message'], float):
            return Response(
                {'message': response.data['message']},
                status=status.HTTP_400_BAD_REQUEST
            )
        total_pesos = response.data['message']

        try:
            dollar_blue_price = self._get_dolar_blue_price()
        except (OrderException, GatewayException) as error:
            return Response({'message': error.MESSAGE}, status=status.HTTP_400_BAD_REQUEST)

        total_usd = total_pesos * dollar_blue_price
        return Response({'message': total_usd}, status=status.HTTP_200_OK)

    def _get_dolar_blue_price(self) -> float:
        """Get dollar blue price for external API."""

        server_configuration = ServerConfiguration(
            api_root_url=API_DOLLAR_SI_URL,
            user=API_DOLLAR_SI_USERNAME,
            password=API_DOLLAR_SI_PASSWORD,
        )
        server_gateway = DollarURLGateway(server_configuration)
        dollar_value = DollarValue(server_gateway)
        return dollar_value.get_dollar_blue_price()

    def _get_order_detail(self, pk: Optional[int] = None) -> Any:
        """Get order details in an order"""

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

    def _save_order_details(
            self,
            order_details: List[Dict[str, Any]]
    ) -> None:
        """Save order details."""

        for detail in order_details:
            query_set = None
            if "id" in detail:
                query_set = OrderDetail.objects.filter(pk=detail["id"]).first()
            order_detail_serializer = OrderDetailSerializer(
                query_set,
                data=detail,
                own_validate=self.own_validate
            )
            if not order_detail_serializer.is_valid():
                raise OrderDetailInstanceError()
            order_detail_serializer.save()

    def _save_products(self, updated_products) -> None:
        """Save products."""

        for product in updated_products.values():
            product_serializer = ProductSerializer(
                Product.objects.filter(pk=product["id"]).first(),
                data=product,
                own_validate=self.own_validate
            )
            if not product_serializer.is_valid():
                raise ProductInstanceError()
            product_serializer.save()

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

    def _get_order_detail_from_response(self, request: Request, pk: int) -> List[Dict[str, Any]]:
        orden_details = request.data['order_detail'] if 'order_detail' in request.data else []
        for detail in orden_details:
            detail['order'] = pk
        return orden_details

    def _match_order_detail_with_new_order_detail(
            self,
            order_details: List[Dict[str, Any]],
            new_order_details: List[Dict[str, Any]],
            delete: bool
    ) -> List[Dict[str, Any]]:
        index = [
            new_detail["id"]
            for new_detail in new_order_details
            if new_detail['id'] is not None
        ]
        matched_order_details = [detail for detail in order_details if detail['id'] in index]
        return matched_order_details if delete else new_order_details

    def _update_order_details_and_products(
            self,
            new_order_detail: List[Dict[str, Any]],
            order_serializer: OrderSerializer,
            pk: int
    ) -> None:
        """Update order details and products."""

        for delete in [True, False]:
            order_detail = self._order_details_for_update_or_delete(pk)

            updated_products = self._get_updated_products(
                order_serializer_data=order_serializer.data,
                order_detail=self._match_order_detail_with_new_order_detail(
                    order_detail,
                    new_order_detail,
                    delete
                ),
                delete=delete
            )
            self._save_products(updated_products)
            if not delete:
                self._save_order_details(new_order_detail)

