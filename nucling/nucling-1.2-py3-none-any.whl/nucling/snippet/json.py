import json


def try_to_parse_json(string):
    """
    try to parse a json string if not a valid json return the same string

    Parameters
    ----------
    string: string
        a string for try to parse like json
    """
    try:
        return json.loads(string)
    except ValueError:
        return string
