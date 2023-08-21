from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .viewsets import AdvisorViewSet, UserViewSet

router = DefaultRouter()
router.register(r'advisor', AdvisorViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
