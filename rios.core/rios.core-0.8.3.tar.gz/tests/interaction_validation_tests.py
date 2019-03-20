#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json
import os

from copy import deepcopy

from rios.core.validation.interaction import Interaction, ValidationError

from utils import *


GOOD_INTERACTION_FILES = os.path.join(EXAMPLE_FILES, 'interactions/good')
BAD_INTERACTION_FILES = os.path.join(EXAMPLE_FILES, 'interactions/bad')


def test_good_files():
    for dirpath, dirnames, filenames in os.walk(GOOD_INTERACTION_FILES):
        for filename in filenames:
            yield check_good_validation, Interaction(), os.path.join(
                GOOD_INTERACTION_FILES,
                filename,
            )


def test_bad_files():
    for dirpath, dirnames, filenames in os.walk(BAD_INTERACTION_FILES):
        for filename in filenames:
            yield check_bad_validation, Interaction(), os.path.join(
                BAD_INTERACTION_FILES,
                filename,
            )


INSTRUMENT = json.load(open(os.path.join(EXAMPLE_FILES, 'instruments/good/all_interaction_types.json'), 'r'))
INTERACTION = json.load(open(os.path.join(EXAMPLE_FILES, 'interactions/good/all_types.json'), 'r'))


def test_good_instrument_validation():
    validator = Interaction(instrument=INSTRUMENT)
    validator.deserialize(INTERACTION)


def test_bad_instrument_id_reference():
    validator = Interaction(instrument=INSTRUMENT)
    interaction = deepcopy(INTERACTION)
    interaction['instrument']['id'] = 'urn:something-else'
    try:
        validator.deserialize(interaction)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'instrument': 'Incorrect Instrument version referenced'},
        )
    else:
        assert False


def test_bad_instrument_version_reference():
    validator = Interaction(instrument=INSTRUMENT)
    interaction = deepcopy(INTERACTION)
    interaction['instrument']['version'] = '2.0'
    try:
        validator.deserialize(interaction)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'instrument': 'Incorrect Instrument version referenced'},
        )
    else:
        assert False


def test_missing_field():
    validator = Interaction(instrument=INSTRUMENT)
    interaction = deepcopy(INTERACTION)
    interaction['steps'].pop()
    try:
        validator.deserialize(interaction)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'steps': 'There are Instrument fields which are missing: enumerationset_field'},
        )
    else:
        assert False


def test_extra_field():
    validator = Interaction(instrument=INSTRUMENT)
    interaction = deepcopy(INTERACTION)
    interaction['steps'].append({
        'type': 'question',
        'options': {
            'fieldId': 'extra_field',
            'text': {
                'en': 'Extra!'
            }
        }
    })
    try:
        validator.deserialize(interaction)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'steps': 'There are extra fields referenced by questions: extra_field'},
        )
    else:
        assert False


def test_duplicate_field():
    validator = Interaction(instrument=INSTRUMENT)
    interaction = deepcopy(INTERACTION)
    interaction['steps'].append(interaction['steps'][1])
    try:
        validator.deserialize(interaction)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'steps': 'Field "nullable_field" is addressed by more than one question'},
        )
    else:
        assert False


def test_unnecessary_enumeration_field():
    validator = Interaction(instrument=INSTRUMENT)
    interaction = deepcopy(INTERACTION)
    interaction['steps'][1]['options']['enumerations'] = [
        {
            'id': 'foo',
            'text': {
                'en': 'Unnecessary'
            }
        }
    ]
    try:
        validator.deserialize(interaction)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'steps.1.options': 'Field "nullable_field" cannot have an enumerations configuration'},
        )
    else:
        assert False


def test_complex_field():
    instrument = deepcopy(INSTRUMENT)
    instrument['record'][0]['type'] = {
        'base': 'recordList',
        'record': [
            {
                'id': 'foo',
                'type': 'text'
            }
        ]
    }
    validator = Interaction(instrument=instrument)
    try:
        validator.deserialize(INTERACTION)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'steps.1.options': 'Complex Instrument Types are not allowed in Interactions'},
        )
    else:
        assert False


def test_bad_enumeration_desc():
    validator = Interaction(instrument=INSTRUMENT)
    interaction = deepcopy(INTERACTION)
    interaction['steps'][9]['options']['enumerations'][0]['id'] = 'wrong'
    try:
        validator.deserialize(interaction)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'steps.9.options': 'Field "enumeration_field" describes an invalid enumeration "wrong"'},
        )
    else:
        assert False


def test_bad_enumerationset_desc():
    validator = Interaction(instrument=INSTRUMENT)
    interaction = deepcopy(INTERACTION)
    interaction['steps'][10]['options']['enumerations'][0]['id'] = 'wrong'
    try:
        validator.deserialize(interaction)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'steps.10.options': 'Field "enumerationset_field" describes an invalid enumeration "wrong"'},
        )
    else:
        assert False

