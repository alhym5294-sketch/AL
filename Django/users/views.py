from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import FaceProfile, User
from .permissions import IsSelfOrCreate, IsSuperAdmin
from .serializers import FaceProfileSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Accounts. Writes require the super admin; others see only their own record."""

    serializer_class = UserSerializer
    permission_classes = [IsSelfOrCreate]

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin:
            return User.objects.select_related('department', 'stage', 'branch').all()
        return User.objects.filter(pk=user.pk)

    def create(self, request, *args, **kwargs):
        if not request.user.is_super_admin:
            return Response({'error': 'إنشاء الحسابات يتطلب صلاحيات المشرف الأعلى.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_super_admin:
            if instance.pk != request.user.pk:
                return Response({'error': 'لا يمكنك تعديل حساب آخر.'},
                                status=status.HTTP_403_FORBIDDEN)
            if 'user_type' in request.data or 'is_superuser' in request.data:
                return Response(
                    {'error': 'تغيير الصفة الوظيفية أو الصلاحيات يتطلب المشرف الأعلى.'},
                    status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_super_admin:
            return Response({'error': 'حذف الحسابات يتطلب صلاحيات المشرف الأعلى.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'], permission_classes=[IsSuperAdmin])
    def deactivate(self, request, pk=None):
        """Deactivation keeps the account, its history and the audit trail."""
        user = self.get_object()
        user.is_active = False
        user.save(update_fields=['is_active', 'updated_at'])
        Token.objects.filter(user=user).delete()
        return Response({'status': 'deactivated', 'id': user.pk})

    @action(detail=True, methods=['post'], permission_classes=[IsSuperAdmin])
    def reactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save(update_fields=['is_active', 'updated_at'])
        return Response({'status': 'reactivated', 'id': user.pk})

    @action(detail=True, methods=['post'], permission_classes=[IsSuperAdmin])
    def reset_password(self, request, pk=None):
        user = self.get_object()
        new_password = request.data.get('password')
        if not new_password:
            return Response({'error': 'كلمة المرور الجديدة مطلوبة.'},
                            status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save(update_fields=['password'])
        # Force re-authentication with the new credential.
        Token.objects.filter(user=user).delete()
        return Response({'status': 'password_reset', 'id': user.pk})


class FaceProfileViewSet(viewsets.ModelViewSet):
    """Biometric profiles. Enrollment/verification is a super-admin action."""

    serializer_class = FaceProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = FaceProfile.objects.select_related('person').prefetch_related('samples')
        if self.request.user.is_super_admin:
            return qs
        return qs.filter(person=self.request.user)

    def create(self, request, *args, **kwargs):
        if not request.user.is_super_admin:
            return Response({'error': 'تسجيل بيانات الوجه يتطلب صلاحيات المشرف الأعلى.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.user.is_super_admin:
            return Response({'error': 'تعديل ملفات الوجه يتطلب صلاحيات المشرف الأعلى.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_super_admin:
            return Response({'error': 'حذف ملفات الوجه يتطلب صلاحيات المشرف الأعلى.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Token login. Replaces the plaintext localStorage check in Js/login.js."""
    username = (request.data.get('username') or '').strip()
    password = request.data.get('password') or ''

    if not username or not password:
        return Response({'error': 'اسم المستخدم وكلمة المرور مطلوبان.'},
                        status=status.HTTP_400_BAD_REQUEST)

    # authenticate() rejects inactive accounts, so a deactivated person cannot
    # obtain a token even with the correct password.
    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({'error': 'بيانات الدخول غير صحيحة.'},
                        status=status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'success': True,
        'token': token.key,
        'user': UserSerializer(user).data,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    Token.objects.filter(user=request.user).delete()
    return Response({'success': True})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    return Response(UserSerializer(request.user).data)
