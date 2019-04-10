import argparse
import json
from pathlib import Path
from typing import Optional, Sequence, Union


def parse(schema: Union[dict, str, Path], args: Optional[Sequence[str]] = None) -> dict:
    if not isinstance(schema, dict):
        with open(str(schema)) as f:
            schema: dict = json.load(f)
    assert 'type' in schema and schema['type'] == 'object'
    assert 'properties' in schema

    required = set(schema.get('required', []))

    type_map = {
        'string': str,
        'integer': int,
        'number': float
    }

    parser = argparse.ArgumentParser(description=schema.get('description'))
    for name, value in schema.get('properties', {}).items():
        assert isinstance(value, dict)

        type = value.get('type')
        default = value.get('default')

        if type == 'boolean':
            parser.add_argument(f'--{name}', action='store_true')
        else:
            parser.add_argument(f'--{name}', type=type_map[type], default=default, required=name in required)

    return vars(parser.parse_args(args=args))
