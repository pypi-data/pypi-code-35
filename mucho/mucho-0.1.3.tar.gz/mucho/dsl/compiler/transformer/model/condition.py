from typing import Union

from .operator import Operator
from .value import Value


class Condition:
    """Logical condition of the DSL."""

    def __init__(
            self, operand_left: Union['Condition', Value], operator: Operator,
            operand_right: Union['Condition', Value],
            is_negated: bool = False):
        """
        :param operand_left: operand on the left of the condition operator
        :param operator: operator of the condition
        :param operand_right: operand on the right of the condition operator
        :param is_negated: if True, the evaluation of the condition will be
        the negation of its operator result
        """
        self.operand_left = operand_left
        self.operator = operator
        self.operand_right = operand_right
        self.is_negated = is_negated

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.__dict__)
