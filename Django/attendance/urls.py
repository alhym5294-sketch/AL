from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import AttendanceViewSet, ScheduleViewSet

router = SimpleRouter()
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'schedule', ScheduleViewSet, basename='schedule')

urlpatterns = [
    path('', include(router.urls)),
]
