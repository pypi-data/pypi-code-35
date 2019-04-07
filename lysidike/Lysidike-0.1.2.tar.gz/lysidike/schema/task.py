def get_schema():
    schema = {
        "description": "a task consists of a target service, rules for when to send, and what to send",
        "type": "object",
        "properties": {
            "name": {
                "description": "name for the task",
                "type": "string"
            },
            "service": {
                "description": "one of the configured services e.g.'email'",
                "type": "string",
                "enum": ["email", "stdout"]
            },
            "subject": {
                "description": "subject for message",
                "type": "string"
            },
            "every-nth-message": {
                "description": "collect this amount of messages before publishing them. 0 for never",
                "type": "integer",
                "minimum": 0
            },
            "every-nth-second": {
                "description": "wait this time before publishing all messages that are waiting. 0 for never",
                "type": "number",
                "minimum": 0
            },
            "topics-sub": {
                "description": "use incoming messages from these topics",
                "type": "array",
                "items": {
                    "description": "mqtt topic",
                    "type": "string"
                },
                "additionalItems": False
            }
        },
        "required": ["name", "service", "subject", "every-nth-message", "every-nth-second", "topics-sub"],
        "additionalItems": False
    }

    return schema
