from typing import Any, Optional

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets

from apps.users.models import User
from apps.users.api.serializers import (
    UserSerializer, UserListSerializer, UpdateUserSerializer, PasswordSerializer
)


class UserViewSet(viewsets.GenericViewSet):
    model = User
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer
    queryset = None

    def get_object(self, pk: int) -> Any:
        return get_object_or_404(self.model, pk=pk)

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects \
                .filter(is_active=True) \
                .values('id', 'username', 'email', 'name')
        return self.queryset

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object(pk)
        password_serializer = PasswordSerializer(data=request.data)
        if not password_serializer.is_valid():
            return Response({
                'message': 'wrong information sent',
                'errors': password_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password_serializer.validated_data['password'])
        user.save()
        return Response({'message': 'password updated successfully'})

    def list(self, request: Request) -> Response:
        users = self.get_queryset()
        users_serializer = self.list_serializer_class(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        user_serializer = self.serializer_class(data=request.data)
        if not user_serializer.is_valid():
            return Response(
                {
                    'message': 'errors in the registry',
                    'errors': user_serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user_serializer.save()
        return Response({'message': 'successfully registered user'}, status=status.HTTP_201_CREATED)

    def retrieve(self, request: Request, pk: Optional[int] = None) -> Response:
        user = self.get_object(pk)
        user_serializer = self.serializer_class(user)
        return Response(user_serializer.data)

    def update(self, request: Request, pk: Optional[int] = None) -> Response:
        user = self.get_object(pk)
        user_serializer = UpdateUserSerializer(user, data=request.data)
        if not user_serializer.is_valid():
            return Response(
                {
                    'message': 'Hay errores en la actualización',
                    'errors': user_serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user_serializer.save()
        return Response({'message': 'user updated successfully'}, status=status.HTTP_200_OK)

    def destroy(self, request: Request, pk: Optional[int] = None) -> Response:
        user_destroy = self.model.objects.filter(id=pk).update(is_active=False)
        if user_destroy != 1:
            return Response({'message': 'user does not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'user deleted successfully'}, status=status.HTTP_200_OK)