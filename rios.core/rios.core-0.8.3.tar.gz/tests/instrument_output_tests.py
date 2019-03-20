#
# Copyright (c) 2015, Prometheus Research, LLC
#


from rios.core.output import get_instrument_json, get_instrument_yaml


INSTRUMENT = {
    'description': 'Describing the Instrument',
    'record': [
        {
            'explanation': 'optional',
            'type': 'zText',
            'required': True,
            'id': 'field1',
            'identifiable': False,
            'annotation': 'none'
        },
        {
            'type': {
                'base': 'matrix',
                'rows': [
                    {
                        'required': True,
                        'description': 'A description',
                        'id': 'row1',
                    },
                    {
                        'id': 'row2',
                    },
                ],
                'columns': [
                    {
                        'type': 'text',
                        'id': 'col1',
                    },
                    {
                        'id': 'col2',
                        'type': {
                            'pattern': 'foo',
                            'base': 'text',
                        }
                    },
                ],
            },
            'id': 'field2',
        },
        {
            'id': 'field3',
            'type': {
                'enumerations': {
                    'foo': {},
                    'baz': {},
                    'bar': {
                        'description': 'Describing an enumeration',
                    },
                },
                'base': 'enumerationSet',
                'length': {
                    'max': 2,
                },
            },
        },
    ],
    'meta': {
        'zcustom': 123,
        'author': 'John Smith',
    },
    'types': {
        'zType': {
            'length': {
                'max': 10,
                'min': 2,
            },
            'base': 'text',
        },
        'aType': {
            'range': {
                'max': 10,
                'min': 2,
            },
            'base': 'integer',
        }
    },
    'title': 'The Instrument Title',
    'version': '1.0',
    'id': 'urn:output-tester',
}


EXPECTED_JSON = """{
  "id": "urn:output-tester",
  "version": "1.0",
  "title": "The Instrument Title",
  "description": "Describing the Instrument",
  "meta": {
    "author": "John Smith",
    "zcustom": 123
  },
  "types": {
    "aType": {
      "base": "integer",
      "range": {
        "min": 2,
        "max": 10
      }
    },
    "zType": {
      "base": "text",
      "length": {
        "min": 2,
        "max": 10
      }
    }
  },
  "record": [
    {
      "id": "field1",
      "type": "zText",
      "required": true,
      "identifiable": false,
      "annotation": "none",
      "explanation": "optional"
    },
    {
      "id": "field2",
      "type": {
        "base": "matrix",
        "columns": [
          {
            "id": "col1",
            "type": "text"
          },
          {
            "id": "col2",
            "type": {
              "base": "text",
              "pattern": "foo"
            }
          }
        ],
        "rows": [
          {
            "id": "row1",
            "description": "A description",
            "required": true
          },
          {
            "id": "row2"
          }
        ]
      }
    },
    {
      "id": "field3",
      "type": {
        "base": "enumerationSet",
        "length": {
          "max": 2
        },
        "enumerations": {
          "bar": {
            "description": "Describing an enumeration"
          },
          "baz": {},
          "foo": {}
        }
      }
    }
  ]
}"""


def test_output_json():
    actual = get_instrument_json(INSTRUMENT, pretty=True)
    assert actual == EXPECTED_JSON, actual


EXPECTED_YAML = '''id: urn:output-tester
version: '1.0'
title: The Instrument Title
description: Describing the Instrument
meta:
  author: John Smith
  zcustom: 123
types:
  aType:
    base: integer
    range:
      min: 2
      max: 10
  zType:
    base: text
    length:
      min: 2
      max: 10
record:
- id: field1
  type: zText
  required: true
  identifiable: false
  annotation: none
  explanation: optional
- id: field2
  type:
    base: matrix
    columns:
    - id: col1
      type: text
    - id: col2
      type:
        base: text
        pattern: foo
    rows:
    - id: row1
      description: A description
      required: true
    - id: row2
- id: field3
  type:
    base: enumerationSet
    length:
      max: 2
    enumerations:
      bar:
        description: Describing an enumeration
      baz: {}
      foo: {}'''


def test_output_yaml():
    actual = get_instrument_yaml(INSTRUMENT, pretty=True)
    assert actual == EXPECTED_YAML, actual

