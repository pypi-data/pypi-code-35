#!/usr/bin/env python
import os
from os.path import abspath, basename, dirname, join, isfile, isdir

import sys


def get_app_name():
    WK_DIR = dirname(abspath(__file__))
    for subdir in os.listdir(WK_DIR):
        if isdir(subdir):
            if isfile(join(subdir, "__init__.py")) \
                    and isfile(join(subdir, "apps.py")) \
                    and isfile(join(subdir, "settings/__init__.py")) \
                    and isfile(join(subdir, "settings/local.py")):
                _app = __import__(basename(subdir), fromlist=['apps'])
                return _app.apps.APP_NAME
                # return basename(subdir)
    return None


if __name__ == "__main__":
    __app_name = get_app_name()
    if __app_name:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings.local" % __app_name)
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
