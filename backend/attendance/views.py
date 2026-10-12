from rest_framework import viewsets

from users.permissions import IsSuperAdminOrReadOnly

from .models import Attendance, Schedule
from .serializers import AttendanceSerializer, ScheduleSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    """Attendance is private per person: students see their own record, a super
    admin sees everything, a teacher sees only lectures they teach."""

    serializer_class = AttendanceSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Attendance.objects.select_related('person')
        if user.is_super_admin:
            return qs
        if user.user_type == user.UserType.TEACHER:
            return qs.filter(
                person__taught_classes__in=user.taught_classes.all()).distinct()
        return qs.filter(person=user)

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        user = self.request.user
        person = serializer.validated_data.get('person')

        if user.is_super_admin:
            serializer.save(recorded_by=user)
            return
        if user.user_type != user.UserType.TEACHER:
            raise PermissionDenied('تسجيل الحضور يتطلب صلاحيات المدرس أو المشرف.')
        if person is None or not self._teacher_shares_class(user, person):
            raise PermissionDenied('لا يمكنك تسجيل حضور من خارج محاضراتك.')
        serializer.save(recorded_by=user)

    @staticmethod
    def _teacher_shares_class(teacher, person):
        """A teacher may record only members of a class they actually teach:
        every schedule dimension the teacher holds must match the person."""
        for schedule in teacher.taught_classes.all():
            if person.department_id != schedule.department_id:
                continue
            if person.stage_id != schedule.stage_id:
                continue
            if person.branch_id != schedule.branch_id:
                continue
            return True
        return False


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    permission_classes = [IsSuperAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        qs = Schedule.objects.select_related('teacher', 'department', 'stage', 'branch')
        if user.is_super_admin:
            return qs
        if user.user_type == user.UserType.TEACHER:
            return qs.filter(teacher=user)
        return qs
