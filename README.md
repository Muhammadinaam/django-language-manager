

# Language Manager 🌍

**A plug-and-play Django app for multilingual websites with RTL support**

## Features ✨

✅ **URL-based language switching** (`/en/`, `/ar/`, `/es/`)  
✅ **RTL (Right-to-Left) support** for Arabic, Urdu, etc.  
✅ **API language detection** via HTTP headers  
✅ **Simple template tags** for language switching  
✅ **Windows-friendly** translation compiler (no gettext needed!)  
✅ **Industry-standard** architecture (like LinkedIn, Facebook)  
✅ **SEO-optimized** with unique URLs per language  
✅ **Cookie persistence** remembers user preference  

---

## Quick Install 🚀

### 1. Install the App

Install directly from GitHub:

```bash
pip install git+https://github.com/yourusername/django-language-manager.git
```

This will also install the required dependency (`polib`).

Or if you have the source code, copy the `language_manager` folder to your project and install dependencies manually:

```bash
pip install polib
```

### 2. Configure Settings

Edit your `settings.py`:

```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ... other apps
    'language_manager',  # Add this
]

# Add middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Add this (for web)
    'language_manager.middleware.APILanguageMiddleware',  # Add this (for API)
    # ... rest of middleware
]

# Configure languages
LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', 'English'),
    ('es', 'Español'),
    ('fr', 'Français'),
    ('de', 'Deutsch'),
    ('ar', 'العربية'),  # RTL
    ('ur', 'اردو'),      # RTL
]

# RTL languages (used in templates for layout)
RTL_LANGUAGES = ['ar', 'ur']

# Locale paths for translation files
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Note: Language cookie settings use Django's defaults (no need to configure)

# Add context processor
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                # ... other processors
                'django.template.context_processors.i18n',  # Add this
                'language_manager.context_processors.rtl_support',  # Add this
            ],
        },
    },
]
```

### 3. Configure URLs

Edit your main `urls.py`:

```python
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView
from language_manager.views import set_language

# Non-translatable URLs (no language prefix)
urlpatterns = [
    path('api/', include('your_api_urls')),  # API uses headers
    path('i18n/setlang/', set_language, name='set_language'),  # Language switcher
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/en/', permanent=False)),  # Redirect to default
]

# Translatable URLs (with language prefix: /en/, /ar/, etc.)
urlpatterns += i18n_patterns(
    path('', your_views.home, name='home'),
    path('about/', your_views.about, name='about'),
    # ... your app URLs
    prefix_default_language=True,  # Include prefix for default language too
)
```

### 4. Optional: Enable Jazzmin Language Selector

If using Jazzmin admin theme, add to your settings:

```python
JAZZMIN_SETTINGS = {
    # ... your other settings
    "language_chooser": True,  # Enables language dropdown in admin navbar
}
```

### 5. Update Base Template

In your `base.html` or main template:

```html
{% load static %}{% load i18n %}
<!DOCTYPE html>
<html lang="{{ LANGUAGE_CODE|default:'en' }}" 
      dir="{% if LANGUAGE_CODE in RTL_LANGUAGES %}rtl{% else %}ltr{% endif %}">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}My Site{% endblock %}</title>
    
    <!-- Load RTL or LTR Bootstrap CSS -->
    {% if LANGUAGE_CODE in RTL_LANGUAGES %}
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    {% else %}
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    {% endif %}
</head>
<body>
    <!-- Language Switcher Example -->
    <nav>
        <ul class="dropdown-menu">
            {% load language_tags %}
            {% get_current_language as LANGUAGE_CODE %}
            
            <li><a href="{% change_language_url 'en' %}">English</a></li>
            <li><a href="{% change_language_url 'es' %}">Español</a></li>
            <li><a href="{% change_language_url 'ar' %}">العربية</a></li>
        </ul>
    </nav>
    
    {% block content %}{% endblock %}
</body>
</html>
```

---

## Usage 📖

### Creating Translation Files

1. **Create directory structure:**
```bash
mkdir -p locale/ur/LC_MESSAGES
```

