from .base import Monad
from .operators import MonadOperator


class Maybe(Monad, MonadOperator):  # pylint: disable=abstract-method
    @classmethod
    def lift(cls, value):
        return Just(value)

    @classmethod
    def convert(cls, function):
        def wrapper(*args, **kwargs):
            try:
                return Just(function(*args, **kwargs))
            except Exception:  # pylint: disable=broad-except
                return Nothing

        return wrapper


class Nothing(Maybe):
    """ This represents no value """

    def __init__(self, exception):
        self.value = exception

    def apply(self, applicative):
        """ apply :: m a -> m (a -> b) -> m b
            Create a new m b, from an m a using the results of calling a lifted function on every value in the m a. """
        return self

    def bind(self, fun):
        """ bind :: m a -> (a -> m b) -> m b
            Create a new m b, from an m a using the results of calling a function on every value in the m a. """
        return self

    def __repr__(self):
        return 'Nothing'

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value

    def __hash__(self):
        return hash(self.value)


class Just(Maybe):
    """ This represents a value """

    def __init__(self, value):
        self.value = value

    def apply(self, applicative):
        """ apply :: m a -> m (a -> b) -> m b
            Create a new m b, from an m a using the results of calling a lifted function on every value in the m a. """
        return applicative.bind(self.fmap)

    def bind(self, fun):
        """ bind :: m a -> (a -> m b) -> m b
            Create a new m b, from an m a using the results of calling a function on every value in the m a. """
        return fun(self.value)

    def __repr__(self):
        return f'Just({self.value})'

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value

    def __hash__(self):
        return hash(self.value)
