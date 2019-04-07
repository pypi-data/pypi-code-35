import lysidike.schema.servicefactory
import lysidike.schema.task


def get_schema():
    schema = {
        "publish-gateway": {
            "description": "Lysidike publishes incoming mqtt messages to various internet services like email.",
            "type": "object",
            "properties": {
                "services": lysidike.schema.servicefactory.get_schema(),
                "tasks": {
                    "description": "all tasks",
                    "type": "array",
                    "items": lysidike.schema.task.get_schema(),
                    "additionalItems": False
                }
            },
            "required": ["services", "tasks"],
            "additionalItems": False
        }
    }

    return schema