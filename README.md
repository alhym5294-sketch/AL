# نظام MUQ - نظام تسجيل الحضور بالتعرف على الوجوه

نظام متطور لتسجيل حضور الطلاب باستخدام تقنية التعرف على الوجوه، مع لوحات تحكم شاملة للأدمن والمدرسين والطلاب.

## 📁 هيكل المشروع

```
MUQ/
├── backend/              # Django REST Framework Backend
│   ├── attendance/       # Attendance & Schedule models
│   ├── departments/      # Department, Stage, Branch models
│   ├── users/           # User & FaceProfile models
│   ├── muq_system/      # Django project settings
│   ├── manage.py        # Django management script
│   ├── requirements.txt # Python dependencies
│   ├── Procfile         # Railway deployment config
│   ├── railway.json     # Railway project config
│   ├── .env.example     # Environment variables template
│   ├── DEPLOYMENT.md    # Deployment guide
│   └── README.md        # Backend documentation
│
├── frontend/            # Vanilla JavaScript Frontend
│   ├── HTML/           # HTML pages
│   ├── Js/             # JavaScript modules
│   ├── css/            # Stylesheets
│   ├── index.html      # Entry point
│   └── README.md       # Frontend documentation
│
├── _backups/           # Archived Flask & Node.js backups
│   ├── flask/          # Old Flask backend
│   └── nodejs/         # Old Node.js backend
│
├── AUDIT_PHASE1.md     # Initial audit report
└── README.md           # This file
```

## 🚀 البدء السريع

### Backend (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py create_superuser
python manage.py runserver
```

Backend سيكون متاح على `http://localhost:8000/api/`

### Frontend

```bash
cd frontend
# Option 1: Open index.html directly in browser
# Option 2: Use a local server
python -m http.server 8010
```

Frontend سيكون متاح على `http://localhost:8010`

## 🌐 النشر

### Backend على Railway

راجع [backend/DEPLOYMENT.md](backend/DEPLOYMENT.md) للتعليمات التفصيلية.

### Frontend على Netlify/Vercel

1. Connect your Git repository
2. Set publish directory to `frontend`
3. Deploy

## المميزات

### للأدمن
- تسجيل الدخول (المشرف الأعلى)
- إدارة الطلاب (إضافة، تعديل، حذف) مع تحديد المادة والمرحلة والشعبة
- إدارة المدرسين (إضافة، تعديل، حذف) مع تحديد المادة والمرحلة والشعبة
- إدارة الموظفين (إداريين، أمنيين، خدمة)
- تسجيل بيانات الوجه للطلاب والمدرسين والموظفين
- إنشاء الجداول الدراسية حسب المادة والمرحلة والشعبة
- عرض الإحصائيات والتقارير

## كيفية الاستخدام

### 1. إعداد المشرف الأعلى (مرة واحدة فقط)
```bash
cd backend
python manage.py create_superuser
```
أدخل اسم المستخدم وكلمة المرور الجديدة
هذا الحساب سيكون له صلاحيات المشرف الأعلى

### 2. تشغيل النظام محلياً

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd frontend
python -m http.server 8010
```

### 3. تسجيل الدخول
- افتح المتصفح على `http://localhost:8010`
- استخدم اسم المستخدم وكلمة المرور التي أنشأتها
- سيتم تحديد نوع المستخدم تلقائياً بناءً على الصلاحيات

### للمدرسين
- عرض الجدول الدراسي حسب المادة والمرحلة الخاصة بهم
- تسجيل الحضور باستخدام التعرف على الوجه الحقيقي
- تسجيل حضور الطلاب عبر الكاميرا مع مقارنة الوجوه
- تأكيد نهاية المحاضرة بالتصوير
- عرض سجل الحضور التفصيلي

### للطلاب
- عرض سجل الحضور الشخصي
- عرض الجدول الدراسي حسب المادتهم ومرحلتهم
- عرض الإحصائيات الشاملة
- عرض الملف الشخصي
- الوصول لتقرير الحضور والغياب الشامل

### للموظفين (إداريين، أمنيين، خدمة)
- تسجيل الحضور اليومي باستخدام التعرف على الوجه
- عرض سجل الحضور الشخصي
- عرض الإحصائيات الشاملة
- عرض الملف الشخصي

## التقنيات المستخدمة

### Backend
- Django 5.1.1
- Django REST Framework 3.15.2
- Django REST Framework SimpleJWT 5.3.1
- PostgreSQL
- Gunicorn
- Whitenoise

### Frontend
- HTML5
- CSS3
- JavaScript (Vanilla)
- WebRTC (Camera access)
- face-api.js (Face recognition)
- JWT Authentication

## المميزات الأمنية

- JWT authentication مع token refresh
- Token blacklisting عند تسجيل الخروج
- تشفير كلمات المرور
- CORS configuration
- Session security
- HSTS و SSL redirect في الإنتاج

## الدعم

- [Backend Documentation](backend/README.md)
- [Frontend Documentation](frontend/README.md)
- [Deployment Guide](backend/DEPLOYMENT.md)
- [Initial Audit Report](AUDIT_PHASE1.md)

لأي استفسارات أو مشاكل، يرجى التواصل مع فريق الدعم الفني.

## License

Proprietary - MUQ System