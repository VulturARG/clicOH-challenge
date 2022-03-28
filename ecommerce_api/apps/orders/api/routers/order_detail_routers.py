from rest_framework.routers import DefaultRouter

from apps.orders.api.viewset.order_detail_viewset import OrderDetailListAPIViewSet

router = DefaultRouter()
router.register(r'', OrderDetailListAPIViewSet, basename='orders-detail')
urlpatterns = router.urls
