import lysidike.schema.emailservice
import lysidike.schema.stdoutservice


def get_schema():
    schema = {
        "description": "list of services for publishing",
        "type": "object",
        "properties": {
            "email": lysidike.schema.emailservice.get_schema(),
            "stdout": lysidike.schema.stdoutservice.get_schema()
        },
        "additionalItems": False
    }
    return schema