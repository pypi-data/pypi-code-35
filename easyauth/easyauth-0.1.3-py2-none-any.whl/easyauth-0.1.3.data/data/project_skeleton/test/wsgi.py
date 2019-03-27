"""
WSGI config for ccm project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import apps
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings.production" % apps.APP_NAME)

application = get_wsgi_application()
