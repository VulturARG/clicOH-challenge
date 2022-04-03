from rest_framework.routers import DefaultRouter

from apps.orders.api.viewset.order_viewset import OrderAPIViewSet

router = DefaultRouter()
router.register(r'', OrderAPIViewSet, basename='orders')
urlpatterns = router.urls
