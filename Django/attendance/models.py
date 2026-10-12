from django.db import models
from users.models import User

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'حاضر'),
        ('absent', 'غائب'),
        ('late', 'متأخر'),
    ]

    person = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='الشخص')
    date = models.DateField(verbose_name='التاريخ')
    time = models.TimeField(verbose_name='الوقت')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='الحالة')
    location = models.CharField(max_length=200, default='البوابة الرئيسية', verbose_name='الموقع')
    notes = models.TextField(blank=True, verbose_name='ملاحظات')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ التسجيل')

    class Meta:
        verbose_name = 'سجل حضور'
        verbose_name_plural = 'سجلات الحضور'
        unique_together = ['person', 'date']

    def __str__(self):
        return f"{self.person.name} - {self.date} ({self.get_status_display()})"

class Schedule(models.Model):
    DAY_CHOICES = [
        ('sunday', 'الأحد'),
        ('monday', 'الاثنين'),
        ('tuesday', 'الثلاثاء'),
        ('wednesday', 'الأربعاء'),
        ('thursday', 'الخميس'),
        ('friday', 'الجمعة'),
        ('saturday', 'السبت'),
    ]

    day = models.CharField(max_length=10, choices=DAY_CHOICES, verbose_name='اليوم')
    time = models.TimeField(verbose_name='الوقت')
    subject = models.CharField(max_length=200, verbose_name='المادة')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_classes', verbose_name='المدرس')
    department = models.CharField(max_length=200, verbose_name='القسم')
    stage = models.CharField(max_length=200, verbose_name='المرحلة')
    branch = models.CharField(max_length=200, verbose_name='الشعبة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')

    class Meta:
        verbose_name = 'جدول دراسي'
        verbose_name_plural = 'الجداول الدراسية'

    def __str__(self):
        return f"{self.day} - {self.time} - {self.subject}"
