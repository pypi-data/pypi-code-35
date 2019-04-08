import os


try:
    from django.conf import settings
except ImportError:
    settings = object()


def s(key, default=None):
    value = getattr(
        settings,
        'PODIANT_%s' % key,
        os.getenv('PODIANT_%s' % key)
    )

    return default if value is None else value


DOMAIN = s('DOMAIN', 'api.podiant.co')
SSL = s('SSL') != 'false'
CLIENT_ID = s('CLIENT_ID')
CLIENT_SECRET = s('CLIENT_SECRET')


__all__ = (
    'DOMAIN',
    'SSL',
    'CLIENT_ID',
    'CLIENT_SECRET'
)
