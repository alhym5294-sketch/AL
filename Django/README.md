# نظام MUQ - Django Backend

هذا هو الـ Backend لنظام MUQ باستخدام Django و Django REST Framework.

## 📋 المتطلبات

- Python 3.8+
- PostgreSQL 12+
- pip

## 🚀 التثبيت

### 1. إنشاء البيئة الافتراضية

```bash
cd Django
python -m venv venv
```

### 2. تفعيل البيئة الافتراضية

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. تثبيت الحزم

```bash
pip install -r requirements.txt
```

### 4. إعداد قاعدة البيانات

**إنشاء قاعدة بيانات PostgreSQL:**
```sql
CREATE DATABASE muq_system;
```

**تعديل إعدادات قاعدة البيانات في `muq_system/settings.py`:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'muq_system',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. تشغيل الترحيلات

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. إنشاء مستخدم الأدمن

```bash
python manage.py createsuperuser
```

### 7. تشغيل الخادم

```bash
python manage.py runserver
```

الخادم سيعمل على: `http://localhost:8000`

## 📊 APIs المتاحة

### الأقسام
- `GET /departments/api/departments/` - عرض جميع الأقسام
- `POST /departments/api/departments/` - إضافة قسم جديد
- `GET /departments/api/departments/{id}/` - عرض قسم محدد
- `PUT /departments/api/departments/{id}/` - تحديث قسم
- `DELETE /departments/api/departments/{id}/` - حذف قسم

### المراحل
- `GET /departments/api/stages/` - عرض جميع المراحل
- `POST /departments/api/stages/` - إضافة مرحلة جديدة
- `GET /departments/api/stages/{id}/` - عرض مرحلة محددة
- `PUT /departments/api/stages/{id}/` - تحديث مرحلة
- `DELETE /departments/api/stages/{id}/` - حذف مرحلة

### الشعب
- `GET /departments/api/branches/` - عرض جميع الشعب
- `POST /departments/api/branches/` - إضافة شعبة جديدة
- `GET /departments/api/branches/{id}/` - عرض شعبة محددة
- `PUT /departments/api/branches/{id}/` - تحديث شعبة
- `DELETE /departments/api/branches/{id}/` - حذف شعبة

### المستخدمين
- `GET /users/api/users/` - عرض جميع المستخدمين
- `POST /users/api/users/` - إضافة مستخدم جديد
- `GET /users/api/users/{id}/` - عرض مستخدم محدد
- `PUT /users/api/users/{id}/` - تحديث مستخدم
- `DELETE /users/api/users/{id}/` - حذف مستخدم

### ملفات الوجه
- `GET /users/api/face-profiles/` - عرض جميع ملفات الوجه
- `POST /users/api/face-profiles/` - إضافة ملف وجه جديد
- `GET /users/api/face-profiles/{id}/` - عرض ملف وجه محدد
- `PUT /users/api/face-profiles/{id}/` - تحديث ملف وجه
- `DELETE /users/api/face-profiles/{id}/` - حذف ملف وجه

### الحضور
- `GET /attendance/api/attendance/` - عرض جميع سجلات الحضور
- `POST /attendance/api/attendance/` - تسجيل حضور جديد
- `GET /attendance/api/attendance/{id}/` - عرض سجل حضور محدد
- `PUT /attendance/api/attendance/{id}/` - تحديث سجل حضور
- `DELETE /attendance/api/attendance/{id}/` - حذف سجل حضور

### الجدول الدراسي
- `GET /attendance/api/schedule/` - عرض الجدول الدراسي
- `POST /attendance/api/schedule/` - إضافة محاضرة جديدة
- `GET /attendance/api/schedule/{id}/` - عرض محاضرة محددة
- `PUT /attendance/api/schedule/{id}/` - تحديث محاضرة
- `DELETE /attendance/api/schedule/{id}/` - حذف محاضرة

## 🔐 لوحة الإدارة

يمكنك الوصول إلى لوحة إدارة Django على:
`http://localhost:8000/admin`

## 📦 هيكل المشروع

```
Django/
├── departments/          # تطبيق الأقسام والمراحل والشعب
├── users/               # تطبيق المستخدمين وملفات الوجه
├── attendance/          # تطبيق الحضور والجدول الدراسي
├── muq_system/         # إعدادات المشروع الرئيسية
├── venv/               # البيئة الافتراضية
├── requirements.txt    # الحزم المطلوبة
└── .env.example       # نموذج ملف البيئة
```

## ⚙️ الإعدادات

### CORS
تم تفعيل CORS للسماح بالاتصال من الواجهة الأمامية.

### قاعدة البيانات
يستخدم Django MySQL كقاعدة بيانات رئيسية.

## 🧪 الاختبار

```bash
python manage.py test
```

## 📝 ملاحظات

- تأكد من تشغيل MySQL قبل تشغيل الخادم
- تأكد من إنشاء قاعدة البيانات قبل تشغيل الترحيلات
- يمكنك تغيير المنفذ (port) باستخدام: `python manage.py runserver 8080`
