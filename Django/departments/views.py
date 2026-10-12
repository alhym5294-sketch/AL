from rest_framework import viewsets

from users.permissions import IsSuperAdminOrReadOnly

from .models import Branch, Department, Stage
from .serializers import BranchSerializer, DepartmentSerializer, StageSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsSuperAdminOrReadOnly]


class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.select_related('department').all()
    serializer_class = StageSerializer
    permission_classes = [IsSuperAdminOrReadOnly]


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.select_related('stage__department').all()
    serializer_class = BranchSerializer
    permission_classes = [IsSuperAdminOrReadOnly]
