from unv.utils.os import get_homepath

from .core import create_component_settings


SCHEMA = {
    "type": "object",
    "properties": {
        "root": {
            "type": "string",
            "required": True
        },
        "debug": {
            "type": "boolean",
            "required": True
        },
        "path": {
            "type": "string",
            "required": True
        },
        "components": {
            "type": "array",
            "items": {"type": "string"},
            "required": True
        }
    }
}

DEFAULTS = {
    "root": str(get_homepath()),
    'debug': False,
    'components': [],
}

SETTINGS = create_component_settings('app', DEFAULTS, SCHEMA)
