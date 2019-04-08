# pylint: disable=invalid-name
import pytest

from monads import Function, List


def randint():
    from random import randint as r
    return r(-1000, 1000)


ITERATIONS = 100
RANDOM_VALUES = [randint() for _ in range(ITERATIONS)]
RANDOM_DOUBLES = [(randint(), randint()) for _ in range(ITERATIONS)]


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_monad_bind_lift_equivalence(value):
    """ m a >= lift == m a """
    m_a = List.lift(value)

    ma_bind_lift = m_a >= List.lift  # pylint: disable=comparison-with-callable

    assert ma_bind_lift == m_a


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_monad_lift_bind_equivalence(value):
    """ lift a >= f == f a """
    f = Function(lambda v: List.lift(v * v))
    m_a = List.lift(value)

    lift_bind = m_a >= f
    f_a = f(value)

    assert lift_bind == f_a


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_monad_bind_composition_equivalence(value):
    """ m >= (a -> f a >>= g) == (m >= f) >= g """
    f = Function(lambda v: List.lift(v * v))
    g = Function(lambda v: List.lift(v + v))
    m_a = List.lift(value)

    left = m_a >= (lambda a: f(a) >= g)
    right = (m_a >= f) >= g

    assert left == right


def test_monad_bind_missing():
    f = Function(lambda v: List.lift(v * v))
    m_a = List([])

    bind = m_a >= f

    assert bind == List([])


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_list_bind_exception(value):
    def fail(value):
        raise ValueError(value)

    something = List([value])
    with pytest.raises(ValueError):
        something.bind(fail)
