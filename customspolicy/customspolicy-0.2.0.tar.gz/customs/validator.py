from jsonschema import validate, FormatChecker
import json
import logging

json_valid = {
    "$schema": "http://json-schema.org/schema#",
    "title": "JSON SCHEMA To Validate Client Input",
    "description": "JSON SCHEMA To Validate Client Input",
    "type": "object",
    "properties": {
        "Reference Date": {
            "type": "string",
            "format": "date"
        },
        "Entries": {
            "type": "array",
            "items": {
                "type": "string",
                "format": "date"
            }
        },
        "Exits": {
            "type": "array",
            "items": {
                "type": "string",
                "format": "date"
            }
        }
    },
    "required": [
        "Reference Date",
        "Entries",
        "Exits"
    ]
}


def is_json_correct(data):
    try:
        flag = validate(data, json_valid, format_checker=FormatChecker())
    except Exception as valid_err:
        logging.info('validation KO: {}'.format(valid_err))
        flag = valid_err.args[0]
    else:
        flag = True
    return flag
