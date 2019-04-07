def get_schema():
    return {
        "type": "object",
        "properties": {
            "name": {
                "description": "unique name for relay event",
                "type": "string"
            },
            "active": {
                "description": "entry ignored if set to False",
                "type": "boolean"
            },
            "type": {
                "description": "[forward, echo, collect, distribute, multiply]",
                "type": "string",
                "enum": ["echo"]
            },
            "topic": {
                "description": "all messages incoming on this topic are published back to this topic.",
                "type": "string"
            },
            "replace-message": {
                "description": "use this message instead of received message (optional)",
                "type": "string"
            }
        },
        "required": ["active", "name", "type", "topic"],
        "additionalProperties": False
    }