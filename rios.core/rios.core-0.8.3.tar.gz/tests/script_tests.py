#
# Copyright (c) 2015, Prometheus Research, LLC
#


import os

from six import StringIO

from rios.core.scripts import validate

from utils import EXAMPLE_FILES


def run_validate(args, expected, exit=0):
    actual = StringIO()
    actual_exit = validate(args, stdout=actual)
    assert actual.getvalue().strip() == expected, actual.getvalue()
    assert actual_exit == exit, actual_exit


def test_validate_good_instrument():
    run_validate(
        ['instrument', os.path.join(EXAMPLE_FILES, 'instruments/good/all_types.json')],
        'Successful validation.',
    )


def test_validate_bad_instrument():
    run_validate(
        ['instrument', os.path.join(EXAMPLE_FILES, 'instruments/bad/title_missing.json')],
        'FAILED validation.\ntitle: Required',
        exit=1,
    )


def test_validate_form():
    run_validate(
        ['form', os.path.join(EXAMPLE_FILES, 'forms/good/all_types.json')],
        'Successful validation.',
    )


def test_validate_form_with_instrument():
    run_validate(
        [
            'form',
            os.path.join(EXAMPLE_FILES, 'forms/good/all_types.json'),
            '-i',
            os.path.join(EXAMPLE_FILES, 'instruments/good/all_types.json'),
        ],
        'Successful validation.',
    )

