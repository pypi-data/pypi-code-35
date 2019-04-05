from .base import Monad
from .operators import MonadOperator


class Either(Monad, MonadOperator):  # pylint: disable=abstract-method
    @classmethod
    def lift(cls, value):
        return Right(value)

    @classmethod
    def convert(cls, function):
        def wrapper(*args, **kwargs):
            try:
                return Right(function(*args, **kwargs))
            except Exception as exception:  # pylint: disable=broad-except
                return Left(exception)

        return wrapper


class Left(Either):
    """ This represents an error """

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
        return f'Left({self.value})'

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value

    def __hash__(self):
        return hash(self.value)


class Right(Either):
    """ This represents success (it's punning on the meanings of right) """

    def __init__(self, value):
        self.value = value

    def apply(self, applicative):
        """ apply :: m a -> m (a -> b) -> m b
            Create a new m b, from an m a using the results of calling a lifted function on every value in the m a. """
        try:
            return applicative.bind(self.fmap)
        except Exception as exception:  # pylint: disable=broad-except
            return Left(exception)

    def bind(self, fun):
        """ bind :: m a -> (a -> m b) -> m b
            Create a new m b, from an m a using the results of calling a function on every value in the m a. """
        try:
            return fun(self.value)
        except Exception as exception:  # pylint: disable=broad-except
            return Left(exception)

    def __repr__(self):
        return f'Right({self.value})'

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value

    def __hash__(self):
        return hash(self.value)
