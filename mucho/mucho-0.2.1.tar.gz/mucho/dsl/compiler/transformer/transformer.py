from typing import Optional, List, Set

from lark import Transformer
from lark.exceptions import VisitError

from mucho.dsl.compiler.transformer.model import (
    OP_AND, OP_OR, OP_EQ, OP_GE, OP_GT, OP_LE, OP_LT)
from mucho.dsl.compiler.transformer.model import (
    Value, Variable, Condition, Rule)


class RulesTransformer(Transformer):
    """Transforms the abstract syntax tree obtained from the analysis of the
    string with the defined rules into its equivalent Python object
    representation.
    """

    def __init__(self, allowed_variables: Optional[Set[str]] = None):
        """
        :param allowed_variables: the list of variable names to be used
        during the evaluation of the rules. If specified, the transformer will
        make sure that the names of the variables used in the definition of the
        rules match the names of the ones in the list of allowed variables.
        """
        super().__init__()
        self._allowed_variables = allowed_variables
        self._rule_ids = dict()  # type: dict

    def transform(self, tree) -> List[Rule]:
        """Transforms the abstract syntax tree obtained from the analysis of the
        string with the defined rules into its equivalent Python object
        representation.

        :param tree: abstract syntax tree with the analysis of the defined
        rules
        :return: list of objects representing the defined rules
        """
        self._reset_rule_ids()
        return super().transform(tree)

    def _reset_rule_ids(self):
        self._rule_ids.clear()

    def value(self, items):
        return Value(float(items[0]))

    def variable(self, items):
        dimension, property = items
        if self._allowed_variables is not None:
            variable_name = "{dimension}.{property}".format(
                dimension=dimension, property=property)
            if variable_name not in self._allowed_variables:
                raise VisitError(
                    "Unknown variable '{0}' in line {1}, column {2}".format(
                        variable_name, dimension.line, dimension.column))
        return Variable(field=str(dimension), property=str(property))

    def opeq(self, _):
        return OP_EQ

    def oplt(self, _):
        return OP_LT

    def opgt(self, _):
        return OP_GT

    def ople(self, _):
        return OP_LE

    def opge(self, _):
        return OP_GE

    def cond(self, items):
        if len(items) == 1:
            if not isinstance(items[0], Variable):
                return items[0]
            else:
                return Condition(
                    operand_left=items[0],
                    operator=OP_EQ,
                    operand_right=Value(True),
                )
        elif len(items) == 2:
            condition = items[1]
            condition.is_negated = not condition.is_negated
            return condition
        elif len(items) == 3:
            return Condition(
                operand_left=items[0],
                operator=items[1],
                operand_right=items[2],
            )

    def condand(self, items):
        if len(items) == 1:
            return items[0]
        elif len(items) == 2:
            return Condition(
                operand_left=items[0],
                operator=OP_AND,
                operand_right=items[1],
            )

    def condor(self, items):
        if len(items) == 1:
            return items[0]
        elif len(items) == 2:
            return Condition(
                operand_left=items[0],
                operator=OP_OR,
                operand_right=items[1],
            )

    def rule(self, items):
        rule_id = items[0]
        if rule_id.value in self._rule_ids:
            raise VisitError(
                "Rule id '{0}' already exists: "
                "(line {1}, column {2}) and (line {3}, column {4})".format(
                    rule_id,
                    self._rule_ids[rule_id].line,
                    self._rule_ids[rule_id].column,
                    rule_id.line,
                    rule_id.column,
                ))
        else:
            self._rule_ids[rule_id.value] = items[0]
        return Rule(
            id=items[0].value,
            description=items[1][1:].strip() or None,
            condition=items[2],
            result=Rule.Result(items[3].upper()),
        )

    def rules(self, items):
        return items
