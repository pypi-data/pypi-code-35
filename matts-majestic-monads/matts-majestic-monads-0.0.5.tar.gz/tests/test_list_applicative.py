# pylint: disable=invalid-name
import pytest

from monads import Applicative, Function, List


def randint():
    from random import randint as r
    return r(-1000, 1000)


ITERATIONS = 100
RANDOM_VALUES = [randint() for _ in range(ITERATIONS)]
RANDOM_DOUBLES = [(randint(), randint()) for _ in range(ITERATIONS)]


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_applicative_equivalence(value):
    """ m a <= m f == m (f a) """
    m_a = List.lift(value)
    f = Function(lambda v: v * v)
    m_f = List.lift(f)

    m_fa = List.lift(f(value))
    ma_mf = m_a <= m_f

    assert ma_mf == m_fa


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_applicative_function_missing(value):
    m_a = List.lift(value)
    m_f = List([])

    ma_mf = m_a <= m_f

    assert ma_mf == List([])


def test_applicative_value_missing():
    m_a = List([])
    f = Function(lambda v: v * v)
    m_f = List.lift(f)

    ma_mf = m_a <= m_f

    assert ma_mf == List([])


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_list_apply_exception(value):
    class Fail(Applicative):
        def apply(self, applicative):
            raise ValueError(value)

        def fmap(self, fun):
            raise ValueError(value)

        @classmethod
        def lift(cls, value):
            raise ValueError(value)

    applicative = Fail()
    something = List([value])
    with pytest.raises(ValueError):
        something.apply(applicative)


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_list_apply_exception_patch(value):
    class Fail(List):
        def bind(self, fun):
            raise ValueError(value)

    applicative = None
    right = Fail([value])
    with pytest.raises(ValueError):
        right.apply(applicative)
