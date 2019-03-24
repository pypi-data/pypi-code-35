# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from pathlib import Path

#: The base directory for logs and database.
BASE_DIR = str(Path.cwd())

#: Default list of admins who receive the emails from error logging.
ADMINS = (
    ('Mailman Suite Admin', 'root@localhost'),
)

#: Hosts/domain names that are valid for this site; required if DEBUG is False.
#: See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    "localhost",  # Archiving API from Mailman, keep it.
    # "lists.your-domain.org",
    # Add here all production URLs you may have.
    "*",
]

#: Enable Development Mode.
DEBUG = False


#: URL Configuration for Django
ROOT_URLCONF = 'mailman_web.urls'


#: Default list of django applications.
INSTALLED_APPS = [
    'hyperkitty',
    'postorius',
    'django_mailman3',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_gravatar',
    'compressor',
    'haystack',
    'django_extensions',
    'django_q',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]


#: Default Django Middlewares.
MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django_mailman3.middleware.TimezoneMiddleware',
    'postorius.middleware.PostoriusMiddleware',
)

#: Default Template finders.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.csrf',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_mailman3.context_processors.common',
                'hyperkitty.context_processors.common',
                'postorius.context_processors.postorius',
            ],
        },
    },
]

#: Wsgi application import path. This will be used by the WSGI server which
#: will be used to deploy this application.
WSGI_APPLICATION = 'mailman_web.wsgi.application'

#: Default Database to be used.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'mailman-web.db'),
        'HOST': '',
        'PORT': '',
    }
}


#: Default password validators.
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
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

#: Default Language code.
LANGUAGE_CODE = 'en-us'

#: Default timezone.
TIME_ZONE = 'UTC'

#: Enable internationalization.
USE_I18N = True

#: Enable localization.
USE_L10N = True

#: Use the timezone information.
USE_TZ = True


#: Default path where static files will be placed.
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#: URL prefix for static files.
#: Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

#: Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # BASE_DIR + '/static/',
)

#: List of finder classes that know how to find static files in
#: various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

#: Django 1.6+ defaults to a JSON serializer, but it won't work with
#: django-openid, see
#: https://bugs.launchpad.net/django-openid-auth/+bug/1252826
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'


#: Default Django URL to redirect to for Login.
LOGIN_URL = 'account_login'
#: Default Django URL to redirect to after a successful login.
LOGIN_REDIRECT_URL = 'list_index'
#: Default Django URL to Logout the user.
LOGOUT_URL = 'account_logout'

#: If you enable email reporting for error messages, this is where those emails
#: will appear to be coming from. Make sure you set a valid domain name,
#: otherwise the emails may get rejected.
#: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SERVER_EMAIL
SERVER_EMAIL = 'root@localhost.local'

#: The default implementation to send out emails. This can be customized to
#: something else for testing purposes.
#: https://docs.djangoproject.com/en/dev/topics/email/#email-backends
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Compatibility with Bootstrap 3
from django.contrib.messages import constants as messages  # flake8: noqa
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}


#: Default Logging configuration.
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
        },
        'file':{
            'level': 'INFO',
            #'class': 'logging.handlers.RotatingFileHandler',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'mailmansuite.log'),
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'hyperkitty': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'postorius': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(process)d %(name)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    #'root': {
    #    'handlers': ['file'],
    #    'level': 'INFO',
    #},
}


# This is merely to setup logging if it isn't defined.
log_path =  Path(LOGGING['handlers']['file']['filename'])
if not log_path.exists():
    log_path.parent.mkdir(exist_ok=True)
    log_path.touch()

#: Current Django Site being served. This is used to customize the web host
#: being used to serve the current website. For more details about Django
#: site, see: https://docs.djangoproject.com/en/dev/ref/contrib/sites/
SITE_ID = 1


#: SECRET_FILE contains the secret key to be used for Django's session and
#: token encryptions.
SECRET_FILE = os.path.join(BASE_DIR, 'secret.txt')
