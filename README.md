# Core CMS — موقع شركة ديناميكي (Django)

مشروع **Django** جاهز لمواقع الشركات والعقارات والمحتوى المتعدد: الصفحة الرئيسية، من نحن، المشاريع، الخدمات، المدونة، و**صفحة اتصال بنموذج Django** (حفظ الرسائل في لوحة التحكم وإرسال بريد عند التوفر). الواجهة مبنية على قالب HTML/CSS/JS مع دعم **RTL/LTR**، والمحتوى والألوان والروابط تُدار من **لوحة الإدارة**.

**للنشر:** الملفات الحساسة والميديا وقاعدة SQLite مُدرجة في `.gitignore` حتى لا تُرفع إلى GitHub بالخطأ. على الاستضافة **لا تحذف** مجلد `media/` أو ملف قاعدة البيانات أو ناتج `collectstatic` عند كل تحديث — راجع قسم «النشر» أدناه.

---

## المميزات

- **صفحات ديناميكية:** الرئيسية ومن نحن من تطبيق `core` مع نماذج قابلة للترجمة.
- **المشاريع والخدمات والصفحات:** تطبيقات منفصلة (`projects`, `services`, `pages`).
- **المدونة:** مقالات مع دعم لغة المحتوى.
- **اتصل بنا:** نموذج Django (`/contact/`) — بدون PHP؛ رسائل مخزنة في الأدمن، ويمكن إشعار البريد حسب الإعدادات.
- **إعدادات الموقع:** الشعار، الألوان، بيانات التواصل، واتساب، تضمين خريطة Google، اللغة الافتراضية.
- **ثنائية اللغة (عربي / إنجليزي):** `django-modeltranslation` + `LocaleMiddleware` وزر تبديل اللغة.
- **محرر نصوص:** CKEditor مع رفع صور (عند التفعيل).
- **واجهة أدمن:** Jazzmin.

---

## هيكل المشروع (مختصر)

| المسار | الوظيفة |
|--------|---------|
| `core_cms/` | إعدادات المشروع (`settings`, `urls`) |
| `core/` | إعدادات الموقع، الفوتر، الصفحة الرئيسية، من نحن، صفحة اتصال (نموذج CMS) |
| `projects/` | المشاريع |
| `services/` | الخدمات |
| `pages/` | صفحات إضافية |
| `blog/` | المدونة |
| `contact/` | نموذج الاتصال ورسائل الزوار |
| `templates/` | قوالب Django |
| `static/` | أصول الثيم (CSS/JS/صور المصدر) — **مُ tracked في Git** |
| `staticfiles/` | ملفات ثابتة مجمّعة للإنتاج — **في `.gitignore`** |
| `media/` | ملفات مرفوعة من الأدمن — **في `.gitignore`** |
| `locale/` | ترجمات واجهة `gettext` |
| `requirements.txt` | الاعتماديات |

---

## المتطلبات

- Python 3.12+
- الاعتماديات مذكورة في `requirements.txt` (Django 6، modeltranslation، ckeditor، jazzmin، Pillow، إلخ).

---

## التثبيت والتشغيل محلياً

```bash
git clone <repository-url>
cd Core-Projects
python -m venv env
source env/bin/activate   # Linux/macOS
# env\Scripts\activate    # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- الموقع: `http://127.0.0.1:8000/`
- لوحة التحكم: `http://127.0.0.1:8000/admin/`

بعد تعديل النصوص في القوالب أو الـ Python:

```bash
python manage.py makemessages -l ar
# عدّلي locale/ar/LC_MESSAGES/django.po ثم:
python manage.py compilemessages -l ar
```

---

## النموذج والاتصال (Django وليس PHP)

- صفحة: **`/contact/`**، القالب `templates/contact-us.html`، النموذج ذو المعرف **`site-contact-form`** يرسل POST إلى Django.
- تمت إزالة الاعتماد على **`php/contact.php`** من سكربت الثيم (`static/ltr/js/theme-script.js` و `static/rtl/js/theme-script.js`) حتى لا يُعاد توجيه الإرسال إلى PHP.

---

## `.gitignore` والنشر على الاستضافة

**ما يُستبعد من Git (ومن رفع GitHub):** البيئة الافتراضية، `__pycache__`، ملفات `.env`، **`media/`**، **`*.sqlite3`**، **`staticfiles/`**، سجلات، وملفات IDE.

**كي لا «يُحذف» السيرفر الميديا أو قاعدة البيانات أو الملفات الثابتة عند التحديث:**

1. **لا تستخدم** على السيرفر أوامر مثل `git clean -fdx` أو نشر يمسح المجلد بالكامل ثم يستنسخ من الصفر دون استثناءات.
2. اجعل **`media/`** و**ملف قاعدة البيانات** و**`staticfiles/`** خارج مجلد الاستنساخ، أو استخدم **Volumes / روابط رمزية** بحيث يبقى المحتوى بين عمليات النشر.
3. بعد سحب التحديث من Git: شغّل **`python manage.py migrate`** ثم **`python manage.py collectstatic --noinput`** دون حذف مجلد `media/` يدوياً.
4. للإنتاج: عيّن `DEBUG=False`، `ALLOWED_HOSTS`، مفاتيح آمنة، و**بريد SMTP** (`EMAIL_*` / `DEFAULT_FROM_EMAIL`) إذا اعتمدتَ إشعارات البريد من نموذج الاتصال.

---

## الأمان

لا ترفع `SECRET_KEY` أو كلمات مرور قواعد البيانات إلى المستودع. استخدم متغيرات بيئة أو ملف `.env` محلي (موجود في `.gitignore`) وانسخ القيم على السيرفر بأمان.

---

## الترخيص والمؤلف

يُرخّص استخدام المشروع للأغراض الشخصية والتجارية حسب ما يراه صاحب المشروع.

مبني بـ Django — **Enas Mohamed**.
