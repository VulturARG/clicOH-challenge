from rest_framework.routers import DefaultRouter

from apps.products.api.viewsets import ProductAPIViewSet

router = DefaultRouter()
router.register(r'', ProductAPIViewSet, basename='products')
urlpatterns = router.urls

