import urllib.parse

from django.contrib import admin
from django.urls import path, include

from ecommerce_api.settings.base import API_VERSION

urlpatterns = [
    path('admin/', admin.site.urls),
    path(urllib.parse.urljoin(API_VERSION, 'users/'), include('apps.users.api.urls')),
    path(urllib.parse.urljoin(API_VERSION, 'products/'), include('apps.products.api.routers')),
]

