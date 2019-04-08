from unv.utils.os import get_homepath

from .core import create_component_settings


SCHEMA = {
    'name': {
        'empty': False,
        'type': 'string',
        'required': True
    },
    'root': {
        'empty': False,
        'type': 'string',
        'required': True
    },
    'env': {
        'type': 'string',
        'allowed': ['production', 'development', 'testing'],
        'required': True
    },
    'components': {
        'type': 'list',
        'empty': True,
        'schema': {'type': 'string'},
        'required': True
    }
}

DEFAULTS = {
    'root': str(get_homepath()),
    'env': 'development',
    'components': [],
}

SETTINGS = create_component_settings('app', DEFAULTS, SCHEMA)

DEVELOPMENT = SETTINGS['env'] == 'development'
PRODUCTION = SETTINGS['env'] == 'production'
TESTING = SETTINGS['env'] == 'testing'
