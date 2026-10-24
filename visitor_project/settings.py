"""Settings for the educational visitor accounting web application."""

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "development-only-change-in-production"
DEBUG = True
ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1", "testserver"]

# PZ5-PZ6 intentionally use the JSON storage and classes from practical work 3.
# Database models, authentication and Django forms are not introduced yet.
INSTALLED_APPS = ["django.contrib.staticfiles", "webapp"]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "visitor_project.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": []},
    },
]
WSGI_APPLICATION = "visitor_project.wsgi.application"

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
