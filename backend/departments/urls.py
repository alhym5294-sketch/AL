from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import BranchViewSet, DepartmentViewSet, StageViewSet

router = SimpleRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'stages', StageViewSet, basename='stage')
router.register(r'branches', BranchViewSet, basename='branch')

urlpatterns = [
    path('', include(router.urls)),
]
