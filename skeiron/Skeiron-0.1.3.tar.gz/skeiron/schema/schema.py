import skeiron.schema.forward
import skeiron.schema.echo
import skeiron.schema.collect
import skeiron.schema.distribute
import skeiron.schema.multiply


def get_schema():
    return {
            "relayservice": {
                "description": "Root node for skeiron specific entries.",
                "type": "array",
                "items": {
                    "oneOf": [
                        skeiron.schema.forward.get_schema(),
                        skeiron.schema.echo.get_schema(),
                        skeiron.schema.collect.get_schema(),
                        skeiron.schema.distribute.get_schema(),
                        skeiron.schema.multiply.get_schema()
                    ]
                },
                "additionalProperties": False
            }
           }
