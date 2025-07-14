# config/settings/development.py
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
INTERNAL_IPS = ['127.0.0.1']
