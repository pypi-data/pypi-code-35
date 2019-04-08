from abc import ABC, abstractmethod


class FunctionOperator(ABC):
    @abstractmethod
    def compose(self, fun):
        """ compose :: (a -> b) -> (b -> c) -> (a -> c)
            Creates a new function through the composition of the two provided functions. """

    def __mul__(self, fun):
        """ * is a synonym for compose """
        return self.compose(fun)


class FunctorOperator(ABC):
    @abstractmethod
    def fmap(self, fun):
        """ fmap :: f a -> (a -> b) -> f b
            Create a new f b, from an f a using the results of calling a function on every value in the f a. """

    @abstractmethod
    def replace(self, value):
        """ replace :: f a -> b -> f b
            Create a new f b, from an f a by replacing all of the values in the f a by a given value of type b. """

    def __gt__(self, fun):
        """ > is a synonym for fmap """
        return self.fmap(fun)

    def __lt__(self, value):
        """ < is a synonym for replace """
        return self.replace(value)


class ApplicativeOperator(FunctorOperator):
    @abstractmethod
    def apply(self, applicative):
        """ apply :: m a -> m (a -> b) -> m b
            Create a new m b, from an m a using the results of calling a lifted function on every value in the m a. """

    def __le__(self, applicative):
        """ <= is a synonym for apply """
        return self.apply(applicative)


class MonadOperator(ApplicativeOperator):
    @abstractmethod
    def bind(self, fun):
        """ bind :: m a -> (a -> m b) -> m b
            Create a new m b, from an m a using the results of calling a function on every value in the m a. """

    def __ge__(self, fun):
        """ >= is a synonym for bind """
        return self.bind(fun)
