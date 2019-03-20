#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json
import os

from copy import deepcopy

from rios.core.validation.form import Form, ValidationError

from utils import *


GOOD_FORM_FILES = os.path.join(EXAMPLE_FILES, 'forms/good')
BAD_FORM_FILES = os.path.join(EXAMPLE_FILES, 'forms/bad')


def test_good_files():
    for dirpath, dirnames, filenames in os.walk(GOOD_FORM_FILES):
        for filename in filenames:
            yield check_good_validation, Form(), os.path.join(GOOD_FORM_FILES, filename)


def test_bad_files():
    for dirpath, dirnames, filenames in os.walk(BAD_FORM_FILES):
        for filename in filenames:
            yield check_bad_validation, Form(), os.path.join(BAD_FORM_FILES, filename)


INSTRUMENT = json.load(open(os.path.join(EXAMPLE_FILES, 'instruments/good/all_types.json'), 'r'))
FORM = json.load(open(os.path.join(EXAMPLE_FILES, 'forms/good/all_types.json'), 'r'))
MATRIX_INSTRUMENT = json.load(open(os.path.join(EXAMPLE_FILES, 'instruments/good/matrix.json'), 'r'))
MATRIX_FORM = json.load(open(os.path.join(EXAMPLE_FILES, 'forms/good/matrix.json'), 'r'))


def test_good_instrument_validation():
    validator = Form(instrument=INSTRUMENT)
    validator.deserialize(FORM)


def test_bad_instrument_id_reference():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['instrument']['id'] = 'urn:something-else'
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'instrument': 'Incorrect Instrument version referenced'},
        )
    else:
        assert False


def test_bad_instrument_version_reference():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['instrument']['version'] = '2.0'
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'instrument': 'Incorrect Instrument version referenced'},
        )
    else:
        assert False


def test_missing_field():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][0]['elements'].pop()
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'': 'There are Instrument fields which are missing: datetime_field'},
        )
    else:
        assert False


def test_extra_field():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][0]['elements'].append({
        'type': 'question',
        'options': {
            'fieldId': 'extra_field',
            'text': {
                'en': 'Extra!'
            }
        }
    })
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'': 'There are extra fields referenced by questions: extra_field'},
        )
    else:
        assert False


def test_duplicate_field():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][0]['elements'].append(form['pages'][0]['elements'][-1])
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'pages.0.elements.12': 'Field "datetime_field" is addressed by more than one question'},
        )
    else:
        assert False


def test_unnecessary_enumeration_field():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][0]['elements'][-1]['options']['enumerations'] = [
        {
            'id': 'foo',
            'text': {
                'en': 'Unnecessary'
            }
        }
    ]
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'pages.0.elements.11.options': 'Field "datetime_field" cannot have an enumerations configuration'},
        )
    else:
        assert False


def test_missing_row():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][3]['options']['rows'].pop()
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'pages.1.elements.3.options': 'There are missing rows in matrix_field: row2'},
        )
    else:
        assert False


def test_duplicate_row():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][3]['options']['rows'][1]['id'] = 'row1'
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'pages.1.elements.3.options': 'Row row1 is addressed by more than one descriptor in matrix_field'},
        )
    else:
        assert False


def test_extra_row():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][3]['options']['rows'].append({
        'id': 'extra',
        'text': {
            'en': 'Extra!',
        },
    })
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'pages.1.elements.3.options': 'There are extra rows referenced by matrix_field: extra'},
        )
    else:
        assert False


def test_unnecessary_row():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][0]['elements'][-1]['options']['rows'] = [
        {
            'id': 'foo',
            'text': {
                'en': 'Foo'
            }
        }
    ]
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'pages.0.elements.11.options': 'Field "datetime_field" cannot have a rows configuration'},
        )
    else:
        assert False


def test_missing_column():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][3]['options']['questions'].pop()
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'pages.1.elements.3.options': 'There are missing subfields in matrix_field: col1'},
        )
    else:
        assert False


def test_duplicate_column():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][3]['options']['questions'][0]['fieldId'] = 'col1'
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'pages.1.elements.3.options': 'Subfield col1 is addressed by more than one question in matrix_field'},
        )
    else:
        assert False


def test_extra_column():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][3]['options']['questions'].append({
        'fieldId': 'extra',
        'text': {
            'en': 'Extra!',
        },
    })
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'pages.1.elements.3.options': 'There are extra subfields referenced by matrix_field: extra'},
        )
    else:
        assert False


def test_missing_question():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][2]['options']['questions'].pop()
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'pages.1.elements.2.options': 'There are missing subfields in recordlist_field: subfield1'},
        )
    else:
        assert False


def test_duplicate_question():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][2]['options']['questions'][0]['fieldId'] = 'subfield1'
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'pages.1.elements.2.options': 'Subfield subfield1 is addressed by more than one question in recordlist_field'},
        )
    else:
        assert False


def test_extra_question():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][2]['options']['questions'].append({
        'fieldId': 'extra',
        'text': {
            'en': 'Extra!',
        },
    })
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'pages.1.elements.2.options': 'There are extra subfields referenced by recordlist_field: extra'},
        )
    else:
        assert False


def test_unnecessary_question():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][0]['elements'][-1]['options']['questions'] = [
        {
            'fieldId': 'foo',
            'text': {
                'en': 'Foo'
            }
        }
    ]
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'pages.0.elements.11.options': 'Field "datetime_field" cannot have a questions configuration'},
        )
    else:
        assert False


def test_bad_enumeration_desc():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][0]['options']['enumerations'][0]['id'] = 'wrong'
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'pages.1.elements.0.options': 'Field "enumeration_field" describes an invalid enumeration "wrong"'},
        )
    else:
        assert False


def test_bad_enumerationset_desc():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][1]['options']['enumerations'][0]['id'] = 'wrong'
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'pages.1.elements.1.options': 'Field "enumerationset_field" describes an invalid enumeration "wrong"'},
        )
    else:
        assert False


def test_bad_deep_enumeration_desc():
    validator = Form(instrument=MATRIX_INSTRUMENT)
    form = deepcopy(MATRIX_FORM)
    form['pages'][0]['elements'][0]['options']['questions'][0]['enumerations'][0]['id'] = 'wrong'
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'pages.0.elements.0.options': 'Field "col1" describes an invalid enumeration "wrong"'},
        )
    else:
        assert False


def test_nonunique_tag():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][0]['tags'] = ['text_field', 'page1']
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'pages.1.elements.0.tags': 'Tag(s) are duplicates of existing identifiers: page1, text_field'},
        )
    else:
        assert False


def test_custom_widget():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][0]['elements'][4]['options']['widget']['type'] = 'myCustomWidget'
    validator.deserialize(form)


def test_wrong_standard_widget():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][0]['elements'][4]['options']['widget']['type'] = 'radioGroup'
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'pages.0.elements.4.options': u'Standard widget "radioGroup" cannot be used with fields of type "text"'},
        )
    else:
        assert False

