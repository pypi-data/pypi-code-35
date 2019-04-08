from .base import Monad
from .operators import MonadOperator


class List(Monad, MonadOperator):
    @classmethod
    def lift(cls, value):
        return List([value])

    @classmethod
    def convert(cls, function):
        def wrapper(*args, **kwargs):
            return List(function(*args, **kwargs))

        return wrapper

    def __init__(self, values):
        self.values = list(iter(values))

    def fmap(self, fun):
        return List(fun(value) for value in self.values)

    def apply(self, applicative):
        return self.bind(lambda v: applicative.fmap(lambda f: f(v)))

    def bind(self, fun):
        return sum((fun(value) for value in self.values), List([]))

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __delitem__(self, key):
        del self.values[key]

    def __iter__(self):
        return iter(self.values)

    def __contains__(self, item):
        return item in self.values

    def __add__(self, other):
        if isinstance(other, List):
            return List(self.values + other.values)
        if isinstance(other, list):
            return List(self.values + other)
        raise NotImplementedError()

    def __radd__(self, other):
        if isinstance(other, List):
            return List(other.values + self.values)
        if isinstance(other, list):
            return List(other + self.values)
        raise NotImplementedError()

    def __mul__(self, other):
        return List(self.values * other)

    def __rmul__(self, other):
        return List(self.values * other)

    def append(self, value):
        self.values.append(value)

    def count(self, value):
        return self.values.count(value)

    def index(self, value):
        return self.values.index(value)

    def extend(self, iterable):
        self.values.extend(iterable)

    def insert(self, index, value):
        self.values.insert(index, value)

    def pop(self):
        return self.values.pop()

    def remove(self, value):
        self.values.remove(value)

    def reverse(self):
        self.values.reverse()

    def sort(self, key=None, reverse=False):
        self.values.sort(key=key, reverse=reverse)

    def __repr__(self):
        return 'List({values})'.format(values=self.values)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.values == other.values
