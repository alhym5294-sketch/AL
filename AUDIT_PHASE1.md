# MUQ — تقرير التدقيق الشامل (المرحلة 1)

التاريخ: 2026-10-11 · النطاق: الفحص للقراءة فقط، **لم يُعدَّل ولم يُحذف أي ملف**
مسار النسخة المدقّقة: `C:\Users\moktata\Desktop\MUQ`

---

## 1. ملخص تنفيذي

النظام اليوم **ليس نظاماً مؤسسياً، بل واجهة تجريبية مربوطة بمتصفح واحد**. كل ما يراه المستخدمون محفوظ في `localStorage`، وقاعدة البيانات المركزية — الموجودة فعلاً بكود كامل — **لا يناديها أي صفحة**.

| الطبقة | الحالة الحقيقية |
|---|---|
| `Js/database.js` (localStorage) | **الطبقة الوحيدة المستخدمة فعلياً** في كل الصفحات الحية |
| `python/app.py` (Flask :5000 + MySQL) | مكتمل نسبياً (25 endpoint) لكنه **غير مستدعى** إلا من صفحة ترحيل واحدة |
| `mysql/server.js` (Node :3000 + MySQL) | نسخة مكرّرة قديمة من الـ API، **لا يشير إليها أحد** في الواجهة |
| `Django/` (DRF + PostgreSQL) | هياكل CRUD فقط، **بلا migrations**، بلا مصادقة، بلا اتصال بالواجهة |
| التعرف على الوجه | صفحة واحدة فقط (`face-registration-new.html`) تعمل حقيقياً؛ البوابة والمراقبة **معطّلتان أو وهميتان** |

النتيجة: البيانات المسجلة في متصفح الأدمن لا يراها الطالب، وسجل الحضور يضيع بمسح الـ cache، ولا وجود لسجل تدقيق.

---

## 2. نقاط الدخول وسير العمل الحالي

```
index.html:205 ──► HTML/login.html ──► Js/login.js:47  (تحقق محلي فقط)
                                        │
                     localStorage.currentUser  (Js/login.js:59)
                                        │
   ┌────────────┬───────────┬───────────┼────────────┬──────────────┐
 admin       teacher      student     staff        gate-entry    monitoring
```

- **تسجيل الدخول**: `Js/login.js:47` ينادي `db.authenticateUser()` وهي مقارنة نصية خام داخل `muq_users` (`Js/database.js:254-257`). `POST /api/login` موجود (`Js/database-api.js:35`) **ولا يناديه شيء**.
- **الجلسة**: `localStorage.currentUser` فقط، بلا انتهاء صلاحية، وتبقى كلمة المرور داخل الكائن المخزّن.
- **الصلاحيات**: `checkAuth()` مكتوبة يدوياً في كل لوحة (`admin-dashboard.js:2-14`)، وتنفّذ **بعد** العرض في لوحات المدرس/الطالب/الموظف (`teacher-dashboard.js:27`, `student-dashboard.js:20`, `staff-dashboard.js:22`) → المحتوى المحمي يُرسم ثم يوجَّه. أي شخص يكتب في Console `localStorage.currentUser='{"type":"admin"}'` ويحصل على لوحة الأدمن كاملة.
- **صفحات بلا أي فحص**: `HTML/attendance-report.html` و`HTML/monitoring-system.html` تفتحان مباشرة بدون تسجيل دخول.

---

## 3. واجهات API الموجودة فعلاً

### Flask `python/app.py` (:5000، MySQL عبر SQLAlchemy، `CORS(app)` مفتوح — سطر 11)
`/api/health` (207) · `/api/login` (213-267) · `/api/departments|stages|branches` CRUD (271-470) · `/api/students|teachers` CRUD (474-651) · `/api/staff/<type>` CRUD (655-772) · `/api/schedule` (776-841) · `/api/attendance` GET/POST/PUT (845-907) · `/api/staff-attendance` (911-977) · `/api/face-profiles` (981-1070) · `/api/face-recognition/recognize` (1074-1148).

