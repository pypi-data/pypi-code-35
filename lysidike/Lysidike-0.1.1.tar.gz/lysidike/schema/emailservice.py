def get_schema():
    schema = {
        "description": "publish data via email",
        "type": "object",
        "properties": {
            "address": {
                "description": "url",
                "type": "string"
            },
            "port": {
                "description": "port (e.g.: 587)",
                "type": "integer",
                "minimum": 0,
                "maximum": 65535
            },
            "credentials-file": {
                "description": "File containing the credentials (optional).",
                "type": "string"
            },
            "username": {
                "description": "username for smtp server",
                "type": "string"
            },
            "password": {
                "description": "password for smtp server",
                "type": "string"
            },
            "from": {
                "description": "sender e-mail address",
                "type": "string"
            },
            "to": {
                "description": "receiver e-mail address",
                "oneOf": [
                    {"type": "string"},
                    {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                ]
            }
        },
        "additionalItems": False,
        "required": ["address", "port", "from", "to"]
    }

    return schema
