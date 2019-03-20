#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json
import os

from copy import deepcopy

from rios.core.validation.assessment import Assessment, ValidationError

from utils import *


GOOD_ASSESSMENT_FILES = os.path.join(EXAMPLE_FILES, 'assessments/good')
BAD_ASSESSMENT_FILES = os.path.join(EXAMPLE_FILES, 'assessments/bad')


def test_good_files():
    for dirpath, dirnames, filenames in os.walk(GOOD_ASSESSMENT_FILES):
        for filename in filenames:
            yield check_good_validation, Assessment(), os.path.join(GOOD_ASSESSMENT_FILES, filename)


def test_bad_files():
    for dirpath, dirnames, filenames in os.walk(BAD_ASSESSMENT_FILES):
        for filename in filenames:
            yield check_bad_validation, Assessment(), os.path.join(BAD_ASSESSMENT_FILES, filename)



INSTRUMENT = json.load(open(os.path.join(EXAMPLE_FILES, 'instruments/good/all_types.json'), 'r'))
ASSESSMENT = json.load(open(os.path.join(EXAMPLE_FILES, 'assessments/good/all_value_types.json'), 'r'))
ASSESSMENT2 = json.load(open(os.path.join(EXAMPLE_FILES, 'assessments/good/all_nulls.json'), 'r'))


def test_good_instrument_validation():
    validator = Assessment(instrument=INSTRUMENT)
    validator.deserialize(ASSESSMENT)
    validator.deserialize(ASSESSMENT2)


def test_bad_instrument_id_reference():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['instrument']['id'] = 'urn:something-else'
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'instrument': 'Incorrect Instrument version referenced'},
        )
    else:
        assert False


def test_bad_instrument_version_reference():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['instrument']['version'] = '2.0'
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'instrument': 'Incorrect Instrument version referenced'},
        )
    else:
        assert False


def test_missing_field():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values'].pop('text_field')
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'No value exists for field ID "text_field"'},
        )
    else:
        assert False


def test_extra_field():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['extra_field'] = {
        'value': 42
    }
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'Unknown field IDs found: extra_field'},
        )
    else:
        assert False


def test_missing_recordlist_field():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['recordlist_field']['value'][0].pop('subfield1')
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'No value exists for field ID "subfield1"'},
        )
    else:
        assert False


def test_missing_matrix_row():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['matrix_field']['value'].pop('row2')
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'Missing values for row ID "row2"'},
        )
    else:
        assert False


def test_missing_matrix_column():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['matrix_field']['value']['row2'].pop('col2')
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': u'Row ID "row2" is missing values for columns: col2'},
        )
    else:
        assert False


def test_extra_row():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['matrix_field']['value']['extra_row'] = {
            'col1': {
                'value': 'foo'
            },
            'col2': {
                'value': 'bar'
            }
    }
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'Unknown row IDs found: extra_row'},
        )
    else:
        assert False


def test_extra_column():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['matrix_field']['value']['row2']['fake'] = {'value': 'foo'}
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': u'Row ID "row2" contains unknown column IDs: fake'}
        )
    else:
        assert False


def test_required_row():
    instrument = deepcopy(INSTRUMENT)
    instrument['record'][11]['type']['rows'][0]['required'] = True
    validator = Assessment(instrument=instrument)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['matrix_field']['value']['row1']['col1'] = {'value': None}
    assessment['values']['matrix_field']['value']['row1']['col2'] = {'value': None}
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': u'Row ID "row1" requires at least one column with a value'}
        )
    else:
        assert False


def test_required_column():
    instrument = deepcopy(INSTRUMENT)
    instrument['record'][11]['type']['columns'][0]['required'] = True
    validator = Assessment(instrument=instrument)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['matrix_field']['value']['row1']['col1'] = {'value': None}
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': u'Row ID "row1" is missing values for columns: col1'}
        )
    else:
        assert False

    assessment['values']['matrix_field']['value']['row1']['col1'] = {'value': 'foo'}
    assessment['values']['matrix_field']['value']['row1']['col2'] = {'value': None}
    validator.deserialize(assessment)

def test_required_value():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['boolean_field']['value'] = None
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'No value present for required field ID "boolean_field"'},
        )
    else:
        assert False


def test_undesired_explanation():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['float_field']['explanation'] = 'foo'
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'Explanation present where not allowed in field ID "float_field"'},
        )
    else:
        assert False


def test_required_explanation():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    del assessment['values']['integer_field']['explanation']
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'Explanation missing for field ID "integer_field"'},
        )
    else:
        assert False


def test_undesired_annotation():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['date_field']['annotation'] = 'foo'
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'Annotation present where not allowed: date_field'},
        )
    else:
        assert False


def test_undesired_annotation2():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['float_field']['annotation'] = 'foo'
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'Annotation provided for non-empty value: float_field'},
        )
    else:
        assert False


def test_required_annotation():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['float_field']['value'] = None
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'Annotation missing for field ID "float_field"'},
        )
    else:
        assert False


BAD_VALUE_TESTS = (
    ('text_field', 42, None),
    ('integer_field', 'foo', None),
    ('float_field', 'foo', None),
    ('enumeration_field', False, None),
    ('boolean_field', 42, None),
    ('date_field', '5/22/2015', None),
    ('time_field', 13231123, None),
    ('datetime_field', 'foo', None),
    ('enumerationset_field', 42, None),
    ('enumerationset_field', [{'blah': {'value': None}}], None),
    ('recordlist_field', 42, None),
    ('recordlist_field', [{'subfield1': {'value': 42}, 'subfield2': {'value': 'foo'}}], 'subfield1'),
    ('matrix_field', 'foo', None),
    ('matrix_field', {"row1": {"col1": {"value": False},"col2": {"value": "bar1"}},"row2": {"col1": {"value": "foo2"},"col2": {"value": "bar2"}}}, 'col1'),
)

def check_bad_value_type(field_id, bad_value, sub_field_id=None):
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values'][field_id]['value'] = bad_value
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        msg = 'Value for "%s" is not of the correct type' % (
            sub_field_id or field_id,
        )
        if msg not in str(exc):
            raise
        assert msg in str(exc)
    else:
        assert False

def test_bad_value_types():
    for field_id, bad_value, sub_field_id in BAD_VALUE_TESTS:
        yield check_bad_value_type, field_id, bad_value, sub_field_id


def test_bad_enumeration_choice():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['enumeration_field']['value'] = 'wrong'
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'Value for "enumeration_field" is not an accepted enumeration'},
        )
    else:
        assert False


def test_bad_enumerationset_choice():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['enumerationset_field']['value'] = ['wrong']
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'Value for "enumerationset_field" is not an accepted enumeration'},
        )
    else:
        assert False

