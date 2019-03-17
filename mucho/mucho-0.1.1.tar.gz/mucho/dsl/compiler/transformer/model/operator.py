from typing import Callable

from operator import lt, le, eq, ge, gt


class Operator:
    """Operator of the DSL, can be logical (and, or)
    or numeric (==, >=, <=).
    """

    def __init__(self, name: str, func: Callable):
        """
        :param name: name of the operator
        :param func: function with the logic performed by the operator
        """
        self.name = name
        self.func = func

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.__dict__)

OP_AND = Operator(name='and', func=lambda a, b: a and b)
OP_OR = Operator(name='or', func=lambda a, b: a or b)
OP_EQ = Operator(name='eq', func=eq)
OP_LT = Operator(name='lt', func=lt)
OP_GT = Operator(name='gt', func=gt)
OP_LE = Operator(name='le', func=le)
OP_GE = Operator(name='ge', func=ge)
