def get_schema():
    schema = {
        "description": "publish to stdout",
        "type": "object",
        "properties": {
            "prefix": {
                "description": "prefix for stdout",
                "type": "string"
            },
            "suffix": {
                "description": "suffix for stdout",
                "type": "string"
            }
        },
        "additionalItems": False,
        "required": ["prefix", "suffix"]
    }

    return schema
