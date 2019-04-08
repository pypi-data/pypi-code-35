# pylint: disable=invalid-name
import re

import pytest

from monads import Function, identity


def randint():
    from random import randint as r
    return r(-1000, 1000)


ITERATIONS = 100
RANDOM_VALUES = [randint() for _ in range(ITERATIONS)]
RANDOM_DOUBLES = [(randint(), randint()) for _ in range(ITERATIONS)]


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_function_identity_composition(value):
    """ f == f * id """
    function = Function(lambda v: v * v)
    composed = function.compose(identity)

    assert function(value) == composed(value)


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_function_composition_equivalence(value):
    """ (f * g) * h == f * (g * h) """
    f = Function(lambda v: v * v)
    g = Function(lambda v: v + v)
    h = Function(lambda v: v - 1)

    fg_h = (f * g) * h
    f_gh = f * (g * h)

    assert fg_h(value) == f_gh(value)


def test_function_stringification():
    def named_function(v):
        return v

    f = Function(named_function)

    assert re.match(r'Function\(<[^)]+>\)', str(f)) is not None