**ولا endpoint واحد فيه فحص هوية أو صلاحية** (لا sessions ولا tokens ولا decorators في الملف).

### Node `mysql/server.js` (:3000)
نفس الأشكال تقريباً (health 38، login 45، CRUD 95-721) **بدون** نقاط الوجه. معطوب بنيوياً: `staff-attendance` و`login` لأنواع security/service يعملان `JOIN administrative_staff` فقط (`server.js:670-674`, `:67-74`) فتسقط بقية الفئات.

### Django (:8000)
`/users/api/users/`، `/users/api/face-profiles/`، `/attendance/api/{attendance,schedule}/`، `/departments/api/{departments,stages,branches}/` — ثمانية مسارات `ModelViewSet` كاملة الحذف/التعديل، **بلا `authentication_classes` ولا `permission_classes` ولا فلترة ولا pagination** (`users/views.py:5-11`, `attendance/views.py:5-11`, `departments/views.py:5-15`). المسارات **لا تطابق** ما تطلبه الواجهة (`/api/students`, `/api/login`, …)، والمنفذ مختلف (8000 مقابل 5000).

---

## 4. قواعد البيانات: ثلاثة مخططات متعارضة

| | المحرك | جداول الوجه | ملاحظات |
|---|---|---|---|
| `python/database.sql` | MySQL `muq_system` | ✅ `face_profiles` + `face_samples` (183-205) | بلا قيد `UNIQUE(person_type, person_id)` → ملفات مكرّرة ممكنة |
| `mysql/database.sql` | MySQL `muq_system` | ❌ لا يوجد | `staff_attendance.staff_id → administrative_staff` بـ FK (180) يخالف نسخة Flask |
| Django `settings.py:85-93` | **PostgreSQL** بكلمة مرور فارغة | لا جداول — `migrations/` فيها `__init__.py` بحجم 0 فقط | `db.create_all()` في Flask (202-203) يتجاوز ملفات SQL أصلاً |

نسخ `User` في كل طبقة different: Flask يوازي `students/teachers/*_staff` بصف `users` (512-520, 603-611, 708-717) — مصدر حقيقة مزدوج داخل نفس القاعدة. Django `User.department` نص حر بلا FK (`users/models.py:18`)، و`Attendance` فيه `unique_together(person, date)` (`attendance/models.py:22`) **يمنع أكثر من حدث بوابة في اليوم** — وهو مناقض لمتطلب الدخول/الخروج.

**غير موجود في أي طبقة**: جداول الأجهزة/البوابات، سجل التدقيق (grep repo-wide لكلمة audit: صفر نتائج)، اتجاه المرور، التأخير/الاستئذان، طابور مزامنة عند انقطاع الشبكة.

---

## 5. محرك التعرف على الوجه: الحقيقي مقابل الوهم

| الصفحة | face-api محمّل؟ | الحقيقة |
|---|---|---|
| `face-registration-new.html` | ✅ سطر 368 (jsdelivr) | المسار الحقيقي الوحيد: استخراج 128-dim descriptor |
| `gate-entry.html` | ❌ | `faceapi` غير معرّف + ينادي دوال **غير موجودة**: `faceEngine.extractEmbedding` (397) و`faceStorage.recognizePerson` (405؛ الاسم الصحيح `detectFace`/`recognizeFace` في `face-storage.js:128`) → البوابة ميتة 100% |
| `student|teacher|staff-face-registration-new.html` | ❌ | **تولّد سمات عشوائية**: `Array(128).map(() => Math.random())` (`student…:343`, `teacher…:343`, `staff…:374`) — ملفات مسمومة لا تطابق وجهاً أبداً |
| `monitoring-system.html` | ❌ | الكاميرا تعمل و`setInterval` يطبع `console.log` مع تعليق «محاكاة … AI» (396-400)؛ التنبيهات أزرار يدوية في مصفوفة ذاكرة (416-436) |
| `face-registration.html` / `staff-face-registration.html` (قديم) | ❌ | يخزّن صور base64 في localStorage (`face-registration.js:70-71, 120-123`) |
| `teacher-dashboard.html:175` / `staff-dashboard.html:103` | ❌ | يحمّلان `face-recognition.js` الذي يفشل عند التحميل (`:7` يشير إلى `faceEngine` غير معرّف، و`:32` `new FaceRecognition()`) ثم تنادى `faceRecognition.verifyIdentity` (`teacher-dashboard.js:268, 354`) |

