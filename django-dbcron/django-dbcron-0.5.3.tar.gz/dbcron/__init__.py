"""Manage your crontab directly from DB."""
VERSION = (0, 5, 3)
__version__ = '.'.join([str(i) for i in VERSION])
__author__ = 'Anthony Monthe (ZuluPro)'
__email__ = 'amonthe@cloudspectator.com'
__url__ = 'https://github.com/cloudspectatordevelopment/django-dbcron'
default_app_config = 'dbcron.apps.DbcronConfig'
