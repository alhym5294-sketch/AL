from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=200, verbose_name='اسم القسم')
    description = models.TextField(blank=True, verbose_name='الوصف')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        verbose_name = 'قسم'
        verbose_name_plural = 'الأقسام'

    def __str__(self):
        return self.name

class Stage(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='القسم')
    name = models.CharField(max_length=200, verbose_name='اسم المرحلة')
    description = models.TextField(blank=True, verbose_name='الوصف')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        verbose_name = 'مرحلة'
        verbose_name_plural = 'المراحل'

    def __str__(self):
        return f"{self.department.name} - {self.name}"

class Branch(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, verbose_name='المرحلة')
    name = models.CharField(max_length=200, verbose_name='اسم الشعبة')
    description = models.TextField(blank=True, verbose_name='الوصف')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        verbose_name = 'شعبة'
        verbose_name_plural = 'الشعب'

    def __str__(self):
        return f"{self.stage.name} - {self.name}"
