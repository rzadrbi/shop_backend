# config/settings/base.py
import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent


env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')

INSTALLED_APPS = [
    # default
    'django.contrib.admin',
    'django.contrib.auth',

    # installed
    'apps.accounts.apps.AccountsConfig',
    # 'apps.catalog.apps.AccountsConfig',
    # 'apps.inventory.apps.AccountsConfig',
    # 'apps.orders.apps.AccountsConfig',
    # 'apps.rest_framework.apps.AccountsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': env.db_url('DATABASE_URL')
}


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
STATIC_URL = '/static/'
