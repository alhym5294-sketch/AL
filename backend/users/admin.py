from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import FaceProfile, FaceSample, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ['name', 'username', 'user_type', 'code', 'department', 'is_active']
    list_filter = ['user_type', 'department', 'is_active']
    search_fields = ['name', 'username', 'code', 'phone']
    ordering = ['name']
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('بيانات MUQ', {
            'fields': ('name', 'user_type', 'code', 'phone', 'department',
                       'subject', 'stage', 'branch'),
        }),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ('بيانات MUQ', {
            'fields': ('name', 'user_type', 'code', 'department'),
        }),
    )


class FaceSampleInline(admin.TabularInline):
    model = FaceSample
    extra = 0
    # The descriptor column is deliberately absent: biometric material must not
    # render into an admin page or its change-history diff.
    fields = ['pose', 'quality_score', 'source', 'captured_at']
    readonly_fields = ['pose', 'quality_score', 'source', 'captured_at']


@admin.register(FaceProfile)
class FaceProfileAdmin(admin.ModelAdmin):
    list_display = ['person', 'model_name', 'model_version', 'sample_count',
                    'is_verified', 'updated_at']
    list_filter = ['model_name', 'model_version', 'is_verified']
    search_fields = ['person__name', 'person__username', 'person__code']
    inlines = [FaceSampleInline]
    readonly_fields = ['created_at', 'updated_at']

    @admin.display(description='عدد العينات')
    def sample_count(self, obj):
        return obj.samples.count()