**النماذج من CDN شخصي**: `face-config.js:39` → `justadudewhohacks.github.io` (صفحات شخص، لا SRI ولا تثبيت ملكية). لا weights مودعة في المستودع (بحث عن `models/` و`*-weights_manifest.json`: صفر). لو تعطل المصدر أو انقطع إنترنت الجامعة يتوقف النظام، و`gate-entry.html:338` **يتجاهل** القيمة المرجعة من `loadModels()` فيدخل حلقة «لا وجه».

**التحقق من الحيوية**: عتبة «رمش» بمقياس ارتفاع عين **10 بكسل** وعدّة إطارات (`face-recognition-engine.js:303-340`) — تعتمد على الدقة، و**غير مفروضة**: عند الفشل يقول «لم يتم اكتشاف الرمش» ثم «السماح بالحفظ حتى بدون الرمش» (`face-registration-new.js:368-372`). صورة مطبوعة تعبر بتخطي التحدي. لا يوجد أي anti-spoofing (نسيج/moiré/عمق/تحدي عشوائي).

**العتبات غير معايرة**: `THRESHOLD: 0.6` بتعليق صريح «قيمة تجريبية، تحتاج للاختبار» (`face-config.js:31`)، والخادم يقبل عتبة **يرسلها العميل** مع افتراض 0.6 (`app.py:1105`). «نسبة الثقة» خطية مفبركة `1 - dist/threshold` (`engine.js:434`, `app.py:1130`) — ليست احتمالاً إحصائياً. **مجلدات `dataset/` و`CCTV-Exam -Monitor -Dataset` لم تعد داخل المشروع** (نُقلت إلى سطح المكتب 2026-10-11 11:42)، ولا يوجد في المستودع أي كود تقييم دقة يشير إليها.

**إصدار النموذج**: العمود موجود (`app.py:184`) لكن العميل يرسل **اسم** النموذج لا إصداره (`face-storage.js:30`)، و`recognize` **لا يقارنه إطلاقاً** (`app.py:1074-1131`) → سمات من نماذج مختلفة تُقارن مع بعضها بصمت.

---

## 6. الأمان والخصوصية

1. كلمات مرور **نص خام** في كل الطبقات: `Django/users/models.py:13`، `app.py:26-32`، مقارنة خام `app.py:226-244` و`server.js:56-76`، ونقلها JSON فوق HTTP (`database-api.js:36-40`).
2. حساب أدمن افتراضي `admin/12345` مثبّت في الكود والملفات SQL: `app.py:1155-1159`، `python/database.sql:208-209`، `mysql/database.sql:184-185`، `Js/database.js:12-13` — **وموثّق علناً في README.md:8**.
3. كلمات مرور الموظفين تُعرض **مقروءة** في جدول لوحة الأدمن (`admin-dashboard.js:883`) ومعبّأة في نماذج التعديل (`:841, 917, 1022, 1108`).
4. `SECRET_KEY` مكتوب في `settings.py:23`، `DEBUG=True` (:26)، `ALLOWED_HOSTS=['*']` (:28)، `CORS_ALLOW_ALL_ORIGINS=True` (:31). ملف `.env.example` موجود و`python-dotenv` مثبّت في `requirements.txt:5` — **ولا شيء يستورد dotenv**، فالمتغيرات حبر على ورق.
5. سمات بيومترية تُسلَّم لأي قارئ: `face_data` تُرجع في `/api/login` وGET العام (`app.py:254, 488`)، بلا تقييد عرض أو حذف أو سياسة احتفاظ.
6. لا سجل تدقيق لكل تعديل يدوي: `PUT /api/attendance/:id` يغيّر الحالة بلا تسجيل فاعل (`app.py:897-907`, `server.js:653-663`).

