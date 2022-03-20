from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.products.api.serialaizer import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    # def list(self, request):
    #
    #     queryset = self.get_queryset()
    #     product_serializer = self.get_serializer(queryset, many=True)
    #     data = {
    #         "total": queryset.count(),
    #         "totalNotFiltered": queryset.count(),
    #         "rows": product_serializer.data
    #     }
    #     return Response(data, status=status.HTTP_200_OK)

    def create(self, request):
        """send information to serializer"""

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'message': 'error', 'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response({'message': 'product created'}, status=status.HTTP_201_CREATED)

    # def retrieve(self, request, pk=None):
    #     product = self.get_queryset(pk)
    #     if product:
    #         product_serializer = ProductRetrieveSerializer(product)
    #         return Response(product_serializer.data, status=status.HTTP_200_OK)
    #     return Response({'error':'No existe un Producto con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if not self.get_queryset(pk):
            return

        product_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
        if not product_serializer.is_valid():
            return Response(
                {'message': 'error', 'error': product_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        product_serializer.save()
        return Response({'message': 'updated product'}, status=status.HTTP_200_OK)


    # def destroy(self, request, pk=None):
    #     product = self.get_queryset().filter(id=pk).first() # get instance
    #     if product:
    #         product.state = False
    #         product.save()
    #         return Response({'message':'Producto eliminado correctamente!'}, status=status.HTTP_200_OK)
    #     return Response({'error':'No existe un Producto con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)
