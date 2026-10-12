# MUQ نظام توثيق نظام MySQL Backend

## المتطلبات

- Node.js (الإصدار 14 أو أحدث)
- MySQL (الإصدار 5.7 أو أحدث)
- npm أو yarn

## التثبيت

### 1. تثبيت الاعتماديات

```bash
cd mysql
npm install
```

### 2. إعداد قاعدة البيانات

#### إنشاء قاعدة البيانات:
```bash
mysql -u root -p
```

```sql
CREATE DATABASE muq_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

#### استيراد البنية:
```bash
mysql -u root -p muq_system < database.sql
```

### 3. إعداد ملف التكوين

```bash
cp .env.example .env
```

عدل ملف `.env` بإعدادات قاعدة البيانات الخاصة بك:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=muq_system
PORT=3000
```

### 4. تشغيل الخادم

#### التشغيل العادي:
```bash
npm start
```

#### التشغيل مع التطوير التلقائي (dev mode):
```bash
npm run dev
```

## واجهة API

### المصادقة
- `POST /api/login` - تسجيل الدخول

### الأقسام
- `GET /api/departments` - جلب جميع الأقسام
- `POST /api/departments` - إضافة قسم جديد
- `PUT /api/departments/:id` - تعديل قسم
- `DELETE /api/departments/:id` - حذف قسم

### المراحل
- `GET /api/stages` - جلب جميع المراحل
- `GET /api/stages?department_id=X` - جلب مراحل قسم معين
- `POST /api/stages` - إضافة مرحلة جديدة
- `PUT /api/stages/:id` - تعديل مرحلة
- `DELETE /api/stages/:id` - حذف مرحلة

### الشعب
- `GET /api/branches` - جلب جميع الشعب
- `GET /api/branches?stage_id=X` - جلب شعب مرحلة معينة
- `POST /api/branches` - إضافة شعبة جديدة
- `PUT /api/branches/:id` - تعديل شعبة
- `DELETE /api/branches/:id` - حذف شعبة

### الطلاب
- `GET /api/students` - جلب جميع الطلاب
- `POST /api/students` - إضافة طالب جديد
- `PUT /api/students/:id` - تعديل طالب
- `DELETE /api/students/:id` - حذف طالب

### المدرسين
- `GET /api/teachers` - جلب جميع المدرسين
- `POST /api/teachers` - إضافة مدرس جديد
- `PUT /api/teachers/:id` - تعديل مدرس
- `DELETE /api/teachers/:id` - حذف مدرس

### الموظفين
- `GET /api/staff/:type` - جلب موظفي نوع معين (administrative, security, service)
- `POST /api/staff/:type` - إضافة موظف جديد
- `PUT /api/staff/:type/:id` - تعديل موظف
- `DELETE /api/staff/:type/:id` - حذف موظف

### الجدول الدراسي
- `GET /api/schedule` - جلب الجدول الدراسي
- `POST /api/schedule` - إضافة محاضرة جديدة
- `PUT /api/schedule/:id` - تعديل محاضرة
- `DELETE /api/schedule/:id` - حذف محاضرة

### الحضور
- `GET /api/attendance` - جلب سجل الحضور
- `POST /api/attendance` - تسجيل حضور جديد
- `PUT /api/attendance/:id` - تحديث حالة الحضور

### حضور الموظفين
- `GET /api/staff-attendance` - جلب سجل حضور الموظفين
- `POST /api/staff-attendance` - تسجيل حضور موظف

## التكامل مع الواجهة الأمامية

لتحويل الواجهة الأمامية من localStorage إلى MySQL، تحتاج إلى:

1. استبدال جميع استدعاءات `db.getStudents()` بـ:
```javascript
fetch('http://localhost:3000/api/students')
  .then(response => response.json())
  .then(data => { /* استخدام البيانات */ });
```

2. استبدال عمليات الحفظ بـ:
```javascript
fetch('http://localhost:3000/api/students', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(studentData)
})
```

3. تحديث نظام تسجيل الدخول لاستخدام API بدلاً من localStorage

## ملاحظات هامة

- تأكد من تشغيل MySQL قبل تشغيل الخادم
- البيانات القديمة في localStorage لن تنتقل تلقائياً
- تحتاج إلى إنشاء سكريبت ترحيل البيانات من localStorage إلى MySQL
- تأكد من صلاحيات MySQL للمستخدم
