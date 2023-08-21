from rest_framework import routers
from django.urls import path, include
from .viewsets import AdminProductViewSet, AdvisorProductLinkViewSet

router = routers.DefaultRouter()
router.register(r'admin-products', AdminProductViewSet)
router.register(r'purchase-products', AdvisorProductLinkViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
