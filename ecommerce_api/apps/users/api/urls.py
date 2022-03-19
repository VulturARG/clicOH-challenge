from django.urls import path
from apps.users.api.api import UserApiView, UserDetailApiView

urlpatterns = [
    path('', UserApiView.as_view(), name='api-user'),
    path('<int:pk>/', UserDetailApiView.as_view(), name='api-user-detail'),
]
