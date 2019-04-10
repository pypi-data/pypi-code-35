from uuid import uuid4
from urllib import parse

def uuid():
    return str(uuid4())

def merge(dict1, dict2):
    copy = dict1.copy()
    copy.update(dict2)
    return copy

def deep_obfuscate(payload, fields, obfuscate_name='[HIDDEN]'):
    try:
        for key in payload:
            if isinstance(key, str) and key.lower() in fields:
                payload[key] = obfuscate_name
            elif isinstance(payload, dict) and isinstance(payload[key], dict):
                payload[key] = deep_obfuscate(payload[key], fields, obfuscate_name)
            elif isinstance(payload, dict) and isinstance(payload[key], list):
                payload[key] = [deep_obfuscate(value, fields, obfuscate_name) for value in payload[key]]
        return payload
    except (AttributeError, TypeError):
        return payload

def deep_compact(payload):
    try:
        for key in payload.copy():
            if payload[key] is None or payload[key] == {} or payload[key] == []:
                del payload[key]
            elif isinstance(payload[key], dict):
                payload[key] = deep_compact(payload[key])
            elif isinstance(payload[key], list):
                payload[key] = [deep_compact(value) for value in payload[key]]
        return payload
    except (AttributeError, TypeError):
        return payload


def url_obfuscate(url, fields, obfuscate_name='HIDDEN'):
    uri = parse.urlsplit(url)
    query = deep_obfuscate(dict(parse.parse_qsl(uri.query)), fields, obfuscate_name)

    return parse.urljoin(url, '?{0}'.format(parse.urlencode(query)))
