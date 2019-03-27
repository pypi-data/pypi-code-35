"""Production settings."""


import os
from os.path import abspath, basename, dirname, join, normpath, isdir
from sys import path


########## PATH CONFIGURATION
# Absolute filesystem path to the top-level project folder:
APP_ROOT = dirname(dirname(abspath(__file__)))

# App name:
APP_NAME = basename(APP_ROOT)

# Absolute filesystem path to the Django project directory:
WK_DIR = dirname(APP_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(WK_DIR)
########## END PATH CONFIGURATION


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
# ADMINS = (
#     ('Your Name', 'your_email@example.com'),
# )

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
# MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


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


########## Cross-Origin Read Blocking CONFIGURATION
# See: https://github.com/ottoyiu/django-cors-headers
# CORS_ORIGIN_REGEX_WHITELIST = True
# Or
# CORS_ORIGIN_WHITELIST = (
#     '<YOUR_DOMAIN>[:PORT]',
# )
# Or
# CORS_ORIGIN_REGEX_WHITELIST = (r'^(https?://)?(\w+\.)?google\.com$', )
# ...
#
########## END Cross-Origin Read Blocking CONFIGURATION

########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
# TIME_ZONE = 'America/Los_Angeles'
TIME_ZONE = 'Asia/Shanghai'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en'
# LANGUAGE_CODE = 'zh-hans'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
########## END GENERAL CONFIGURATION


########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(WK_DIR, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(WK_DIR, 'static'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    # Add vue-ui/dist to django webapp
    normpath(join(WK_DIR, 'vue-ui/dist')),
)
#
# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
########## END STATIC FILE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
SECRET_KEY = r"a@m_u@22l@r0m)pgkm(unp2dll-14ms&aw%e-svhrdf$g657us"
########## END SECRET CONFIGURATION


########## FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    normpath(join(WK_DIR, 'fixtures')),
)
########## END FIXTURE CONFIGURATION


########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

# # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    normpath(join(WK_DIR, 'templates')),
)
########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    # Default Django middleware.
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'easyauth.middleware.SwitchLanguageMiddleware',
    'easyauth.middleware.RequestLoggingMiddleware',
)
########## END MIDDLEWARE CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Admin panel and documentation:
    'django.contrib.admin',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'rest_framework',
    'django_filters',
    'corsheaders',
    'easyauth',
    '%s' % APP_NAME
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS
########## END APP CONFIGURATION


########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
########## END LOGGING CONFIGURATION


########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = '%s.wsgi.application' % APP_NAME
########## END WSGI CONFIGURATION

########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % APP_NAME
########## END URL CONFIGURATION


########## SOUTH CONFIGURATION
# See: http://south.readthedocs.org/en/latest/installation.html#configuring-your-django-installation
INSTALLED_APPS += (
    # Database migration helpers:
    # 'south',
)
# Don't need to use South when setting up a test database.
# SOUTH_TESTS_MIGRATE = False
########## END SOUTH CONFIGURATION


#X_FRAME_OPTIONS = 'ALLOWALL'


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
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
    'PAGE_SIZE': 500
}

AUTH_USER_MODEL = '%s.User' % APP_NAME

########## SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*', ]
########## END SITE CONFIGURATION


LOCALE_PATHS = ('/locale', )

# Create log folder
LOG_ROOT_PATH = join(WK_DIR, 'logs')
if not isdir(LOG_ROOT_PATH):
    os.mkdir(LOG_ROOT_PATH)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)s [%(threadName)s] [%(name)s] %(pathname)s %(funcName)s %(lineno)d: %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s [%(threadName)s] [%(name)s] %(message)s'
        },
    },
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
        'server_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_ROOT_PATH, "server.log"),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'encoding': 'UTF-8',
            'formatter': 'simple'
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'django.db.backends': {
            'level': os.getenv('DJANGO_DB_BACKEND_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        # 'django.server': {
        #     'level': os.getenv('DJANGO_SERVER_LOG_LEVEL', 'INFO'),
        #     'propagate': True,
        # },
        'easyauth': {
            'level': os.getenv('EASYAUTH_LOG_LEVEL', 'INFO'),
            'propagate': True
        },
        '': {
            'handlers': ['server_log', 'console'],
            'level': 'INFO',
            'propagate': True
        },
    }
}

################### Session Setting #####################
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 7 days
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False


EASYAUTH_CONF = {
    'USER_DEFAULT_PWD_MAINTAIN_BY_ADMIN': "12345678",
    'ACCOUNT_LOGOUT_ON_GET': True,
    'DISABLE_REGISTER': False,
    'LANG_PARAM': 'lang',
}
