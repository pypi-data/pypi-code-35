# pylint: disable=invalid-name
import pytest

from monads import List


def randint():
    from random import randint as r
    return r(-1000, 1000)


ITERATIONS = 100
RANDOM_VALUES = [randint() for _ in range(ITERATIONS)]
RANDOM_DOUBLES = [(randint(), randint()) for _ in range(ITERATIONS)]


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_list_convert(value):
    @List.convert
    def to_list(value):
        return [value]

    actual = to_list(value)
    expected = List([value])

    assert actual == expected


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_list_convert_exception(value):
    @List.convert
    def to_list(value):
        raise ValueError(value)

    with pytest.raises(ValueError):
        to_list(value)


def test_empty_stringification():
    empty = List([])
    expected = 'List([])'

    assert str(empty) == expected


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_something_stringification(value):
    something = List([value])
    expected = 'List([{value}])'.format(value=value)

    assert str(something) == expected


def test_empty_equality():
    empty = List([])
    compare = List([])

    assert empty == compare


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_something_equality(value):
    something = List([value])
    compare = List([value])

    assert something == compare


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_something_inequality(value):
    something = List([value])
    compare = List([value + 1])

    assert something != compare


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_nothing_just_inequality(value):
    empty = List([])
    something = List([value])

    assert empty != something
