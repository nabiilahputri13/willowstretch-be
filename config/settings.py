import os
import sys
from datetime import timedelta
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
load_dotenv(BASE_DIR / ".env")

# --- SETTINGS LOGIC UNTUK TESTING ---
IS_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"
IS_TESTING = "test" in sys.argv or any("pytest" in arg for arg in sys.argv)
# ------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

# SECRET_KEY = os.getenv("SECRET_KEY")
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-kunci-rahasia-buat-local-aja"
)
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set")

# DEBUG = os.getenv("DEBUG") == "True"
DEBUG = "RENDER" not in os.environ
# ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",") if not DEBUG else []
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "core",
    "users",
    "classes",
    "pricing",
    "teachers",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --- LOGIKA FINAL: 3 DUNIA (VERCEL, GITHUB, LAPTOP) ---

# Cek variabel lingkungan
IS_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"
IN_VERCEL = os.getenv("VERCEL")

if IS_GITHUB_ACTIONS:
    # 1. KONDISI GITHUB ACTIONS (ROBOT) 🤖
    # Pake SQLite biar test-nya jalan & gak perlu install Postgres
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
elif IN_VERCEL:
    # 2. KONDISI VERCEL (PRODUCTION) 🌍
    # Pake Neon (Pastikan Environment Variable DATABASE_URL sudah di-set di Vercel)
    DATABASES = {
        "default": dj_database_url.config(
            default=os.environ.get("DATABASE_URL"), conn_max_age=600, ssl_require=True
        ) # type: ignore
    }
else:
    # 3. KONDISI LAPTOP NAPUT (LOCAL) 🏠
    # Pake Postgres lokal kamu yang udah ada isinya
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "willowstretch",
            "USER": "willowstretch_user",
            "PASSWORD": "password123",
            "HOST": "localhost",
            "PORT": "5432",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

# --- BAGIAN PENTING YANG DIPERBAIKI ---
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # 1. Agar bisa baca Header 'Authorization: Bearer'
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        # 2. Agar bisa baca Cookie 'access_token'
        "users.authentication.CookieJWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}
# --------------------------------------

AUTH_USER_MODEL = "users.User"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Jakarta"

USE_I18N = True
USE_TZ = True

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
