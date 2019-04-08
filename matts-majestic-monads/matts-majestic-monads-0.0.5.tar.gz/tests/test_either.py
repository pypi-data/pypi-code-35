# pylint: disable=invalid-name
import pytest

from monads import Applicative, Either, Left, Right


def randint():
    from random import randint as r
    return r(-1000, 1000)


ITERATIONS = 100
RANDOM_VALUES = [randint() for _ in range(ITERATIONS)]
RANDOM_DOUBLES = [(randint(), randint()) for _ in range(ITERATIONS)]


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_either_convert(value):
    @Either.convert
    def to_either(value):
        return value

    actual = to_either(value)
    expected = Right(value)

    assert actual == expected


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_either_convert_exception(value):
    @Either.convert
    def to_either(value):
        raise ValueError(value)

    actual = to_either(value)
    expected = Left(ValueError(value))

    assert actual.value.args == expected.value.args
    assert actual.value.__class__ == expected.value.__class__


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_left_stringification(value):
    left = Left(ValueError(value))
    expected = 'Left({value})'.format(value=value)

    assert str(left) == expected


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_right_stringification(value):
    right = Right(value)
    expected = 'Right({value})'.format(value=value)

    assert str(right) == expected


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_left_equality(value):
    error = ValueError(value)
    left = Left(error)
    compare = Left(error)

    assert left == compare


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_left_inequality(value):
    left = Left(ValueError(value))
    compare = Left(ValueError(value))

    assert left != compare


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_right_equality(value):
    right = Right(value)
    compare = Right(value)

    assert right == compare


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_right_inequality(value):
    right = Right(value)
    compare = Right(value + 1)

    assert right != compare


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_left_right_inequality(value):
    error = ValueError(value)
    left = Left(value)
    right = Right(error)

    assert left != right


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_left_hash(value):
    left = Left(ValueError(value))

    assert left in {left}


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_right_hash(value):
    right = Right(ValueError(value))

    assert right in {right}
