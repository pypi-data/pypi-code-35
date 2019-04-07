from unv.app.core import create_component_settings
from unv.app.helpers import project_path


SCHEMA = {
    'domain': {'type': 'string'},
    'host': {'type': 'string'},
    'port': {'type': 'integer'},
    'autoreload': {'type': 'boolean'},
    'jinja2': {
        'type': 'dict',
        'schema': {
            'enabled': {'type': 'boolean'}
        }
    },
    'static': {
        'type': 'dict',
        'schema': {
            'public': {
                'type': 'dict',
                'schema': {
                    'path': {'type': 'string'},
                    'url': {'type': 'string'}
                }
            },
            'private': {
                'type': 'dict',
                'schema': {
                    'path': {'type': 'string'},
                    'url': {'type': 'string'}
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