---

## 7. أخطاء تكسر النظام اليوم (مرتّبة)

1. **نظام الطلاب معطوب كلياً**: `getStudents()` معرّفة `async` (`database.js:129`) وتُنادى **بلا await** في 12+ مكان داخلي (`:138, 149, 160, 260, 285-319`) وخارجي (`admin-dashboard.js:62, 88, 297, 427, 505, 642, 700, 785`; `teacher-dashboard.js:90, 173, 175`; `attendance-report.js:18, 77, 335`) → كل عملية ترجع Promise، فالقوائم والحضور والتقارير تفشل. (أيضاً `:131` يشير إلى `dbAPI` غير محمّل في `database.js`.)
2. **حضور البوابة يضيع بصمت**: `gate-entry.html:492` ينادي `db.saveAttendance()` وهي **غير موجودة** (`database.js` فيه `addAttendance` فقط)، والاستثناء يبتلعانه `catch` في `:495-497`.
3. **الخادم لا يُستخدم**: `database-api.js` يُحمَّل في `migrate-to-mysql.html:93` وحدها. كل اللوحات تعمل على `database.js` (`admin-dashboard.html:635`, `teacher…:174`, `student…:116`, `staff…:102`).
4. **مساران متوازيان لتسجيل الوجه**: الأدمن يربط القديم (`admin-dashboard.js:1231, 864`) والمنافذ تربط `-new` (`login.js:12, 17`, `portal-auth.js:5`) — أحدهما base64 والآخر descriptors.
5. **`GET /api/face-profiles/...` لا يُرجع `embedding`** (`app.py:1005-1010`) بينما `face-storage.js:88` يقرأ `s.embedding` → undefined، فكل تحقق هوية لاحق فاشل.
6. **حقل الجودة مختلف الاسم**: العميل يرسل `quality` (`engine.js:274`) والخادم يقرأ `quality_score` (`app.py:1035`) → تُخزَّن 0.0 دائماً.
7. **`POST /api/face-profiles` يعمل INSERT دائماً** (`app.py:1019-1026`) بلا upsert → إعادة التسجيل تضاعف الملفات للأبد.
8. **تقارير الموظفين فارغة دائماً**: تعتمد `record.personId` (`attendance-report.js:151, 170, 189`) وهو الحقل الذي تكتبه البوابة فقط — والبوابة معطوبة (#2).
9. **المطابقة O(كل الأشخاص × كل العينات × 128) بحلقة بايثون** مع N+1 استعلام (`app.py:1084-1093`) → غير صالحة على 400 عينة أو مدرسة كاملة.
10. **`localhost:5000` مثبّت** في `face-config.js:10` → لا نشر على شبكة محلية.
11. **PDF غير موجود** رغم أنه مذكور في README كميزة مستقبلية؛ CSV (`attendance-report.js:376-402`) والطباعة (`:404-406`) حقيقيان.
12. **ترحيل غير idempotent**: `Js/data-migration.js` يرسل كل سجل بلا فحص تكرار (حلقات 49-55) فيضاعف الصفوف عند كل تشغيل، **ويتخطى بيانات الوجه و`staff_attendance`**، وينقل كلمات المرور خاماً (`:97, 117, 137`)؛ لكنه **لا يمسح** localStorage (غير مدمّر).

---

## 8. الملفات الميتة/اليتيمة

- HTML بلا أي مرجع: `add-departments.html`، `migrate-to-mysql.html`، `staff-face-registration-new.html`، `student-face-registration-new.html`، `teacher-face-registration-new.html`.
- JS ميت: `data-migration.js` (مرجع واحد لصفحة ترحيل يتيمة)، `database-api.js` (كذلك)، `face-registration.js` + `face-recognition.js` (الصفحات القديمة فقط).
- تكرار CSS: 10 من 17 صفحة تحقن `<style>` مكرّراً فوق `css/style.css` (1387 سطر)، منها إعادة تعريف `@keyframes` في `gate-entry.html:116-124`.
- إيجابي: كل الصفحات الـ17 فيها `lang="ar" dir="rtl"`.

---

## 9. مخاطر بيئة العمل (تقرر قبل أي تعديل)

1. **لا يوجد نظام إصدار للمجلد**: `git rev-parse --show-toplevel` = `C:/Users/moktata`، و`git ls-files` داخل MUQ = **0 ملف متعقَّب**. لا شبكة أمان لاسترجاع أي تعديل.
2. **نسخ متعددة للمشروع**: `MUQ` (68M، المدقَّق هنا) · `MUQ1` (636M، أقدم، فيه مجلد `Al` بدل `HTML`) · `SCHOOL_SYS` (1.8M، 142 ملفاُ عُدّلت في أكتوبر — نظام مدرسة مختلف بواجهة ثابتة) · `MUQ.zip` (23M، أُنشئ 11:44) · `MUQ (5).zip` (1.3G، 29 سبتمبر).
3. مجلدات العينات أُخرجت من المشروع اليوم 11:42 → **لا بيانات اختبار لتسوية العتبة** داخل المستودع.
4. `Django/venv` داخل المجلد (سبب الـ 68M) مع `psycopg2-binary 2.9.13` المثبّت مقابل `2.9.9` المطلوب.

## 10. ما لم أتحقق منه (unverified)

- هل `python manage.py check` ينجو فعلاً (لم أنفّذ أوامر على الـ venv في هذه المرحلة)، وهل توجد قاعدة PostgreSQL أو MySQL حيّة على الجهاز.
- هل القوائم المنسدلة في لوحات المدرس/الطالب تعمل بعد الخطأ #1 أو تظهر فارغة (استنتاج من الكود، لم يُختبر في متصفح).
- دقة face-api الفعلية على كاميرات الموقع والإضاءة الحقيقية.
- هل jsdelivr كان متاحاً يوم التسجيل في أجهزة الجامعة.

---

## 11. الخطوة التالية المقترحة (المرحلة 2)

بترتيب يعتمد على بعضه:

0. **نسخة احتياطية** من `MUQ/` (باستثناء `venv`) + `init git` داخل المجلد نفسه، قبل أي تعديل.
1. **قرار مصدر الحقيقة**: توحيد على Django/DRF مع PostgreSQL، ورحيل `python/app.py` منطقياً إليه، وطيّة `mysql/server.js` في مجلد `archive/` (نقل، لا حذف).
2. **مصادقة حقيقية**: `AUTH_USER_MODEL` + JWT/Sessions + `make_password` + صلاحيات DRF لكل ViewSet + إزالة الأدمن الافتراضي و`README.md:8`، وربط `FACE_CONFIG.STORAGE.API_URL` بمتغير بيئة.
3. **ربط الواجهات**: استبدال طبقة `database.js` في كل لوحة باستدعاءات API، مع إصلاح #1 (async) و#5/#6/#7 (أسماء الحقول والمسارات) — وبعدها تعمل صفحات الطلاب فعلياً.
4. **ترحيل آمن**: جعل `data-migration.js` idempotent (مفتاح طبيعي + فحص وجود) وشاملاً لبيانات الوجه، مع تقرير متحقَّق منه قبل/بعد.
