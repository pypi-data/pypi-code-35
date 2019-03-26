from django.conf import settings
from importlib import import_module
from .registry import HandlerRegistry
import imp
import sys


handlers = HandlerRegistry()


def process_webhook(source, request):
    return handlers.receive(source, request)


def autodiscover():
    for app in settings.INSTALLED_APPS:
        import_module(app)
        app_path = sys.modules[app].__path__

        try:
            imp.find_module('webhook_handlers', app_path)
        except ImportError:
            continue

        import_module('%s.%s' % (app, 'webhook_handlers'))
