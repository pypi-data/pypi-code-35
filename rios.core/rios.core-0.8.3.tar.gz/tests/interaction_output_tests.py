#
# Copyright (c) 2015, Prometheus Research, LLC
#


from rios.core.output import get_interaction_json, get_interaction_yaml


INTERACTION = {
    'defaultTimeout': {
        'abort': {
            'text': {
                'en': 'Abort!',
            },
            'threshold': 123,
        },
        'warn': {
            'threshold': 40,
            'text': {
                'fr': 'French warning',
                'en': 'Warning!',
            },
        },
    },
    'steps': [
        {
            'options': {
                'text': {
                    'en': 'Introductory message',
                },
            },
            'type': 'text',
        },
        {
            'options': {
                'error': {
                    'en': 'You failed',
                },
                'enumerations': [
                    {
                        'text': {
                            'en': 'Foo',
                        },
                        'id': 'foo',
                    },
                    {
                        'id': 'bar',
                        'text': {
                            'en': 'Bar',
                            'ar': 'Arabic Bar',
                        },
                    },
                ],
                'fieldId': 'field1',
                'text': {
                    'en': 'Text for field1',
                },
            },
            'type': 'question',
        },
    ],
    'meta': {
        'zcustom': 123,
        'author': 'John Smith',
    },
    'instrument': {
        'version': '1.0',
        'id': 'urn:some-test',
    },
    'defaultLocalization': 'en',
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
  "defaultLocalization": "en",
  "defaultTimeout": {
    "warn": {
      "threshold": 40,
      "text": {
        "en": "Warning!",
        "fr": "French warning"
      }
    },
    "abort": {
      "threshold": 123,
      "text": {
        "en": "Abort!"
      }
    }
  },
  "steps": [
    {
      "type": "text",
      "options": {
        "text": {
          "en": "Introductory message"
        }
      }
    },
    {
      "type": "question",
      "options": {
        "fieldId": "field1",
        "text": {
          "en": "Text for field1"
        },
        "error": {
          "en": "You failed"
        },
        "enumerations": [
          {
            "id": "foo",
            "text": {
              "en": "Foo"
            }
          },
          {
            "id": "bar",
            "text": {
              "ar": "Arabic Bar",
              "en": "Bar"
            }
          }
        ]
      }
    }
  ]
}"""


def test_output_json():
    actual = get_interaction_json(INTERACTION, pretty=True)
    assert actual == EXPECTED_JSON, actual


EXPECTED_YAML = '''instrument:
  id: urn:some-test
  version: '1.0'
meta:
  author: John Smith
  zcustom: 123
defaultLocalization: en
defaultTimeout:
  warn:
    threshold: 40
    text:
      en: Warning!
      fr: French warning
  abort:
    threshold: 123
    text:
      en: Abort!
steps:
- type: text
  options:
    text:
      en: Introductory message
- type: question
  options:
    fieldId: field1
    text:
      en: Text for field1
    error:
      en: You failed
    enumerations:
    - id: foo
      text:
        en: Foo
    - id: bar
      text:
        ar: Arabic Bar
        en: Bar'''


def test_output_yaml():
    actual = get_interaction_yaml(INTERACTION, pretty=True)
    assert actual == EXPECTED_YAML, actual

