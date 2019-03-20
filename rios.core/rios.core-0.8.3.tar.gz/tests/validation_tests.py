#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json
import os

from rios.core.validation import *


INSTRUMENT_FILE = os.path.join(os.path.dirname(__file__), 'examples/instruments/good/text.json')
CALCULATION_FILE = os.path.join(os.path.dirname(__file__), 'examples/calculationsets/good/text.json')
ASSESSMENT_FILE = os.path.join(os.path.dirname(__file__), 'examples/assessments/good/text.json')
FORM_FILE = os.path.join(os.path.dirname(__file__), 'examples/forms/good/text.json')
INTERACTION_FILE = os.path.join(os.path.dirname(__file__), 'examples/interactions/good/text.json')



INSTRUMENT_TESTS = (
    open(INSTRUMENT_FILE, 'r'),
    open(INSTRUMENT_FILE, 'r').read(),
    json.load(open(INSTRUMENT_FILE, 'r')),
)

def test_instrument_validation():
    for instrument in INSTRUMENT_TESTS:
        yield validate_instrument, instrument


ASSESSMENT_TESTS = (
    (open(ASSESSMENT_FILE, 'r'), None),
    (open(ASSESSMENT_FILE, 'r'), open(INSTRUMENT_FILE, 'r')),
    (open(ASSESSMENT_FILE, 'r'), open(INSTRUMENT_FILE, 'r').read()),
    (open(ASSESSMENT_FILE, 'r'), json.load(open(INSTRUMENT_FILE, 'r'))),

    (open(ASSESSMENT_FILE, 'r').read(), None),
    (open(ASSESSMENT_FILE, 'r').read(), open(INSTRUMENT_FILE, 'r')),
    (open(ASSESSMENT_FILE, 'r').read(), open(INSTRUMENT_FILE, 'r').read()),
    (open(ASSESSMENT_FILE, 'r').read(), json.load(open(INSTRUMENT_FILE, 'r'))),

    (json.load(open(ASSESSMENT_FILE, 'r')), None),
    (json.load(open(ASSESSMENT_FILE, 'r')), open(INSTRUMENT_FILE, 'r')),
    (json.load(open(ASSESSMENT_FILE, 'r')), open(INSTRUMENT_FILE, 'r').read()),
    (json.load(open(ASSESSMENT_FILE, 'r')), json.load(open(INSTRUMENT_FILE, 'r'))),
)

def test_assessment_validation():
    for assessment, instrument in ASSESSMENT_TESTS:
        yield validate_assessment, assessment, instrument


FORM_TESTS = (
    (open(FORM_FILE, 'r'), None),
    (open(FORM_FILE, 'r'), open(INSTRUMENT_FILE, 'r')),
    (open(FORM_FILE, 'r'), open(INSTRUMENT_FILE, 'r').read()),
    (open(FORM_FILE, 'r'), json.load(open(INSTRUMENT_FILE, 'r'))),

    (open(FORM_FILE, 'r').read(), None),
    (open(FORM_FILE, 'r').read(), open(INSTRUMENT_FILE, 'r')),
    (open(FORM_FILE, 'r').read(), open(INSTRUMENT_FILE, 'r').read()),
    (open(FORM_FILE, 'r').read(), json.load(open(INSTRUMENT_FILE, 'r'))),

    (json.load(open(FORM_FILE, 'r')), None),
    (json.load(open(FORM_FILE, 'r')), open(INSTRUMENT_FILE, 'r')),
    (json.load(open(FORM_FILE, 'r')), open(INSTRUMENT_FILE, 'r').read()),
    (json.load(open(FORM_FILE, 'r')), json.load(open(INSTRUMENT_FILE, 'r'))),
)

def test_form_validation():
    for form, instrument in FORM_TESTS:
        yield validate_form, form, instrument


INTERACTION_TESTS = (
    (open(INTERACTION_FILE, 'r'), None),
    (open(INTERACTION_FILE, 'r'), open(INSTRUMENT_FILE, 'r')),
    (open(INTERACTION_FILE, 'r'), open(INSTRUMENT_FILE, 'r').read()),
    (open(INTERACTION_FILE, 'r'), json.load(open(INSTRUMENT_FILE, 'r'))),

    (open(INTERACTION_FILE, 'r').read(), None),
    (open(INTERACTION_FILE, 'r').read(), open(INSTRUMENT_FILE, 'r')),
    (open(INTERACTION_FILE, 'r').read(), open(INSTRUMENT_FILE, 'r').read()),
    (open(INTERACTION_FILE, 'r').read(), json.load(open(INSTRUMENT_FILE, 'r'))),

    (json.load(open(INTERACTION_FILE, 'r')), None),
    (json.load(open(INTERACTION_FILE, 'r')), open(INSTRUMENT_FILE, 'r')),
    (json.load(open(INTERACTION_FILE, 'r')), open(INSTRUMENT_FILE, 'r').read()),
    (json.load(open(INTERACTION_FILE, 'r')), json.load(open(INSTRUMENT_FILE, 'r'))),
)

def test_interaction_validation():
    for interaction, instrument in INTERACTION_TESTS:
        yield validate_interaction, interaction, instrument


CALCULATION_TESTS = (
    (open(CALCULATION_FILE, 'r'), None),
    (open(CALCULATION_FILE, 'r'), open(INSTRUMENT_FILE, 'r')),
    (open(CALCULATION_FILE, 'r'), open(INSTRUMENT_FILE, 'r').read()),
    (open(CALCULATION_FILE, 'r'), json.load(open(INSTRUMENT_FILE, 'r'))),

    (open(CALCULATION_FILE, 'r').read(), None),
    (open(CALCULATION_FILE, 'r').read(), open(INSTRUMENT_FILE, 'r')),
    (open(CALCULATION_FILE, 'r').read(), open(INSTRUMENT_FILE, 'r').read()),
    (open(CALCULATION_FILE, 'r').read(), json.load(open(INSTRUMENT_FILE, 'r'))),

    (json.load(open(CALCULATION_FILE, 'r')), None),
    (json.load(open(CALCULATION_FILE, 'r')), open(INSTRUMENT_FILE, 'r')),
    (json.load(open(CALCULATION_FILE, 'r')), open(INSTRUMENT_FILE, 'r').read()),
    (json.load(open(CALCULATION_FILE, 'r')), json.load(open(INSTRUMENT_FILE, 'r'))),
)

def test_calculation_validation():
    for calculation, instrument in CALCULATION_TESTS:
        yield validate_calculationset, calculation, instrument

