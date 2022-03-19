from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.models import User
from apps.users.api.serializers import UserSerializer


class UserApiView(APIView):
    """Global User API View"""

    def get(self, request):
        """Get all users"""

        users = User.objects.all()
        users_serializer = UserSerializer(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new user"""

        users_serializer = UserSerializer(data=request.data)
        if not users_serializer.is_valid():
            return Response(users_serializer.errors, status=status.HTTP_404_NOT_FOUND)

        users_serializer.save()
        return Response(users_serializer.data, status=status.HTTP_201_CREATED)


class UserDetailApiView(APIView):
    """User Detail API View"""

    def get(self, request, pk):
        """Get a user"""

        user = User.objects.filter(pk=pk).first()
        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Update a user"""

        user = User.objects.filter(pk=pk).first()
        user_serializer = UserSerializer(user, data=request.data)
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """Delete a user"""

        user = User.objects.filter(pk=pk).first()
        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({'message': 'User deleted'}, status=status.HTTP_200_OK)

