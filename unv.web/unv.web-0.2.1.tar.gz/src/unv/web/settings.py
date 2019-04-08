from unv.app.core import create_component_settings
from unv.app.helpers import project_path


SCHEMA = {
    'domain': {'type': 'string', 'required': True},
    'autoreload': {'type': 'boolean', 'required': True},
    'jinja2': {
        'type': 'dict',
        'required': True,
        'schema': {
            'enabled': {'type': 'boolean'}
        }
    },
    'static': {
        'type': 'dict',
        'required': True,
        'schema': {
            'public': {
                'type': 'dict',
                'required': True,
                'schema': {
                    'path': {'type': 'string', 'required': True},
                    'url': {'type': 'string', 'required': True}
                }
            },
            'private': {
                'type': 'dict',
                'required': True,
                'schema': {
                    'path': {'type': 'string', 'required': True},
                    'url': {'type': 'string', 'required': True}
                }
            }
        }
    }
}

DEFAULTS = {
    'domain': 'https://app.local',
    'autoreload': False,
    'jinja2': {'enabled': True},
    'static': {
        'public': {
            'path': project_path('static', 'public'),
            'url': '/static/public',
        },
        'private': {
            'path': project_path('static', 'private'),
            'url': '/static/private'
        }
    }
}

SETTINGS = create_component_settings('web', DEFAULTS, SCHEMA)
