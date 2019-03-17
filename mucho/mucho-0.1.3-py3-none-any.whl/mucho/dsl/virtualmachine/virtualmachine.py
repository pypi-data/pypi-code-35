from typing import List, Optional, Union

from mucho.comparison.result import ComparisonResult
from mucho.dsl.compiler.transformer.model import (
    Condition, Variable, Value, Rule)


class VirtualMachine:
    """Evaluates the object representation of the rules according to the
    specified context."""

    def run(self, rules: List[Rule],
            context: ComparisonResult) -> Optional[Rule]:
        """Evaluates the rules according to the specified context and return
        the first rule that is satisfied.

        :param rules: object representation of the rules
        :param context: data to use during the evaluation of the rules, i.e.
        values of the variables used in the rules
        :return: first rule satisfied or None if no rule is satisfied
        """
        for rule in rules:
            if self._eval_condition(rule.condition, context):
                return rule
        return None

    def _eval_condition(
            self, condition: Union[Condition, Value],
            context: ComparisonResult) -> Union[bool, float]:
        if isinstance(condition, Value):
            return self._eval_value(condition)
        elif isinstance(condition, Variable):
            return self._eval_variable(condition, context)
        elif isinstance(condition, Condition):
            result = condition.operator.func(
                self._eval_condition(condition.operand_left, context),
                self._eval_condition(condition.operand_right, context),
            )
            return not result if condition.is_negated else result
        else:
            raise ExecutionError(
                "Wrong type evaluating condition: '{0}'".format(
                    type(condition)))

    def _eval_value(self, value: Value) -> Union[bool, float]:
        return value.value

    def _eval_variable(
            self, variable: Variable, context: ComparisonResult) -> float:
        try:
            field_value = getattr(context, variable.field)
        except AttributeError:
            raise ExecutionError(
                "Field '{0}' not in context".format(variable.field))
        try:
            property_value = getattr(field_value, variable.property)
            return property_value
        except AttributeError:
            raise ExecutionError(
                "Property '{0}.{1}' not in context".format(
                    variable.field, variable.property))


class ExecutionError(Exception):
    pass
