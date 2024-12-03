from pathlib import Path
from typing import Dict, List

from dotenv import dotenv_values

from split_settings.tools import include


CONFIG: Dict[str, str] = {
    **dotenv_values(".env.shared"),  # type: ignore[dict-item]
    **dotenv_values(".env"),  # type: ignore[dict-item]
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-t=l0aupwp(*ktptudw*qork@1!e519lb5=2en^%g45x%=-1kms'

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS: List[str] = []

DEBUG = CONFIG["DEBUG"] in ["true", "1", "yes"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'eventlog.apps.EventLogConfig',
    'rest_framework',
    'rest_framework.authtoken',
    "django_filters",
    "django_commands",
    "health_check",
    "corsheaders",
    "health_check.db",
    "health_check.cache",
    "health_check.contrib.celery",
    "health_check.contrib.psutil",
    "health_check.contrib.redis",
    "constance",
    "django_extensions",
    'school',
    "sync_model",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'schoolproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'schoolproject.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'django_static/'
STATIC_ROOT = 'django_static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DJANGO_COMMANDS_ALLOW_REMOTE_CALL = ["slow_command"]

include(
        "logging_settings.py",
        "cache_settings.py",
        "rest_settings.py",
        "database_settings.py",
)

CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
