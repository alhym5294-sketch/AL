from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FaceProfileViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'face-profiles', FaceProfileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
