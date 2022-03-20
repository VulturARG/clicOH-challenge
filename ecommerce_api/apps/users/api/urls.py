from django.urls import path
from apps.users.api.api import UserAPIView, UserDetailAPIView

urlpatterns = [
    path('', UserAPIView.as_view(), name='api-user'),
    path('<int:pk>/', UserDetailAPIView.as_view(), name='api-user-detail'),
]
