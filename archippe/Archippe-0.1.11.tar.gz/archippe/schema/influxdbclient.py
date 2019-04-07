def get_schema():
    schema = {
        "description": "Influx configuration",
        "type": "object",
        "properties": {
            "influx-address": {
                "description": "URL of influx db",
                "type": "string"
            },
            "influx-port": {
                "description": "Port of influx db",
                "type": "integer",
                "minimum": 0,
                "exclusiveMinimum": True
            },
            "log-level": {
                "description": "Log level to be used (optional).",
                "type": "string",
                "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            },
            "credentials-file": {
                "description": "File containing the credentials (optional).",
                "type": "string"
            },
            "influx-user": {
                "description": "User name for influx db (optional).",
                "type": "string"
            },
            "influx-password": {
                "description": "Password for influx db (optional).",
                "type": "string"
            },
            "database": {
                "description": "Database",
                "type": "string"
            }
        },
        "required": ["influx-address", "influx-port", "database"]
    }

    return schema
