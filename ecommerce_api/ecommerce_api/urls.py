import urllib.parse

from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.views import Logout, Login
from ecommerce_api.settings.base import API_VERSION

schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="API for ecommerce ClicOH challenge",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns_swagger = [
   re_path(
       r'^swagger(?P<format>\.json|\.yaml)$',
       schema_view.without_ui(cache_timeout=0),
       name='schema-json'
   ),
   re_path(
       r'^swagger/$',
       schema_view.with_ui('swagger', cache_timeout=0),
       name='schema-swagger-ui'
   ),
   re_path(
       r'^redoc/$',
       schema_view.with_ui('redoc', cache_timeout=0),
       name='schema-redoc'),
]

urlpatterns = urlpatterns_swagger + [
    path('admin/', admin.site.urls),
    path('logout/', Logout.as_view(), name='logout'),
    path('login/', Login.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(urllib.parse.urljoin(API_VERSION, 'users/'), include('apps.users.api.routers')),
    path(urllib.parse.urljoin(API_VERSION, 'products/'), include('apps.products.api.routers')),
    path(urllib.parse.urljoin(API_VERSION, 'orders/'), include('apps.orders.api.routers')),
]

