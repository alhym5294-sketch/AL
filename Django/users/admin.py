from django.contrib import admin
from .models import User, FaceProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'user_type', 'department', 'created_at']
    list_filter = ['user_type', 'department']
    search_fields = ['name', 'username']

@admin.register(FaceProfile)
class FaceProfileAdmin(admin.ModelAdmin):
    list_display = ['person', 'version', 'model_name', 'created_at']
    list_filter = ['version', 'model_name']
