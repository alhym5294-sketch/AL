from django.contrib import admin
from .models import Department, Stage, Branch

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'created_at']
    list_filter = ['department']
    search_fields = ['name']

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'stage', 'created_at']
    list_filter = ['stage']
    search_fields = ['name']
