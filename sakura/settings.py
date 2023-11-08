"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 3.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import configparser
from configparser import RawConfigParser
from pathlib import Path

config = RawConfigParser()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
config.read(str(BASE_DIR) + '/settings.ini')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('setup', 'SECRET')

# DISCORD BOT TOKEN
TOKEN = config.get('discord', "DISCORD_TOKEN")

# DISCORD BOT AUTH REDIRECT URL
DISCORD_AUTH_URL = config.get('discord', "DISCORD_AUTH_URL")

CLIENT_ID = config.get('discord', "CLIENT_ID")
CLIENT_SECRET = config.get('discord', "CLIENT_SECRET")
DISCORD_REDIRECT_URL = config.get('discord', "DISCORD_REDIRECT_URL")
# DISCORD BOT INVITE LINK
DISCORD_INVITE_LINK = config.get('discord', "DISCORD_INVITE_LINK")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.get('setup', "DJANGO_DEBUG")

ALLOWED_HOSTS = ["*"]

try:
    GUILD_IDS = config.get('discord', "GUILD_ID")
except configparser.NoOptionError:
    GUILD_IDS = None

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth',
    'django.contrib.contenttypes', 'django.contrib.sessions',
    'django.contrib.messages', 'django.contrib.staticfiles',
    'sakura.authentication', 'sakura.bot', 'sakura.server', 'sakura.dashboard',
    'sakura.welcome', 'sakura.help', 'sakura.selfrole'
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    'sakura.authentication.auth.SakuraAuthenticationBackend'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sakura.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            Path.joinpath(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'sakura.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.' +
        'UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# SECURE_HSTS_SECONDS = 31536000

# SECURE_CONTENT_TYPE_NOSNIFF = True

# CSRF_COOKIE_SECURE = True

# SECURE_HSTS_PRELOAD = True

# SECURE_SSL_REDIRECT = True

# SESSION_COOKIE_SECURE = True

# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_URL = '/static/'
STATIC_ROOT = 'assets/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

LOGIN_URL = 'http://127.0.0.1:8000/auth/login'
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'