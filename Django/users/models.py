from django.db import models

class User(models.Model):
    USER_TYPES = [
        ('student', 'طالب'),
        ('teacher', 'مدرس'),
        ('administrative', 'موظف إداري'),
        ('security', 'موظف أمني'),
        ('service', 'موظف خدمة'),
    ]

    username = models.CharField(max_length=200, unique=True, verbose_name='اسم المستخدم')
    password = models.CharField(max_length=200, verbose_name='كلمة المرور')
    name = models.CharField(max_length=200, verbose_name='الاسم الكامل')
    user_type = models.CharField(max_length=20, choices=USER_TYPES, verbose_name='نوع المستخدم')
    email = models.EmailField(blank=True, verbose_name='البريد الإلكتروني')
    phone = models.CharField(max_length=20, blank=True, verbose_name='رقم الهاتف')
    department = models.CharField(max_length=200, blank=True, verbose_name='القسم')
    face_data = models.JSONField(blank=True, null=True, verbose_name='بيانات الوجه')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        verbose_name = 'مستخدم'
        verbose_name_plural = 'المستخدمين'

    def __str__(self):
        return f"{self.name} ({self.get_user_type_display()})"

class FaceProfile(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='الشخص')
    version = models.IntegerField(default=2, verbose_name='الإصدار')
    model_name = models.CharField(max_length=200, default='face-api.js', verbose_name='اسم النموذج')
    samples = models.JSONField(verbose_name='عينات الوجه')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')

    class Meta:
        verbose_name = 'ملف وجه'
        verbose_name_plural = 'ملفات الوجه'

    def __str__(self):
        return f"{self.person.name} - Face Profile v{self.version}"
