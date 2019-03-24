import os

from mailman_web.settings.base import *
from mailman_web.settings.mailman import *

from django_settings_toml import load_settings


load_settings(__name__, ['/etc/mailman-web.toml', '/etc/mailman3/mailman-web.toml', './mailman-web.toml'])


# If the SECRET_KEY variable is defined, we don't need to do anything, but if
# it is not, we try to read it from SECRET_FILE.
try:
    SECRET_KEY
except NameError:
    if os.path.exists(SECRET_FILE):
        with open(SECRET_FILE) as fd:
            SECRET_KEY = fd.read().strip()
    else:
        print('Please create a {} file with random characters'
              ' to generate your secret key!'.format(SECRET_FILE))
        print('You can run "$ dd if=/dev/urandom bs=100 count=1|base64 > secret.txt"')


#: Add social accounts to Django's INSTALLED_APPS so that they can be enabled
#: for use.
INSTALLED_APPS.extend(DJANGO_SOCIAL_AUTH_PROVERS)
