#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json
import os

from copy import deepcopy

from rios.core.validation.calculationset import CalculationSet, \
    ValidationError

from utils import *


GOOD_CALCULATION_FILES = os.path.join(EXAMPLE_FILES, 'calculationsets/good')
BAD_CALCULATION_FILES = os.path.join(EXAMPLE_FILES, 'calculationsets/bad')


def test_good_files():
    for dirpath, dirnames, filenames in os.walk(GOOD_CALCULATION_FILES):
        for filename in filenames:
            yield check_good_validation, CalculationSet(), os.path.join(
                GOOD_CALCULATION_FILES,
                filename,
            )


def test_bad_files():
    for dirpath, dirnames, filenames in os.walk(BAD_CALCULATION_FILES):
        for filename in filenames:
            yield check_bad_validation, CalculationSet(), os.path.join(
                BAD_CALCULATION_FILES,
                filename,
            )


INSTRUMENT = json.load(open(os.path.join(EXAMPLE_FILES, 'instruments/good/all_types.json'), 'r'))
CALCULATION = json.load(open(os.path.join(EXAMPLE_FILES, 'calculationsets/good/all_types.json'), 'r'))


def test_good_instrument_validation():
    validator = CalculationSet(instrument=INSTRUMENT)
    validator.deserialize(CALCULATION)


def test_bad_instrument_id_reference():
    validator = CalculationSet(instrument=INSTRUMENT)
    calculation = deepcopy(CALCULATION)
    calculation['instrument']['id'] = 'urn:something-else'
    try:
        validator.deserialize(calculation)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'instrument': 'Incorrect Instrument version referenced'},
        )
    else:
        assert False


def test_bad_instrument_version_reference():
    validator = CalculationSet(instrument=INSTRUMENT)
    calculation = deepcopy(CALCULATION)
    calculation['instrument']['version'] = '2.0'
    try:
        validator.deserialize(calculation)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'instrument': 'Incorrect Instrument version referenced'},
        )
    else:
        assert False


def test_duped_instrument_field_id():
    validator = CalculationSet(instrument=INSTRUMENT)
    calculation = deepcopy(CALCULATION)
    calculation['calculations'][0]['id'] = 'text_field'
    try:
        validator.deserialize(calculation)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'calculations': 'Calculation IDs cannot be the same as Instrument Field IDs: text_field'},
        )
    else:
        assert False

