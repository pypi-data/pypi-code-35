from .base import Function as BaseFunction
from .operators import FunctionOperator


def identity(v):  # pylint: disable=invalid-name
    return v


class Function(BaseFunction, FunctionOperator):
    def __init__(self, fun=identity):
        self.fun = fun

    def __call__(self, arg):
        return self.fun(arg)

    def __repr__(self):
        return f'Function({self.fun})'
