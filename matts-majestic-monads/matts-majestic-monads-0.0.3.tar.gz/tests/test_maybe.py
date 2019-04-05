# pylint: disable=invalid-name
import pytest

from monads import Applicative, Just, Maybe, Nothing


def randint():
    from random import randint as r
    return r(-1000, 1000)


ITERATIONS = 100
RANDOM_VALUES = [randint() for _ in range(ITERATIONS)]
RANDOM_DOUBLES = [(randint(), randint()) for _ in range(ITERATIONS)]


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_maybe_convert(value):
    @Maybe.convert
    def to_maybe(value):
        return value

    actual = to_maybe(value)
    expected = Just(value)

    assert actual == expected


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_maybe_convert_exception(value):
    @Maybe.convert
    def to_maybe(value):
        raise ValueError(value)

    actual = to_maybe(value)
    expected = Nothing

    assert actual == expected


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_maybe_apply_exception(value):
    class Fail(Applicative):
        def apply(self, applicative):
            raise ValueError(value)

        def fmap(self, fun):
            raise ValueError(value)

        @classmethod
        def lift(cls, value):
            raise ValueError(value)

    applicative = Fail()
    just = Just(value)
    actual = just.apply(applicative)

    assert actual == Nothing


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_maybe_bind_exception(value):
    def fail(value):
        raise ValueError(value)

    just = Just(value)
    actual = just.bind(fail)

    assert actual == Nothing


def test_nothing_stringification():
    nothing = Nothing
    expected = 'Nothing'

    assert str(nothing) == expected


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_just_stringification(value):
    just = Just(value)
    expected = 'Just({value})'.format(value=value)

    assert str(just) == expected


def test_nothing_equality():
    nothing = Nothing
    compare = Nothing

    assert nothing == compare


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_just_equality(value):
    just = Just(value)
    compare = Just(value)

    assert just == compare


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_just_inequality(value):
    just = Just(value)
    compare = Just(value + 1)

    assert just != compare


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_nothing_just_inequality(value):
    nothing = Nothing
    just = Just(value)

    assert nothing != just


def test_nothing_hash():
    nothing = Nothing

    assert nothing in {nothing}


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_just_hash(value):
    just = Just(value)

    assert just in {just}
