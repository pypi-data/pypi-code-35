# -*- coding: utf-8 -*-

import os
import re

import yaml
from sanic.response import json


def format_path(*parts):
    path = ''

    for part in parts:
        path = f'/{path}/{part}'

    return re.sub(r'/+', '/', path.rstrip('/'))


def validated_identifier(value):
    if not re.match(r'^[a-zA-Z0-9-]*$', value):
        raise Exception(
            f'Invalid identifier "{value}" - may only contain alphanumeric and hyphen characters.'
        )

    return value


def jsonify(data, **kwargs):
    return json(body=data, **kwargs, indent=4)


def request_ip(request):
    return request.remote_addr or request.ip


def yaml_parse(file, keys_to_upper=False):
    settings_dir = os.environ.get('JET_SETTINGS_DIR', 'settings')
    path = f'{settings_dir}/{file}'

    with open(path, 'r') as stream:
        for key, value in yaml.load(stream).items():
            if keys_to_upper:
                yield key.upper(), value
            else:
                yield key, value
