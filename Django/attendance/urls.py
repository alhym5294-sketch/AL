from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet, ScheduleViewSet

router = DefaultRouter()
router.register(r'attendance', AttendanceViewSet)
router.register(r'schedule', ScheduleViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
