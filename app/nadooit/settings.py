# Author: Christoph Backhaus
# Date: 2022-10-30
# Version: 1.0.0
# Description: This is the settings file for the nadooit app. It contains the settings for the app.
# Compatibility: Django 4
# License: TBD

"""
Django settings for nadooit project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Build a path to the .env file
env_path = Path(__file__).resolve().parent.parent.parent / ".env"

# Load the .env file into the environment. This is done before the settings are loaded.
# This is done to make sure that the environment variables are available when the settings are loaded.
# Was required to make the environment variables available in the test_services.py file.
load_dotenv(dotenv_path=env_path)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "changeme")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = bool(int(os.environ.get("DJANGO_DEBUG", 0)))

# The list of allowed hosts is set in the environment variable DJANGO_ALLOWED_HOSTS
# The value is a comma separated list of hosts
# Example: DJANGO_ALLOWED_HOSTS= "localhost, nadooit.de,
ALLOWED_HOSTS = [] if DEBUG else os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")

# Application definition
# This is the list of installed apps. If a new app is added, it must be added here.
# The order of the apps is important. The apps are loaded in the order they are listed here.
# See the documentation of the apps for more information.
INSTALLED_APPS = [
    "sslserver",
    "ordered_model",
    "django_is_url_active_templatetag",
    "grappelli",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "nadooit_auth",
    "nadooit_api_key",
    "nadooit_crm",
    "nadooit_hr",
    "nadooit_time_account",
    "nadooit_workflow",
    "nadooit_network",
    "nadooit_program",
    "nadooit_program_ownership_system",
    "nadooit_api_executions_system.apps.NadooitApiExecutionsSystemConfig",
    "nadooit_website.apps.NadooitWebsiteConfig",
    "nadooit_os",
    "nadooit_key",
    "rest_framework",
    "pwa",
    "django_extensions",
    "mfa",
    "crispy_forms",
    "crispy_bootstrap5",
    "debug_toolbar",
    "django_htmx",
    "nadoo_complaint_management",
    "djmoney",
]

# Middelware is a list of functions that are called for every request.
# The order of the middleware is important. The middleware is called in the order they are listed here.
# A request is processed from top to bottom. A response is processed from bottom to top.
# Add new middelware to process requests and responses.
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

# The Authentication backends are used to authenticate users.
# Multiple backends can be used.
# If one backend fails, the next backend is used.
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "nadooit_auth.custom_user_code_auth_backend.UserCodeBackend",
]

# Configure how templates are loaded.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Staic stettings
STATICFILES_DIRS = [(os.path.join(BASE_DIR, "static")), "/var/www/static/"]

# STATIC_URL = "/static/"
STATIC_URL = "/static/static/"
MEDIA_URL = "/static/media/"


STATIC_ROOT = "/vol/web/static/"
MEDIA_ROOT = "/vol/web/media/"

ROOT_URLCONF = "nadooit.urls"

# The WSGI application is used to serve the application.
# The WSGI application is called by the webserver.
# This is the entry point for the application.
WSGI_APPLICATION = "nadooit.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django_cockroachdb",
        "NAME": os.getenv("COCKROACH_DB_NAME"),
        "USER": os.getenv("COCKROACH_DB_USER"),
        "PASSWORD": os.getenv("COCKROACH_DB_PASSWORD"),
        "HOST": os.getenv("COCKROACH_DB_HOST"),
        "PORT": os.getenv("COCKROACH_DB_PORT"),
        "OPTIONS": {
            "sslmode": "verify-full",
            "options": os.getenv("COCKROACH_DB_OPTIONS"),
        },
    }
}


# Default user model
AUTH_USER_MODEL = "nadooit_auth.User"

# Password validation
CSRF_TRUSTED_ORIGINS = [os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS")]

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
INTERNAL_IPS = [
    "127.0.0.1",
]


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Settings for additional apps

# Settings for Django Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# PWA settings
PWA_SERVICE_WORKER_PATH = os.path.join(
    BASE_DIR, "static", "static", "js", "nadooit_serviceworker.js"
)
PWA_APP_NAME = "NADOOIT"
PWA_APP_DESCRIPTION = "NADOOIT PWA"
PWA_APP_THEME_COLOR = "#000000"
PWA_APP_BACKGROUND_COLOR = "#ffffff"
PWA_APP_DISPLAY = "standalone"
PWA_APP_SCOPE = "/"
PWA_APP_ORIENTATION = "any"
PWA_APP_START_URL = "/nadooit-os"
PWA_APP_STATUS_BAR_COLOR = "default"
PWA_APP_ICONS = [
    {"src": "/static/static/static/appicon/maskable_icon_x192.png", "sizes": "192x192"}
]
PWA_APP_ICONS_APPLE = [
    {"src": "/static/static/static/appicon/maskable_icon_x192.png", "sizes": "192x192"}
]
PWA_APP_SPLASH_SCREEN = [
    {
        "src": "/static/static/splashscreen/nadooit.png",
        "media": "(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)",
    }
]
PWA_APP_DIR = "ltr"
PWA_APP_LANG = "de-DE"


# MFA settings
MFA_UNALLOWED_METHODS = (
    "TOTP",
    "Email",
    "U2F",
    "Trusted_Devices",
    "RECOVERY",
)  # Methods that shouldn't be allowed for the user
MFA_LOGIN_CALLBACK = "nadooit_auth.views.log_user_in"  # A function that should be called by username to login the user in session
MFA_RECHECK = True  # Allow random rechecking of the user
MFA_RECHECK_MIN = 10  # Minimum interval in seconds
MFA_RECHECK_MAX = 30  # Maximum in seconds
MFA_QUICKLOGIN = True  # Allow quick login for returning users by provide only their 2FA
MFA_HIDE_DISABLE = ("",)  # Can the user disable his key (Added in 1.2.0).
MFA_OWNED_BY_ENTERPRISE = False  # Who owns security keys

TOKEN_ISSUER_NAME = "nadooit"  # TOTP Issuer name

if DEBUG:
    U2F_APPID = "https://localhost"  # URL For U2F
    FIDO_SERVER_ID = (
        "localhost"  # Server rp id for FIDO2, it is the full domain of your project
    )
else:
    U2F_APPID = "https://nadooit.de"  # URL For U2F
    FIDO_SERVER_ID = "nadooit.de"

FIDO_SERVER_NAME = "nadooit"
MFA_REDIRECT_AFTER_REGISTRATION = (
    "nadooit_os:nadooit-os"  # Allows Changing the page after successful registeration
)
MFA_SUCCESS_REGISTRATION_MSG = (
    "Schlüssel erfolgreich registriert"  # The text of the link
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "Simple_Format": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file_debug": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "./logs/log_DEBUG.log",
            "formatter": "Simple_Format",
        },
        "file_info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "./logs/log_INFO.log",
            "formatter": "Simple_Format",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "root": {
            "handlers": ["file_debug", "file_info"],
            "level": "DEBUG",
        },
    },
}
