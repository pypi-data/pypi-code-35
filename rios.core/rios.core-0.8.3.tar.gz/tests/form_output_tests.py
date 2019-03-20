#
# Copyright (c) 2015, Prometheus Research, LLC
#


from rios.core.output import get_form_json, get_form_yaml


FORM = {
    'pages': [
        {
            'id': 'page1',
            'elements': [
                {
                    'type': 'header',
                    'options': {
                        'text': {
                            'en': 'A Header'
                        },
                    },
                },
                {
                    'tags': [
                        'foo',
                        'bar',
                    ],
                    'type': 'divider',
                },
                {
                    'type': 'question',
                    'options': {
                        'help': {
                            'en': 'Some Help',
                        },
                        'questions': [
                            {
                                'text': {
                                    'en': 'SubField',
                                },
                                'fieldId': 'subfield',
                            },
                        ],
                        'text': {
                            'fr': 'French Question 1',
                            'en': 'Question 1',
                        },
                        'widget': {
                            'options': {
                                'foo': 'bar',
                                'baz': 'stuff',
                            },
                            'type': 'matrix',
                        },
                        'rows': [
                            {
                                'help': {
                                    'en': 'Help',
                                },
                                'text': {
                                    'en': 'Row 1',
                                },
                                'id': 'row1',
                            },
                            {
                                'audio': {
                                    'en': [
                                        '/foo',
                                        '/bar',
                                    ],
                                },
                                'text': {
                                    'en': 'Row 2',
                                },
                                'id': 'row2',
                            },
                        ],
                        'fieldId': 'field1',
                    },
                }
            ],
        },
        {
            'id': 'page2',
            'elements': [
                {
                    'type': 'question',
                    'options': {
                        'events': [
                            {
                                'action': 'hide',
                                'targets': [
                                    'foo',
                                ],
                                'trigger': 'is_null(field2)'
                            },
                            {
                                'action': 'fail',
                                'options': {
                                    'text': {
                                        'en': 'Failed'
                                    },
                                },
                                'targets': [
                                    'field1',
                                ],
                                'trigger': '!is_null(field2)'
                            },
                        ],
                        'text': {
                            'en': 'Question 2',
                        },
                        'fieldId': 'field2',
                    },
                },
            ],
        },
    ],
    "defaultLocalization": "en",
    'meta': {
        'zcustom': 123,
        'author': 'John Smith',
    },
    'parameters': {
        'zzz': {
            'type': 'text',
        },
        'aaa': {
            'type': 'boolean',
        },
    },
    "title": {
        "en": "Form Title",
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
  "defaultLocalization": "en",
  "title": {
    "en": "Form Title"
  },
  "pages": [
    {
      "id": "page1",
      "elements": [
        {
          "type": "header",
          "options": {
            "text": {
              "en": "A Header"
            }
          }
        },
        {
          "type": "divider",
          "tags": [
            "foo",
            "bar"
          ]
        },
        {
          "type": "question",
          "options": {
            "fieldId": "field1",
            "text": {
              "en": "Question 1",
              "fr": "French Question 1"
            },
            "help": {
              "en": "Some Help"
            },
            "questions": [
              {
                "fieldId": "subfield",
                "text": {
                  "en": "SubField"
                }
              }
            ],
            "rows": [
              {
                "id": "row1",
                "text": {
                  "en": "Row 1"
                },
                "help": {
                  "en": "Help"
                }
              },
              {
                "id": "row2",
                "text": {
                  "en": "Row 2"
                },
                "audio": {
                  "en": [
                    "/foo",
                    "/bar"
                  ]
                }
              }
            ],
            "widget": {
              "type": "matrix",
              "options": {
                "baz": "stuff",
                "foo": "bar"
              }
            }
          }
        }
      ]
    },
    {
      "id": "page2",
      "elements": [
        {
          "type": "question",
          "options": {
            "fieldId": "field2",
            "text": {
              "en": "Question 2"
            },
            "events": [
              {
                "trigger": "is_null(field2)",
                "action": "hide",
                "targets": [
                  "foo"
                ]
              },
              {
                "trigger": "!is_null(field2)",
                "action": "fail",
                "targets": [
                  "field1"
                ],
                "options": {
                  "text": {
                    "en": "Failed"
                  }
                }
              }
            ]
          }
        }
      ]
    }
  ],
  "parameters": {
    "aaa": {
      "type": "boolean"
    },
    "zzz": {
      "type": "text"
    }
  }
}"""


def test_output_json():
    actual = get_form_json(FORM, pretty=True)
    assert actual == EXPECTED_JSON, actual


EXPECTED_YAML = '''instrument:
  id: urn:some-test
  version: '1.0'
meta:
  author: John Smith
  zcustom: 123
defaultLocalization: en
title:
  en: Form Title
pages:
- id: page1
  elements:
  - type: header
    options:
      text:
        en: A Header
  - type: divider
    tags:
    - foo
    - bar
  - type: question
    options:
      fieldId: field1
      text:
        en: Question 1
        fr: French Question 1
      help:
        en: Some Help
      questions:
      - fieldId: subfield
        text:
          en: SubField
      rows:
      - id: row1
        text:
          en: Row 1
        help:
          en: Help
      - id: row2
        text:
          en: Row 2
        audio:
          en:
          - /foo
          - /bar
      widget:
        type: matrix
        options:
          baz: stuff
          foo: bar
- id: page2
  elements:
  - type: question
    options:
      fieldId: field2
      text:
        en: Question 2
      events:
      - trigger: is_null(field2)
        action: hide
        targets:
        - foo
      - trigger: '!is_null(field2)'
        action: fail
        targets:
        - field1
        options:
          text:
            en: Failed
parameters:
  aaa:
    type: boolean
  zzz:
    type: text'''


def test_output_yaml():
    actual = get_form_yaml(FORM, pretty=True)
    assert actual == EXPECTED_YAML, actual

