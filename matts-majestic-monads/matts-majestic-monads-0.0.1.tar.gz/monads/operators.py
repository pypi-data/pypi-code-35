from abc import ABC, abstractmethod


class FunctionOperator(ABC):
    @abstractmethod
    def compose(self, fun):
        pass

    def __mul__(self, fun):
        """ * is a synonym for compose """
        return self.compose(fun)


class FunctorOperator(ABC):
    @abstractmethod
    def fmap(self, fun):
        pass

    @abstractmethod
    def replace(self, value):
        pass

    def __gt__(self, fun):
        """ > is a synonym for fmap """
        return self.fmap(fun)

    def __lt__(self, value):
        """ < is a synonym for replace """
        return self.replace(value)


class ApplicativeOperator(FunctorOperator):
    @abstractmethod
    def apply(self, applicative):
        pass

    def __le__(self, applicative):
        """ <= is a synonym for apply """
        return self.apply(applicative)


class MonadOperator(ApplicativeOperator):
    @abstractmethod
    def bind(self, fun):
        pass

    def __ge__(self, fun):
        """ >= is a synonym for bind """
        return self.bind(fun)
