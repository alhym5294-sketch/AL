from rest_framework import serializers
from .models import Department, Stage, Branch

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class StageSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Stage
        fields = '__all__'

class BranchSerializer(serializers.ModelSerializer):
    stage_name = serializers.CharField(source='stage.name', read_only=True)
    department_name = serializers.CharField(source='stage.department.name', read_only=True)

    class Meta:
        model = Branch
        fields = '__all__'
