from unv.app.core import create_component_settings
from unv.app.helpers import project_path


SCHEMA = {
    "type": "object",
    "properties": {
        "domain": {
            "type": "string",
            "required": "true"
        },
        "protocol": {
            "type": "string",
            "allowed": ["http", "https"],
            "required": "true"
        },
        "host": {
            "type": "string",
            "required": "true"
        },
        "port": {
            "type": "integer",
            "required": "true"
        },
        "autoreload": {
            "type": "boolean",
            "required": "true"
        },
        "static": {
            "type": "object",
            "properties": {
                "paths": {
                    "type": "object",
                    "properties": {
                        "public": {"type": "string", "required": True},
                        "private": {"type": "string", "required": True}
                    }
                },
                "urls": {
                    "type": "object",
                    "properties": {
                        "public": {"type": "string", "required": True},
                        "private": {"type": "string", "required": True}
                    }
                }
            }
        }
    }
}

DEFAULTS = {
    'domain': 'app.local',
    'protocol': 'https',
    'host': '0.0.0.0',
    'port': 8000,
    'autoreload': False,
    'static': {
        'paths': {
            'public': project_path('static', 'public'),
            'private': project_path('static', 'private')
        },
        'urls': {
            'public': '/static/public',
            'private': '/static/private'
        }
    }
}

SETTINGS = create_component_settings('web', DEFAULTS, SCHEMA)