2. **Create `locale/ur/LC_MESSAGES/django.po`:**
```po
msgid ""
msgstr ""
"Project-Id-Version: 1.0\n"
"Language: ur\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"

msgid "Welcome"
msgstr "خوش آمدید"

msgid "Home"
msgstr "ہوم"

msgid "About"
msgstr "کے بارے میں"
```

### Compiling Translations

**Use the management command:**
```bash
python manage.py compiletranslations
```

Output:
```
📂 Scanning: /path/to/locale
✅ Compiled: locale/ur/LC_MESSAGES/django.po → locale/ur/LC_MESSAGES/django.mo
🎉 Successfully compiled 1 translation file(s)!
⚠️  Please restart the Django server for changes to take effect.
```

### Testing

1. Start server: `python manage.py runserver`
2. Visit: `http://localhost:8000/en/` (English)
3. Visit: `http://localhost:8000/ur/` (Urdu with RTL!)
4. Visit: `http://localhost:8000/ar/` (Arabic with RTL!)

---

## Template Usage 🎨

### Language Switcher Dropdown

```html
{% load language_tags %}
{% get_current_language as LANGUAGE_CODE %}

<div class="dropdown">
    <button class="dropdown-toggle">
        🌐 Language
    </button>
    <ul class="dropdown-menu">
        <li>
            <a href="{% change_language_url 'en' %}">
                {% if LANGUAGE_CODE == 'en' %}✓{% endif %} English
            </a>
        </li>
        <li>
            <a href="{% change_language_url 'ar' %}">
                {% if LANGUAGE_CODE == 'ar' %}✓{% endif %} العربية
            </a>
        </li>
        <li>
            <a href="{% change_language_url 'ur' %}">
                {% if LANGUAGE_CODE == 'ur' %}✓{% endif %} اردو
            </a>
        </li>
    </ul>
</div>
```

### Translatable Strings

```html
{% load i18n %}

<h1>{% trans "Welcome to our site" %}</h1>
<p>{% trans "Browse our products" %}</p>
<button>{% trans "Get Started" %}</button>
```

### Checking RTL

```html
{% if LANGUAGE_CODE in RTL_LANGUAGES %}
    <!-- RTL-specific content -->
    <div class="text-right">مرحبا</div>
{% else %}
    <!-- LTR content -->
    <div class="text-left">Hello</div>
{% endif %}
```

---

## API Usage 📱

For mobile apps and API clients:

### Request with Language Header

```javascript
// React Native / Flutter / JavaScript
fetch('https://yoursite.com/api/endpoint/', {
    headers: {
        'X-Language': 'ar',  // Custom header
        'Accept-Language': 'ar',  // Standard header
        'Authorization': 'Bearer token...'
    }
})
```

### Python Requests

```python
import requests

response = requests.get(
    'https://yoursite.com/api/endpoint/',
    headers={
        'X-Language': 'ur',
        'Accept-Language': 'ur'
    }
)
```

The API will return content in the requested language!

---

## File Structure 📁

```
language_manager/
├── __init__.py
├── apps.py
├── views.py                    # set_language view
├── middleware.py               # APILanguageMiddleware
├── context_processors.py       # rtl_support
├── templatetags/
│   ├── __init__.py
│   └── language_tags.py        # change_language_url tag
├── management/
│   └── commands/
│       └── compiletranslations.py  # Compile command
└── README.md                   # This file
```

---

## How It Works 🔍

### URL-Based Language Detection

```
User visits: /ar/products/
          ↓
Django LocaleMiddleware detects: 'ar' from URL
          ↓
Sets: LANGUAGE_CODE = 'ar'
          ↓
Template loads Arabic translations
          ↓
Bootstrap RTL CSS loads automatically
          ↓
Page displays in Arabic (right-to-left)
```

### Language Priority

1. **URL prefix** → `/ar/` sets Arabic
2. **Cookie** → `django_language=ar`
3. **Session** → `_language=ar`
4. **Accept-Language header** (API only)
5. **Default** → `LANGUAGE_CODE` from settings

