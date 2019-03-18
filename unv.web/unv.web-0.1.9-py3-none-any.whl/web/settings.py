from unv.app.core import create_component_settings
from unv.app.helpers import project_path


SCHEMA = {
    "type": "object",
    "properties": {
        "domain": {
            "type": "string",
            "required": True
        },
        "protocol": {
            "type": "string",
            "allowed": ["http", "https"],
            "required": True
        },
        "host": {
            "type": "string",
            "required": True
        },
        "port": {
            "type": "integer",
            "required": True
        },
        "autoreload": {
            "type": "boolean",
            "required": True
        },
        "jinja2": {
            "type": "object",
            "properties": {
                "enabled": {
                    "type": "boolean",
                    "required": True
                }
            }
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
    'jinja2': {
        'enabled': True,
    },
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
