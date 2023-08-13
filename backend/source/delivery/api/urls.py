from django.urls import path
from delivery.api.views import (
    CustomerViewSet,
    TgServiceViewSet,
    OrderViewSet,
    DeliveryScheduleViewSet
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

app_name = 'delivery'

router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'tgservices', TgServiceViewSet, basename='tgservice')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'deliveryschedules', DeliveryScheduleViewSet, basename='deliveryschedule')

urlpatterns = router.urls