---

## Common Tasks 🛠️

### Add a New Language

1. **Add to settings.py:**
```python
LANGUAGES = [
    # ... existing languages
    ('hi', 'हिन्दी'),  # Hindi
]
```

2. **Create translation file:**
```bash
mkdir -p locale/hi/LC_MESSAGES
# Create locale/hi/LC_MESSAGES/django.po
```

3. **Add translations in .po file**

4. **Compile:**
```bash
python manage.py compiletranslations
```

5. **Restart server**

### Update Existing Translations

1. Edit `.po` file: `locale/ur/LC_MESSAGES/django.po`
2. Compile: `python manage.py compiletranslations`
3. Restart server

### Generate Translation Template

```bash
# Auto-detect translatable strings in templates/code
python manage.py makemessages -l ur --ignore=venv
```

---

## Troubleshooting 🔧

### Translations Not Showing

✅ **Check:** Did you compile? `python manage.py compiletranslations`  
✅ **Check:** Does `.mo` file exist? `locale/ur/LC_MESSAGES/django.mo`  
✅ **Check:** Did you restart server?  
✅ **Check:** Are you on correct URL? `/ur/` not `/en/`  
✅ **Check:** Is string marked for translation? `{% trans "text" %}`  

### Language Switcher Not Working

✅ **Check:** Is `language_manager` in `INSTALLED_APPS`?  
✅ **Check:** Is URL configured? `path('i18n/setlang/', set_language)`  
✅ **Check:** Template loads tags? `{% load language_tags %}`

### RTL Not Working

✅ **Check:** Is language in `RTL_LANGUAGES` list?  
✅ **Check:** Template has `dir` attribute? `dir="{% if LANGUAGE_CODE in RTL_LANGUAGES %}rtl{% else %}ltr{% endif %}"`  
✅ **Check:** RTL CSS loading? Check Bootstrap RTL link  

---

## Why This Architecture? 🏆

### Industry Standard

✅ **LinkedIn**: `linkedin.com/ar/` - URL-based  
✅ **Facebook**: `facebook.com/ar/` - URL-based  
✅ **Wikipedia**: `ar.wikipedia.org/` - Subdomain  
✅ **Google**: `google.com/ar` - URL-based  

### Benefits

✅ **SEO**: Each language has unique, crawlable URLs  
✅ **Mobile Apps**: Stateless, works with REST APIs  
✅ **Shareable**: Links preserve language  
✅ **Professional**: Enterprise-grade solution  
✅ **Scalable**: Handles millions of users  

---

## Requirements 📦

- Django 3.2+
- Python 3.8+
- polib (for compiling translations)

```bash
pip install Django>=3.2 polib
```

---

## Development Workflow 🔧

### For Package Maintainers

If you want to modify or extend this app:

**1. Local Development (Recommended)**
- Keep the app in your Django project root (e.g., `backend/language_manager/`)
- Develop and test as a normal Django app
- Use `'language_manager'` in INSTALLED_APPS
- Import paths are identical to pip-installed version ✨

**2. Publishing Updates**
```bash
# Make changes, test locally
cd language_manager/

# Commit to git
git add .
git commit -m "Add new feature"
git push origin main

# Release new version
git tag -a v1.1.0 -m "Version 1.1.0"
git push origin v1.1.0
```

**3. Installing in Other Projects**
```bash
# Install from GitHub
pip install git+https://github.com/yourusername/django-language-manager.git@v1.1.0

# Use without 'apps.' prefix
INSTALLED_APPS = ['language_manager']
```

**4. Editable Installation (Advanced)**
```bash
# For active cross-project development
pip install -e /path/to/language_manager
```

### Version Management
- **1.0.x** → Bug fixes (patch)
- **1.x.0** → New features (minor)  
- **x.0.0** → Breaking changes (major)

---

## License 📄

Free to use in your projects!

---

## Support 💬

Copy this app to any Django project and it just works!

**Questions?** Check the troubleshooting section above.

---

**Made with ❤️ for the Django community**

