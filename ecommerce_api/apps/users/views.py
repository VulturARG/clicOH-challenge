from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.api.serializers import (
    CustomTokenObtainPairSerializer, CustomUserSerializer
)
from apps.users.models import User


class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {'error': 'incorrect username or password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        login_serializer = self.serializer_class(data=request.data)
        if not login_serializer.is_valid():
            return Response(
                {'error': 'incorrect username or password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_serializer = CustomUserSerializer(user)
        return Response(
            {
                'token': login_serializer.validated_data.get('access'),
                'refresh-token': login_serializer.validated_data.get('refresh'),
                'user': user_serializer.data,
                'message': 'login successful'
            },
            status=status.HTTP_200_OK
        )


class Logout(GenericAPIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        user = User.objects.filter(id=request.data.get('user', 0))
        if not user.exists():
            return Response({'error': 'user does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        RefreshToken.for_user(user.first())
        return Response({'message': 'successfully closed session'}, status=status.HTTP_200_OK)
