#
# Copyright (c) 2015, Prometheus Research, LLC
#


from rios.core.output import get_calculationset_json, get_calculationset_yaml


CALCULATIONSET = {
    'calculations': [
        {
            'method': 'python',
            'id': 'foo',
            'options': {
                'expression': 'field1 * 2',
            },
            'type': 'integer',
            'description': 'Some description',
        },
        {
            'options': {
                'callable': 'some_module.my_callable',
            },
            'method': 'python',
            'type': 'integer',
            'id': 'bar',
        }
    ],
    'meta': {
        'zcustom': 123,
        'author': 'John Smith',
    },
    'instrument': {
        'version': '1.0',
        'id': 'urn:some-test',
    },
}


EXPECTED_JSON = """{
  "instrument": {
    "id": "urn:some-test",
    "version": "1.0"
  },
  "meta": {
    "author": "John Smith",
    "zcustom": 123
  },
  "calculations": [
    {
      "id": "foo",
      "description": "Some description",
      "type": "integer",
      "method": "python",
      "options": {
        "expression": "field1 * 2"
      }
    },
    {
      "id": "bar",
      "type": "integer",
      "method": "python",
      "options": {
        "callable": "some_module.my_callable"
      }
    }
  ]
}"""


def test_output_json():
    actual = get_calculationset_json(CALCULATIONSET, pretty=True)
    assert actual == EXPECTED_JSON, actual


EXPECTED_YAML = '''instrument:
  id: urn:some-test
  version: '1.0'
meta:
  author: John Smith
  zcustom: 123
calculations:
- id: foo
  description: Some description
  type: integer
  method: python
  options:
    expression: field1 * 2
- id: bar
  type: integer
  method: python
  options:
    callable: some_module.my_callable'''


def test_output_yaml():
    actual = get_calculationset_yaml(CALCULATIONSET, pretty=True)
    assert actual == EXPECTED_YAML, actual

