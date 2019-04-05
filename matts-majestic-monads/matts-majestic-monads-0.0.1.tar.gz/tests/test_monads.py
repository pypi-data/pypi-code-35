import pytest

import monads


def randint():
    from random import randint as r
    return r(-1000, 1000)


ITERATIONS = 100
RANDOM_VALUES = [randint() for _ in range(ITERATIONS)]
RANDOM_DOUBLES = [(randint(), randint()) for _ in range(ITERATIONS)]


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_function_identity_composition(value):
    """ f == f * id """
    function = monads.Function(lambda v: v * v)
    composed = function.compose(monads.identity)

    assert function(value) == composed(value)


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_function_composition_equivalence(value):
    """ (f * g) * h == f * (g * h) """
    f = monads.Function(lambda v: v * v)  # pylint: disable=invalid-name
    g = monads.Function(lambda v: v + v)  # pylint: disable=invalid-name
    h = monads.Function(lambda v: v - 1)  # pylint: disable=invalid-name

    fg_h = (f * g) * h
    f_gh = f * (g * h)

    assert fg_h(value) == f_gh(value)


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_functor_identity_preservation(value):
    """ fmap id == id """
    functor = monads.Either.lift(value)

    fmap_id = functor > monads.identity  # pylint: disable=comparison-with-callable
    identity = monads.identity(functor)

    assert fmap_id == identity


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_functor_composition_preservation(value):
    """ fmap (f * g) == fmap f * fmap g """
    f = monads.Function(lambda v: v * v)  # pylint: disable=invalid-name
    g = monads.Function(lambda v: v + v)  # pylint: disable=invalid-name
    functor = monads.Either.lift(value)

    left = functor > f * g
    right = (functor > f) > g
    assert left == right


@pytest.mark.parametrize("original,value", RANDOM_DOUBLES)
def test_functor_replacement(original, value):
    """ f a < b == f b """
    functor = monads.Either.lift(original)

    replacement = functor < value

    assert replacement == monads.Either.lift(value)


def test_functor_fmap_missing():
    f = monads.Function(lambda v: v * v)  # pylint: disable=invalid-name
    functor = monads.Left(None)

    result = functor > f

    assert isinstance(result, monads.Left)


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_functor_replacement_missing(value):
    functor = monads.Left(None)

    replacement = functor < value

    assert isinstance(replacement, monads.Left)


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_applicative_equivalence(value):
    """ m a <= m f == m (f a) """
    m_a = monads.Either.lift(value)
    f = monads.Function(lambda v: v * v)  # pylint: disable=invalid-name
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
    f = monads.Function(lambda v: v * v)  # pylint: disable=invalid-name
    m_f = monads.Either.lift(f)

    ma_mf = m_a <= m_f

    assert isinstance(ma_mf, monads.Left)


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_monad_bind_lift_equivalence(value):
    """ m a >= lift == m a """
    m_a = monads.Either.lift(value)

    ma_bind_lift = m_a >= monads.Either.lift  # pylint: disable=comparison-with-callable

    assert ma_bind_lift == m_a


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_monad_lift_bind_equivalence(value):
    """ lift a >= f == f a """
    f = monads.Function(lambda v: monads.Either.lift(v * v))  # pylint: disable=invalid-name
    m_a = monads.Either.lift(value)

    lift_bind = m_a >= f
    f_a = f(value)

    assert lift_bind == f_a


@pytest.mark.parametrize("value", RANDOM_VALUES)
def test_monad_bind_composition_equivalence(value):
    """ m >= (a -> f a >>= g) == (m >= f) >= g """
    f = monads.Function(lambda v: monads.Either.lift(v * v))  # pylint: disable=invalid-name
    g = monads.Function(lambda v: monads.Either.lift(v + v))  # pylint: disable=invalid-name
    m_a = monads.Either.lift(value)

    left = m_a >= (lambda a: f(a) >= g)
    right = (m_a >= f) >= g

    assert left == right


def test_monad_bind_missing():
    f = monads.Function(lambda v: monads.Either.lift(v * v))  # pylint: disable=invalid-name
    m_a = monads.Left(None)

    bind = m_a >= f

    assert isinstance(bind, monads.Left)
