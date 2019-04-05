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
def test_either_convert(value):
    @monads.Either.convert
    def to_either(value):
        return value

    actual = to_either(value)
    expected = monads.Right(value)

    assert actual == expected


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_either_convert_exception(value):
    @monads.Either.convert
    def to_either(value):
        raise ValueError(value)

    actual = to_either(value)
    expected = monads.Left(ValueError(value))

    assert actual.value.args == expected.value.args
    assert actual.value.__class__ == expected.value.__class__


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_either_apply_exception(value):
    def fail(value):
        raise ValueError(value)

    applicative = monads.Right(fail)
    right = monads.Right(value)
    actual = right.apply(applicative)

    assert isinstance(actual, monads.Left)


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_either_bind_exception(value):
    def fail(value):
        raise ValueError(value)

    right = monads.Right(value)
    actual = right.bind(fail)

    assert isinstance(actual, monads.Left)


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_left_stringification(value):
    left = monads.Left(ValueError(value))
    expected = 'Left({value})'.format(value=value)

    assert str(left) == expected


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_right_stringification(value):
    right = monads.Right(value)
    expected = 'Right({value})'.format(value=value)

    assert str(right) == expected


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_left_equality(value):
    error = ValueError(value)
    left = monads.Left(error)
    compare = monads.Left(error)

    assert left == compare


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_left_inequality(value):
    left = monads.Left(ValueError(value))
    compare = monads.Left(ValueError(value))

    assert left != compare


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_right_equality(value):
    right = monads.Right(value)
    compare = monads.Right(value)

    assert right == compare


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_right_inequality(value):
    right = monads.Right(value)
    compare = monads.Right(value + 1)

    assert right != compare


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_left_right_inequality(value):
    error = ValueError(value)
    left = monads.Left(value)
    right = monads.Right(error)

    assert left != right


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_left_hash(value):
    left = monads.Left(ValueError(value))

    assert left in {left}


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_right_hash(value):
    right = monads.Right(ValueError(value))

    assert right in {right}
