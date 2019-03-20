# Django settings for votebase core.
import os
from django.core.urlresolvers import reverse_lazy

DEBUG = False
TEMPLATE_DEBUG = DEBUG
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
PREPEND_WWW = True

AUTH_PROFILE_MODULE = 'accounts.Profile'
MAX_USERNAME_LENGTH = 70

LOGIN_URL = reverse_lazy('accounts_login')
REQUIRED_ACTIVATION = False

ADMINS = (
)
MANAGERS = ADMINS

# Facebook
FACEBOOK_APP_ID = '172886466168460'
FACEBOOK_APP_SECRET = '27cdfba10ad0cf80bfceb65fd57f2881'
FACEBOOK_LOGIN_DEFAULT_REDIRECT = reverse_lazy('surveys_index')
FACEBOOK_HIDE_CONNECT_TEST = True

# Google API
GOOGLE_API_KEY = 'TODO'

# GeoIP
import votebase
VOTEBASE_PATH = os.path.dirname(votebase.__file__)
GEOIP_PATH = VOTEBASE_PATH + '/core/voting/geoip/'

# Rosetta
ROSETTA_MESSAGES_PER_PAGE = 10

# DEBUG TOOLBAR CONFIG
INTERNAL_IPS = ('127.0.0.1', )

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}


########## EMAIL CONFIGURATION
DEFAULT_EMAIL_FROM = 'TODO'
DEFAULT_EMAIL_FROM_NAME = 'TODO'
EMAIL_HOST = 'TODO'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'TODO'
EMAIL_HOST_PASSWORD = 'TODO'
EMAIL_USE_TLS = True
########## END EMAIL CONFIGURATION


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'TODO',                      # Or path to database file if using sqlite3.
        'USER': 'TODO',                      # Not used with sqlite3.
        'PASSWORD': 'TODO',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Packages settings
#from votebase.core.accounts.models import Profile
VOTEBASE_SUBSCRIPTION_PERIOD_IN_DAYS = 31
VOTEBASE_PACKAGES_SETTINGS = {
    'BASIC': {
        'monthly_fee': 0, #EUR per month
        'voters_limit': 100000, #per survey
    },
    'STANDARD': {
        'monthly_fee': 9.90, #EUR per month
        'voters_limit': 1000, #per survey
    },
    'PREMIUM': {
        'monthly_fee': 49.90, #EUR per month
        'voters_limit': 100000, #per survey
    }
}

# commerce
COMMERCE_URL = 'http://www.votehub.net'
COMMERCE_EMAIL_FROM = DEFAULT_EMAIL_FROM
COMMERCE_VARIABLE_SYMBOL_PREFIX = '02'


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Bratislava'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

gettext = lambda s: s
LANGUAGES = (
    ('en', gettext('English')),
    ('sk', gettext('Slovak')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = SITE_ROOT + '/media/'
MEDIA_IMAGES_DIR = 'images/'
MEDIA_IMAGES_ROOT = MEDIA_ROOT + MEDIA_IMAGES_DIR

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'


# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4*=tr6jh!fup&amp;jk%g_c#18c*@@2!ag4=cpg=4e2xpw6n=ha(sb'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django_facebook.context_processors.facebook',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'votebase.context_processors.host',
    'votebase.context_processors.protocol',
    'votebase.context_processors.urls',
    'votebase.context_processors.settings_constants',
)

AUTHENTICATION_BACKENDS = (
    'django_facebook.auth_backends.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'breadcrumbs.middleware.BreadcrumbsMiddleware',
    'impersonate.middleware.ImpersonateMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'votebase.core.voting.middleware.VotingFallbackMiddleware',
)

ROOT_URLCONF = 'votehub.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'votehub.wsgi.application'

ABSOLUTE_PATH_TO_DEVELOPER_TOOLKIT = '/home/eskills/environment/lib/python2.6/site-packages/developer_toolkit'
TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
    os.path.join(ABSOLUTE_PATH_TO_DEVELOPER_TOOLKIT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'debug_toolbar',
    'south',
    'easy_thumbnails',
    'django_facebook',
    'impersonate',
    'googl',
    'rosetta',
    'wkhtmltopdf',
    'developer_toolkit',
    'smartextends',
    'longerusername',
    'import_export',

    'votebase',
    'votebase.core.utils',
    'votebase.core.accounts',
    'votebase.core.surveys',
    'votebase.core.statistics',
    'votebase.core.questions',
    'votebase.core.voting',
    'votebase.core.payments',
)

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
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
#        'django': {
#            'handlers': ['console'],
#            'level': 'DEBUG',
#            },
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s',
            },
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
}
########## END LOGGING CONFIGURATION




########## DATE CONFIGURATION
from django.conf.global_settings import DATE_INPUT_FORMATS
DATE_FORMAT = '%Y-%m-%d'
DATE_FORMAT_JS = 'yyyy-mm-dd'
DATE_FORMAT_TAG = 'Y-m-d'
DATE_INPUT_FORMATS = DATE_INPUT_FORMATS + (DATE_FORMAT,)
########## END DATE CONFIGURATION


API_DOCUMENTATION_PATH = os.path.join(STATIC_URL, 'files/votehub_api_v1_documentation_rev12.pdf')
