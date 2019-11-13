# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import
import os

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "testing_secret"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_approval',
    }
}


ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    'django.contrib.messages',
    "django.contrib.contenttypes",
    "django.contrib.sites",
    'django.contrib.sessions',
    "django.contrib.staticfiles",
    "django_approval",
    "django_approval.test_utils.test_app"
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.context_processors.auth'
            ]
        }
    },
]

STATIC_URL = '/static/'
SITE_ID = 1
