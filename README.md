# Core CMS – Django Dynamic Company Website

Core CMS هو مشروع Django معمول كـ **مكتبة / Base CMS**
تقدري تستخدميه في أي مشروع موقع شركة (Corporate Website)
وكل حاجة فيه **Dynamic من الأدمن** (Pages – Services – Projects – Blog – Contact – Settings).

---

## 🚀 Features

- Dynamic Pages (Home, About, etc.)
- Services Module
- Projects Module
- Blog Module
- Contact Form (Messages stored in Admin)
- Global Site Settings (Logo, Colors, Social Links, Language)
- Multi-language support (Arabic / English)
- Rich Text Editor (CKEditor)
- Clean Admin UI (Jazzmin – Optional)
- Ready to plug with any HTML Template

---

## 📁 Project Structure

core_cms/
│
├── core_cms/ # Main project settings
│
├── core/ # Site settings (SiteSettings model)
│
├── pages/ # Pages app (Home, About, etc.)
├── services/ # Services app
├── projects/ # Projects app
├── blog/ # Blog / Posts app
├── contact/ # Contact messages app
│
├── templates/ # Global templates
├── static/ # Static files (CSS, JS, Images)
├── staticfiles/ # Collected static files
│
├── env/ # Virtual environment
├── manage.py
└── README.md



---

## 🧰 Used Technologies & Libraries

- Python 3.12+
- Django 6.0.1
- django-ckeditor
- django-modeltranslation
- django-jazzmin
- Pillow

---

## 📦 Requirements

```txt
Django==6.0.1
django-ckeditor==6.7.3
django-modeltranslation==0.19.19
django-jazzmin==3.0.1
Pillow



⚙️ Installation Steps
1️⃣   Clone the project

    - git clone https://github.com/your-username/core-cms.git
    - cd core-cms

2️⃣   Create & activate virtual environment
    - python -m venv env
    - source env/bin/activate  # Linux / Mac
    - env\Scripts\activate     # Windows

3️⃣   Install dependencies
    - pip install -r requirements.txt
    
OR manually:

    - pip install django django-ckeditor django-modeltranslation django-jazzmin pillow

4️⃣   Update settings.py
   -  INSTALLED_APPS = [
            ...
            'jazzmin',
            'ckeditor',
            'ckeditor_uploader',
            'modeltranslation',
        
            'core',
            'pages',
            'services',
            'projects',
            'blog',
            'contact',
        ]
   - CKEDITOR_UPLOAD_PATH = "uploads/"
   - LANGUAGES = (
        ('en', 'English'),
        ('ar', 'Arabic'),
    )
    
    MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
    MODELTRANSLATION_LANGUAGES = ('en', 'ar')
     

5️⃣   Run migrations
    - python manage.py makemigrations
    - python manage.py migrate

6️⃣   Create superuser
    - python manage.py createsuperuser

7️⃣   Run server
    - python manage.py runserver

Admin panel:
    - http://127.0.0.1:8000/admin/



🎨 Site Settings
From Admin → Site Settings you can control:

    * Site name
    
    * Logo & favicon
    
    * Primary & Secondary colors
    
    * Contact info
    
    * Social media links
    
    * Default language
    
    * All available globally in templates via context processor.

🌍 Multi-Language Support

    * Uses django-modeltranslation
    
    * Each model supports Arabic & English
    
    * Language switching supported via Django i18n


📌 Notes

    * This project is designed as a base CMS library
    
    * You can reuse it with any frontend template
    
    * All content is editable from admin without code changes


👩‍💻 Author
    Built with ❤️ using Django
    By: Enas Mohamed


📄 License
    Free to use for personal and commercial projects.




