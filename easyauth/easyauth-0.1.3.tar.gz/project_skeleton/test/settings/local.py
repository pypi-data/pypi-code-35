"""Development settings."""

import os
os.environ['EASYAUTH_LOG_LEVEL'] = 'DEBUG'
# os.environ['DJANGO_SERVER_LOG_LEVEL'] = 'DEBUG'
# os.environ['DJANGO_LOG_LEVEL'] = 'DEBUG'

from os.path import join, normpath
from .production import *


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
CORS_ORIGIN_ALLOW_ALL = DEBUG
CORS_ALLOW_CREDENTIALS = DEBUG
########## END DEBUG CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': normpath(join(WK_DIR, 'db.sqlite3')),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
########## END DATABASE CONFIGURATION

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    'DEFAULT_PERMISSION_CLASSES': (
        'easyauth.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'easyauth.authentication.CsrfExemptSessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        #  Enable BrowsableAPI
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter'
    ),
    'EXCEPTION_HANDLER': 'easyauth.views.exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'easyauth.pagination.CustomizedPageNumberPagination',
    'PAGE_SIZE': 500,
}
