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
    "path": ".",
    'debug': False,
    'components': [],
}

SETTINGS = create_component_settings('app', DEFAULTS, SCHEMA)
