# pylint: disable=invalid-name
import pytest

from monads import Function, Maybe, Nothing, identity


def randint():
    from random import randint as r
    return r(-1000, 1000)


ITERATIONS = 100
RANDOM_VALUES = [randint() for _ in range(ITERATIONS)]
RANDOM_DOUBLES = [(randint(), randint()) for _ in range(ITERATIONS)]


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_functor_identity_preservation(value):
    """ fmap id == id """
    functor = Maybe.lift(value)

    fmap_id = functor > identity  # pylint: disable=comparison-with-callable
    id_fmap = identity(functor)

    assert fmap_id == id_fmap


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_functor_composition_preservation(value):
    """ fmap (f * g) == fmap f * fmap g """
    f = Function(lambda v: v * v)
    g = Function(lambda v: v + v)
    functor = Maybe.lift(value)

    nothing = functor > f * g
    just = (functor > f) > g
    assert nothing == just


@pytest.mark.parametrize("original,value", RANDOM_DOUBLES)
def test_functor_replacement(original, value):
    """ f a < b == f b """
    functor = Maybe.lift(original)

    replacement = functor < value

    assert replacement == Maybe.lift(value)


def test_functor_fmap_missing():
    f = Function(lambda v: v * v)
    functor = Nothing

    result = functor > f

    assert result is Nothing


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_functor_replacement_missing(value):
    functor = Nothing

    replacement = functor < value

    assert replacement is Nothing
