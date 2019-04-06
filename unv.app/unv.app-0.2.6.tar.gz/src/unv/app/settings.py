from unv.utils.os import get_homepath

from .core import create_component_settings


SCHEMA = {
    'root': {
        'empty': False,
        'type': 'string',
    },
    'env': {
        'type': 'string',
        'allowed': ['production', 'development', 'testing']
    },
    'components': {
        'type': 'list',
        'empty': True,
        'schema': {'type': 'string'},
    }
}

DEFAULTS = {
    'root': str(get_homepath()),
    'env': 'development',
    'components': [],
}

SETTINGS = create_component_settings('app', DEFAULTS, SCHEMA)
