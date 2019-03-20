#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json
import os

import six

from rios.core.output import *


INSTRUMENT_FILE = os.path.join(os.path.dirname(__file__), 'examples/instruments/good/text.json')
CALCULATION_FILE = os.path.join(os.path.dirname(__file__), 'examples/calculationsets/good/text.json')
ASSESSMENT_FILE = os.path.join(os.path.dirname(__file__), 'examples/assessments/good/text.json')
FORM_FILE = os.path.join(os.path.dirname(__file__), 'examples/forms/good/text.json')
INTERACTION_FILE = os.path.join(os.path.dirname(__file__), 'examples/interactions/good/text.json')

TESTS = (
    (get_instrument_json, open(INSTRUMENT_FILE, 'r')),
    (get_instrument_json, open(INSTRUMENT_FILE, 'r').read()),
    (get_instrument_json, json.load(open(INSTRUMENT_FILE, 'r'))),
    (get_instrument_yaml, open(INSTRUMENT_FILE, 'r')),
    (get_instrument_yaml, open(INSTRUMENT_FILE, 'r').read()),
    (get_instrument_yaml, json.load(open(INSTRUMENT_FILE, 'r'))),

    (get_calculationset_json, open(CALCULATION_FILE, 'r')),
    (get_calculationset_json, open(CALCULATION_FILE, 'r').read()),
    (get_calculationset_json, json.load(open(CALCULATION_FILE, 'r'))),
    (get_calculationset_yaml, open(CALCULATION_FILE, 'r')),
    (get_calculationset_yaml, open(CALCULATION_FILE, 'r').read()),
    (get_calculationset_yaml, json.load(open(CALCULATION_FILE, 'r'))),

    (get_assessment_json, open(ASSESSMENT_FILE, 'r')),
    (get_assessment_json, open(ASSESSMENT_FILE, 'r').read()),
    (get_assessment_json, json.load(open(ASSESSMENT_FILE, 'r'))),
    (get_assessment_yaml, open(ASSESSMENT_FILE, 'r')),
    (get_assessment_yaml, open(ASSESSMENT_FILE, 'r').read()),
    (get_assessment_yaml, json.load(open(ASSESSMENT_FILE, 'r'))),

    (get_form_json, open(FORM_FILE, 'r')),
    (get_form_json, open(FORM_FILE, 'r').read()),
    (get_form_json, json.load(open(FORM_FILE, 'r'))),
    (get_form_yaml, open(FORM_FILE, 'r')),
    (get_form_yaml, open(FORM_FILE, 'r').read()),
    (get_form_yaml, json.load(open(FORM_FILE, 'r'))),

    (get_interaction_json, open(INTERACTION_FILE, 'r')),
    (get_interaction_json, open(INTERACTION_FILE, 'r').read()),
    (get_interaction_json, json.load(open(INTERACTION_FILE, 'r'))),
    (get_interaction_yaml, open(INTERACTION_FILE, 'r')),
    (get_interaction_yaml, open(INTERACTION_FILE, 'r').read()),
    (get_interaction_yaml, json.load(open(INTERACTION_FILE, 'r'))),
)


def check_output(func, obj):
    output = func(obj)
    assert isinstance(output, six.string_types), type(output)
    assert len(output) > 0

def test_output():
    for func, obj in TESTS:
        yield check_output, func, obj

