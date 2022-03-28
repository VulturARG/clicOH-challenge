from typing import Any, Optional

from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.orders.api.serializers.order_detail_serializers import OrderDetailSerializer
from domain.vatidate.validate import Validate


class OrderDetailListAPIViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    own_validate = Validate()

    def get_queryset(self, pk: Optional[int] = None) -> Any:
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        return self.get_serializer().Meta.model.objects.filter(id=pk).first()


    # def list(self, request: Any, *args, **kwargs) -> Response:
    #     """List an order_id"""
    #
    #     pass
    #
    def create(self, request: Any, *args, **kwargs) -> Response:
        """Create a new order_id detail"""

        serializer = self.serializer_class(data=request.data, own_validate=self.own_validate)
        if not serializer.is_valid():
            return Response(
                {'message': 'error', 'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        # serializer.save()
        return Response({'message': 'order_id created'}, status=status.HTTP_201_CREATED)

    # def update(self, request: Any, pk: Optional[int] = None, *args, **kwargs) -> Response:
    #     """Update an order_id"""
    #
    #     pass
    #
    # def destroy(self, request: Any, pk: Optional[int] = None, *args, **kwargs) -> Response:
    #     """Delete an order_id"""
    #
    #     pass




