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
def test_monad_bind_lift_equivalence(value):
    """ m a >= lift == m a """
    m_a = monads.Either.lift(value)

    ma_bind_lift = m_a >= monads.Either.lift  # pylint: disable=comparison-with-callable

    assert ma_bind_lift == m_a


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_monad_lift_bind_equivalence(value):
    """ lift a >= f == f a """
    f = monads.Function(lambda v: monads.Either.lift(v * v))
    m_a = monads.Either.lift(value)

    lift_bind = m_a >= f
    f_a = f(value)

    assert lift_bind == f_a


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_monad_bind_composition_equivalence(value):
    """ m >= (a -> f a >>= g) == (m >= f) >= g """
    f = monads.Function(lambda v: monads.Either.lift(v * v))
    g = monads.Function(lambda v: monads.Either.lift(v + v))
    m_a = monads.Either.lift(value)

    left = m_a >= (lambda a: f(a) >= g)
    right = (m_a >= f) >= g

    assert left == right


def test_monad_bind_missing():
    f = monads.Function(lambda v: monads.Either.lift(v * v))
    m_a = monads.Left(None)

    bind = m_a >= f

    assert isinstance(bind, monads.Left)
