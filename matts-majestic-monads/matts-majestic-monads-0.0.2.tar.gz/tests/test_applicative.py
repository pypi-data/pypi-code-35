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
def test_applicative_equivalence(value):
    """ m a <= m f == m (f a) """
    m_a = monads.Either.lift(value)
    f = monads.Function(lambda v: v * v)
    m_f = monads.Either.lift(f)

    m_fa = monads.Either.lift(f(value))
    ma_mf = m_a <= m_f

    assert ma_mf == m_fa


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_applicative_function_missing(value):
    m_a = monads.Either.lift(value)
    m_f = monads.Left(None)

    ma_mf = m_a <= m_f

    assert isinstance(ma_mf, monads.Left)


def test_applicative_value_missing():
    m_a = monads.Left(None)
    f = monads.Function(lambda v: v * v)
    m_f = monads.Either.lift(f)

    ma_mf = m_a <= m_f

    assert isinstance(ma_mf, monads.Left)
