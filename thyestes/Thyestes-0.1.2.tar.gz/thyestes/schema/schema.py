def get_schema():
    return {
            "timerservice": {
                "description": "Root node for thyestes specific entries.",
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "description": "unique name for timer event",
                            "type": "string"
                        },
                        "topic-sub": {
                            "description": "topics to be subscribed to",
                            "type": "string"
                        },
                        "topic-command": {
                            "description": "message that initiates the timer. optional - if no-entry or None as value "
                                           "every message will trigger timer",
                            "type": ["string", "null"]
                        },
                        "topic-pub": {
                            "description": "topic to publish the timer event to",
                            "type": "string"
                        },
                        "timer-message": {
                            "description": "message to be published when a timer event happens",
                            "type": "string"
                        },
                        "on-new-command-behavior": {
                            "description": "[restart, spawn] - should the same timer be restarted (there is only one "
                                           "timer and it will be resetted) or should a new timer be spawned (the "
                                           "previous timer continous to count down untouched).",
                            "type": "string",
                            "enum": ["restart", "spawn", "RESTART", "SPAWN", "Restart", "Spawn"]
                        },
                        "timer-value": {
                            "description": "timeout in seconds",
                            "type": "number",
                            "minimum": 0,
                            "exclusiveMinimum": True
                        },
                        "active": {
                            "description": "entry ignored if set to False",
                            "type": "boolean"
                        }
                    },
                    "required": ["active", "name",  "timer-value", "on-new-command-behavior", "timer-message",
                                 "topic-pub", "topic-sub"],
                    "additionalProperties": False
                },
                "additionalProperties": False
            }
           }
