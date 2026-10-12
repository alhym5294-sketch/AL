from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, StageViewSet, BranchViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'stages', StageViewSet)
router.register(r'branches', BranchViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
