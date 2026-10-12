from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FaceProfileViewSet, UserViewSet, login_view, logout_view, me_view

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'face-profiles', FaceProfileViewSet, basename='face-profile')

urlpatterns = [
    path('auth/login/', login_view, name='api-login'),
    path('auth/logout/', logout_view, name='api-logout'),
    path('auth/me/', me_view, name='api-me'),
    path('', include(router.urls)),
]
