from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSuperAdmin(BasePermission):
    message = 'هذه العملية تتطلب صلاحيات المشرف الأعلى.'

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_super_admin)


class IsSuperAdminOrReadOnly(BasePermission):
    """Master data (departments, stages, branches, schedules) is readable by any
    signed-in account but writable only by the super admin."""

    message = 'تعديل البيانات الأساسية يتطلب صلاحيات المشرف الأعلى.'

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True
        return user.is_super_admin


class IsSelfOrCreate(BasePermission):
    """Ordinary accounts may read themselves; only a super admin may write."""

    message = 'لا تملك صلاحية الوصول إلى هذا السجل.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_super_admin or obj == request.user
        return request.user.is_super_admin
