# pylint: disable=invalid-name
import pytest

import monads


def randint():
    from random import randint as r
    return r(-1000, 1000)


ITERATIONS = 100
RANDOM_VALUES = [randint() for _ in range(ITERATIONS)]
RANDOM_DOUBLES = [(randint(), randint()) for _ in range(ITERATIONS)]


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_functor_identity_preservation(value):
    """ fmap id == id """
    functor = monads.Either.lift(value)

    fmap_id = functor > monads.identity  # pylint: disable=comparison-with-callable
    identity = monads.identity(functor)

    assert fmap_id == identity


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_functor_composition_preservation(value):
    """ fmap (f * g) == fmap f * fmap g """
    f = monads.Function(lambda v: v * v)
    g = monads.Function(lambda v: v + v)
    functor = monads.Either.lift(value)

    left = functor > f * g
    right = (functor > f) > g
    assert left == right


@pytest.mark.parametrize("original,value", RANDOM_DOUBLES)
def test_functor_replacement(original, value):
    """ f a < b == f b """
    functor = monads.Either.lift(original)

    replacement = functor < value

    assert replacement == monads.Either.lift(value)


def test_functor_fmap_missing():
    f = monads.Function(lambda v: v * v)
    functor = monads.Left(None)

    result = functor > f

    assert isinstance(result, monads.Left)


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_functor_replacement_missing(value):
    functor = monads.Left(None)

    replacement = functor < value

    assert isinstance(replacement, monads.Left)
