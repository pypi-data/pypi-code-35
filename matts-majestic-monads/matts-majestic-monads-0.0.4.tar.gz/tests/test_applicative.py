# pylint: disable=invalid-name
import pytest

from monads import Either, Function, Left


def randint():
    from random import randint as r
    return r(-1000, 1000)


ITERATIONS = 100
RANDOM_VALUES = [randint() for _ in range(ITERATIONS)]
RANDOM_DOUBLES = [(randint(), randint()) for _ in range(ITERATIONS)]


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_applicative_equivalence(value):
    """ m a <= m f == m (f a) """
    m_a = Either.lift(value)
    f = Function(lambda v: v * v)
    m_f = Either.lift(f)

    m_fa = Either.lift(f(value))
    ma_mf = m_a <= m_f

    assert ma_mf == m_fa


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_applicative_function_missing(value):
    m_a = Either.lift(value)
    m_f = Left(None)

    ma_mf = m_a <= m_f

    assert isinstance(ma_mf, Left)


def test_applicative_value_missing():
    m_a = Left(None)
    f = Function(lambda v: v * v)
    m_f = Either.lift(f)

    ma_mf = m_a <= m_f

    assert isinstance(ma_mf, Left)
