from typing import Optional, Any

from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.products.api.serializers import ProductSerializer
from domain.vatidate.validate import Validate


class ProductAPIViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    own_validate = Validate()

    def get_queryset(self, pk: Optional[int] = None) -> Any:
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    def create(self, request: Any, *args, **kwargs) -> Response:
        """Create a new product"""

        serializer = self.serializer_class(data=request.data, own_validate=self.own_validate)
        if not serializer.is_valid():
            return Response(
                {'message': 'error', 'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response({'message': 'product created'}, status=status.HTTP_201_CREATED)

    def update(self, request: Any, pk: Optional[int] = None, *args, **kwargs) -> Response:
        """Update a product"""

        queryset = self.get_queryset(pk)
        if not queryset:
            return Response(
                {'error': 'bad index'},
                status=status.HTTP_404_NOT_FOUND
            )

        product_serializer = self.serializer_class(
            queryset, data=request.data, own_validate=self.own_validate
        )
        if not product_serializer.is_valid():
            return Response(
                {'message': 'error', 'error': product_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        product_serializer.save()
        return Response({'message': 'updated product'}, status=status.HTTP_200_OK)

    def destroy(self, request: Any, pk: Optional[int] = None, *args, **kwargs) -> Response:
        """Delete a product"""

        queryset = self.get_queryset(pk)
        if not queryset:
            return Response(
                {'error': 'bad index'},
                status=status.HTTP_404_NOT_FOUND
            )

        product_serializer = self.serializer_class(
            queryset, data=request.data, own_validate=self.own_validate
        )
        if not product_serializer.is_valid():
            return Response(
                {'message': 'error', 'error': product_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        product_serializer.save()
        return Response({'message': 'deleted product'}, status=status.HTTP_200_OK)

