from rest_framework.routers import DefaultRouter

from apps.orders.api.viewset.order_viewset import OrderListAPIViewSet

router = DefaultRouter()
router.register(r'', OrderListAPIViewSet, basename='orders')
urlpatterns = router.urls
