"""
Django settings for delegues project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import re
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DELEGUES_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'delegues',
    'flat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'pagination',
    'djangobb_forum',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',


    'djangobb_forum.middleware.LastLoginMiddleware',
    'djangobb_forum.middleware.UsersOnline',
    'djangobb_forum.middleware.TimezoneMiddleware',
)

ROOT_URLCONF = 'delegues.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'djangobb_forum.context_processors.forum_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'delegues.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {

    }
}

# Tequila backend
AUTH_USER_MODEL = 'delegues.DegUser'
AUTHENTICATION_BACKENDS = ('delegues.tequila.Backend',)
LOGIN_URL = '/login'

TEQUILA_SERVER = 'https://tequila.epfl.ch'  # Url of tequila server
TEQUILA_SERVICE = 'Forum des Délégués'  # Title used in tequila
TEQUILA_AUTOCREATE = True  # Auto create users ?
TEQUILA_UPDATE = True  # Update users ?
TEQUILA_FAILURE = '/failure'  # Where to redirect user if there is a problem

LDAP = "ldaps://ldap.epfl.ch:636"

LDAP_REFRESH = datetime.timedelta(weeks=1)

# LDAP ou=.. filters
AUTHORIZED_ORGANISATIONS = [re.compile(r) for r in [
    r'agepoly', # Comité
    r'agepolytique', # Agepolitique
    r'agepinfo', # Agepinfo (for admin purpose)
    r'ae', # EPFL Assembly
    r'cf-\w+', # Faculty Council # TODO: handle CF-{{section_name}}
]]

AUTHORIZED_GROUPS = [re.compile(r) for r in [
    r'delegues-classes'
]]


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

try:
    from .local_settings import *
except ImportError:
    pass
