import os

#: Mailman Core default API Path
MAILMAN_REST_API_URL = 'http://localhost:8001'
#: Mailman Core API user
MAILMAN_REST_API_USER = 'restadmin'
#: Mailman Core API user's password.
MAILMAN_REST_API_PASS = 'restpass'
#: Mailman Core Shared archiving key. This value is set in the :
#: mailman-hyperkitty's configuration file.
MAILMAN_ARCHIVER_KEY = 'SecretArchiverAPIKey'
#: Host for Mailman Core, from where Hyperkitty will accept connections
#: for archiving.
MAILMAN_ARCHIVER_FROM = ('127.0.0.1', '::1')

#: Filter visible Mailing Lists based on the current host being used to serve.
FILTER_VHOST = False

#: Sender in Emails sent out by Postorius.
DEFAULT_FROM_EMAIL = 'postorius@localhost'


# Django Allauth
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_UNIQUE_EMAIL  = True

#: Protocol for URLs generated for authentication, like email
#: confirmation.
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"

SOCIALACCOUNT_PROVIDERS = {
    'openid': {
        'SERVERS': [
            dict(id='yahoo',
                 name='Yahoo',
                 openid_url='http://me.yahoo.com'),
        ],
    },
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email'],
        'FIELDS': [
            'email',
            'name',
            'first_name',
            'last_name',
            'locale',
            'timezone',
        ],
        'VERSION': 'v2.4',
    },
}

#
# django-compressor
# https://pypi.python.org/pypi/django_compressor
#
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
    ('text/x-scss', 'sassc -t compressed {infile} {outfile}'),
    ('text/x-sass', 'sassc -t compressed {infile} {outfile}'),
)


#: Enabled Social Authentication Providers that can be used to
#: authenticate with. A full list of providers can be found at
#: https://django-allauth.readthedocs.io/en/latest/providers.html
#: Please also note that extra configuration is required after
#: a provider is enabled. Django-allauth's documentation mentioned
#: above provides more details about how to configure one.
#: Example::
#:
#:     DJANGO_SOCIAL_AUTH_PROVIDERS = [
#:         'allauth.socialaccount.providers.openid',
#:         'django_mailman3.lib.auth.fedora',
#:         'allauth.socialaccount.providers.github',
#:         'allauth.socialaccount.providers.gitlab',
#:         'allauth.socialaccount.providers.google',
#:         'allauth.socialaccount.providers.facebook',
#:         'allauth.socialaccount.providers.twitter',
#:         'allauth.socialaccount.providers.stackexchange',
#:     ]
DJANGO_SOCIAL_AUTH_PROVERS = []


#
# Social auth
#
#: Authentication backends for Django to be used.
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

#
# Full-text search engine
#
#: Django-Haystack connection parameters.
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': "fulltext_index",
        # You can also use the Xapian engine, it's faster and more accurate,
        # but requires another library.
        # http://django-haystack.readthedocs.io/en/v2.4.1/installing_search_engines.html#xapian
        # Example configuration for Xapian:
        #'ENGINE': 'xapian_backend.XapianEngine'
    },
}

#
# Asynchronous tasks
#
#: Django Q connection parameters.
Q_CLUSTER = {
    'timeout': 300,
    'save_limit': 100,
    'orm': 'default',
}

#: On a production setup, setting COMPRESS_OFFLINE to True will bring a
#: significant performance improvement, as CSS files will not need to be
#: recompiled on each requests. It means running an additional "compress"
#: management command after each code upgrade.
#: http://django-compressor.readthedocs.io/en/latest/usage/#offline-compression
COMPRESS_OFFLINE = True

# Needed for debug mode
# INTERNAL_IPS = ('127.0.0.1',)
