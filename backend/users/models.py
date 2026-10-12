from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Single account record for every person in the institution."""

    class UserType(models.TextChoices):
        ADMIN = 'admin', 'مشرف أعلى'
        TEACHER = 'teacher', 'مدرس'
        STUDENT = 'student', 'طالب'
        ADMINISTRATIVE = 'administrative', 'موظف إداري'
        SECURITY = 'security', 'موظف أمني'
        SERVICE = 'service', 'موظف خدمة'
        GATE = 'gate', 'بوابة'
        REGISTRATION = 'registration', 'قسم التسجيل'

    # New types must be added here; roles/permissions come from Groups, not from
    # this enum, so adding a type never requires rebuilding authorization.
    name = models.CharField('الاسم الكامل', max_length=200)
    user_type = models.CharField(
        'نوع المستخدم', max_length=20, choices=UserType.choices, db_index=True)
    code = models.CharField(
        'الرقم الوظيفي/الجامعي', max_length=50, unique=True, null=True, blank=True)
    phone = models.CharField('رقم الهاتف', max_length=20, blank=True)
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='members',
        verbose_name='القسم')
    subject = models.CharField('المادة', max_length=200, blank=True)
    stage = models.ForeignKey(
        'departments.Stage',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='users',
        verbose_name='المرحلة')
    branch = models.ForeignKey(
        'departments.Branch',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='users',
        verbose_name='الشعبة')
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)

    class Meta:
        verbose_name = 'مستخدم'
        verbose_name_plural = 'المستخدمين'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.get_user_type_display()})'

    @property
    def is_super_admin(self):
        return self.is_superuser or self.user_type == self.UserType.ADMIN


class FaceProfile(models.Model):
    """One active biometric profile per person, versioned by recognition model."""

    person = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='face_profile', verbose_name='الشخص')
    version = models.IntegerField('الإصدار', default=1)
    model_name = models.CharField('اسم النموذج', max_length=100, default='face-api.js')
    model_version = models.CharField('إصدار النموذج', max_length=50, default='1')
    is_verified = models.BooleanField('تم اعتماد الملف', default=False)
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)

    class Meta:
        verbose_name = 'ملف وجه'
        verbose_name_plural = 'ملفات الوجوه'
        ordering = ['person__name']

    def __str__(self):
        return f'{self.person.name} - {self.model_name} v{self.model_version}'


class FaceSample(models.Model):
    """A single captured descriptor. Kept per row so registration can grow and be
    audited without rewriting the whole profile."""

    class Source(models.TextChoices):
        REGISTRATION = 'registration', 'تسجيل أولي'
        RETAKE = 'retake', 'إعادة تسجيل'
        SUPPLEMENT = 'supplement', 'عينات إضافية'

    profile = models.ForeignKey(
        FaceProfile, on_delete=models.CASCADE,
        related_name='samples', verbose_name='الملف')
    embedding = models.JSONField('السمات')
    pose = models.CharField('الزاوية', max_length=30, blank=True)
    quality_score = models.FloatField('الجودة', default=0.0)
    source = models.CharField(
        max_length=20, choices=Source.choices, default=Source.REGISTRATION,
        verbose_name='المصدر')
    captured_at = models.DateTimeField('وقت الالتقاط', auto_now_add=True)

    class Meta:
        verbose_name = 'عينة وجه'
        verbose_name_plural = 'عينات الوجوه'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quality_score__gte=0, quality_score__lte=1),
                name='face_sample_quality_in_range'),
        ]
        indexes = [models.Index(fields=['profile', 'captured_at'])]

    def __str__(self):
        return f'{self.profile.person.username} - {self.pose or "unknown"}'
