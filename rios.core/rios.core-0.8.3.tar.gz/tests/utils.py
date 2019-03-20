from __future__ import print_function

import json
import os

from six import PY3

from rios.core.validation.common import ValidationError


__all__ = (
    'EXAMPLE_FILES',
    'FAILURES',
    'check_good_validation',
    'check_bad_validation',
    'assert_validation_error',
)


EXAMPLE_FILES = os.path.join(os.path.dirname(__file__), 'examples')
FAILURES = json.load(open(os.path.join(EXAMPLE_FILES, 'failures.json')))
FAILURE_EXCEPTIONS = json.load(open(os.path.join(EXAMPLE_FILES, 'failure_exceptions.json')))


def check_good_validation(validator, filename):
    file_contents = open(filename, 'r').read()
    file_structure = json.loads(file_contents)
    validator.deserialize(file_structure)


def check_bad_validation(validator, filename):
    file_contents = open(filename, 'r').read()
    file_structure = json.loads(file_contents)
    filename = os.path.relpath(filename, EXAMPLE_FILES)
    try:
        validator.deserialize(file_structure)
    except ValidationError as exc:
        if filename not in FAILURES:
            print(filename, exc)
        else:
            expected = FAILURES[filename]
            actual = exc.asdict()
            for key, value in list(expected.items()):
                if key in actual:
                    key_actual = actual.pop(key)
                    key_expected = expected[key]
                    if PY3:
                        # %r under PY3 doesn't output the old "u" unicode marker
                        key_expected = key_expected.replace("u'", "'")
                    assert key_expected == key_actual, 'Expected "%s" to have "%s", got "%s"' % (key, key_expected, key_actual)
                else:
                    assert False, 'Expected failure for %s: %s' % (key, exc)
            if actual:
                assert False, 'Got unexpected failures: "%s"' % (actual,)

    else:
        if PY3:
            if filename in FAILURE_EXCEPTIONS['PY3']:
                return
        assert False, '%s did not fail validation' % filename


def assert_validation_error(exc, expected):
    actual = exc.asdict()
    if actual != expected:
        raise AssertionError(
            'Expected %r but got %r' % (
                expected,
                actual,
            )
        )

