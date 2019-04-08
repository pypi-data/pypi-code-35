from abc import ABC, abstractclassmethod, abstractmethod


class Function(ABC):
    """ A Unary Function suitable for use with Functor, Applicative and Monad """

    @abstractmethod
    def __call__(self, arg):
        """ Invoke the Function """

    def compose(self, fun):
        """ compose :: (a -> b) -> (b -> c) -> (a -> c)
            Creates a new function through the composition of the two provided functions. """
        return self.__class__(lambda arg: fun(self(arg)))


class Functor(ABC):
    """ The Functor typeclass represents the mathematical functor: a mapping between categories in the context of category theory.
        In practice a functor represents a type that can be mapped over. """

    @abstractclassmethod
    def lift(cls, value):
        """ lift :: f -> a -> f a
            Creates a new f a, from an a.
            In Haskell this is `return`, which is a keyword in python. """

    @abstractmethod
    def fmap(self, fun):
        """ fmap :: f a -> (a -> b) -> f b
            Create a new f b, from an f a using the results of calling a function on every value in the f a. """

    def replace(self, value):
        """ replace :: f a -> b -> f b
            Create a new f b, from an f a by replacing all of the values in the f a by a given value of type b. """
        return self.fmap(lambda _: value)


class Applicative(Functor):  # pylint: disable=abstract-method
    @abstractmethod
    def apply(self, applicative):
        """ apply :: m a -> m (a -> b) -> m b
            Create a new m b, from an m a using the results of calling a lifted function on every value in the m a. """


class Monad(Applicative):
    @abstractmethod
    def bind(self, fun):
        """ bind :: m a -> (a -> m b) -> m b
            Create a new m b, from an m a using the results of calling a function on every value in the m a. """

    def fmap(self, fun):
        """ fmap :: f a -> (a -> b) -> f b
            Create a new f b, from an f a using the results of calling a function on every value in the f a. """
        return self.bind(lambda v: self.lift(fun(v)))
