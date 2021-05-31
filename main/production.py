from main.settings import *

DEBUG = False

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

SECURE_HSTS_SECONDS = 31536000

SECURE_CONTENT_TYPE_NOSNIFF = True

CSRF_COOKIE_SECURE = True

SECURE_HSTS_PRELOAD = True

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
