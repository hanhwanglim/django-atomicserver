from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-ei@r%o6ok%w2ad*yypax2+mve483wjj0zpe9-co!bxmomf3e%7"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "atomicserver",
    "test_app",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "test_project.urls"

WSGI_APPLICATION = "test_project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
