import unittest
from unittest.mock import Mock

from mucho.dsl.compiler.transformer.model import OP_EQ, OP_GT, OP_OR
from mucho.dsl.compiler.transformer.model import (
    Value, Variable, Condition, Rule)
from mucho.dsl.virtualmachine import VirtualMachine, ExecutionError
from mucho.comparison import ComparisonResult


class VirtualMachineTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.virtual_machine = VirtualMachine()

    def test_eval_value_returns_raw_value(self):
        value_raw = 5.15
        value_obj = Value(value_raw)
        self.assertEqual(
            value_raw,
            self.virtual_machine._eval_value(value_obj))

    def test_eval_variable_returns_result_dot_field_dot_property(self):
        field, property, value = 'years', 'difference', 15
        context = ComparisonResult(**{
            field: ComparisonResult(**{
                property: value})
        })
        variable = Variable(field, property)
        self.assertEqual(
            value,
            self.virtual_machine._eval_variable(variable, context))

    def test_eval_condition_returns_raw_value_if_condition_is_value(self):
        value_raw = 5
        condition = Value(value_raw)
        self.assertEqual(
            value_raw,
            self.virtual_machine._eval_condition(condition, Mock()))

    def test_eval_condition_returns_variable_value_if_condition_is_variable(
            self):
        condition = Variable('years', 'difference')
        variable_value = 22
        context = Mock(years=Mock(difference=variable_value))
        self.assertEqual(
            variable_value,
            self.virtual_machine._eval_condition(condition, context))

    def test_eval_condition_returns_op_result_if_condition_is_variable_op_value(
            self):
        variable = Variable('years', 'difference')
        variable_value = 4
        value_raw = 5
        value = Value(value_raw)
        condition = Condition(variable, OP_EQ, value)
        context = ComparisonResult(
            years=ComparisonResult(difference=variable_value))
        self.assertEqual(
            variable_value == value_raw,
            self.virtual_machine._eval_condition(condition, context))

    def test_eval_condition_returns_op_result_if_condition_is_cond_op_cond(
            self):
        var_1, var_1_value = Variable('years', 'are_same'), False
        var_2, var_2_value = Variable('titles', 'sim'), 87.55
        value_raw = 85
        value = Value(value_raw)
        condition_1 = Condition(var_1, OP_EQ, Value(True))
        condition_2 = Condition(var_2, OP_GT, value)
        condition = Condition(condition_1, OP_OR, condition_2)
        context = ComparisonResult(
            years=ComparisonResult(are_same=var_1_value),
            titles=ComparisonResult(sim=var_2_value),
        )
        self.assertEqual(
            var_1_value or var_2_value > value_raw,
            self.virtual_machine._eval_condition(condition, context))

    def test_eval_condition_returns_not_op_result_if_condition_is_cond_op_cond_and_negated(
            self):
        var_1, var_1_value = Variable('years', 'are_same'), False
        var_2, var_2_value = Variable('titles', 'sim'), 87.55
        value_raw = 85
        value = Value(value_raw)
        condition_1 = Condition(var_1, OP_EQ, Value(True))
        condition_2 = Condition(var_2, OP_GT, value)
        condition = Condition(condition_1, OP_OR, condition_2, is_negated=True)
        context = ComparisonResult(
            years=ComparisonResult(are_same=var_1_value),
            titles=ComparisonResult(sim=var_2_value),
        )
        self.assertEqual(
            not (var_1_value or var_2_value > value_raw),
            self.virtual_machine._eval_condition(condition, context))

    def test_eval_condition_raises_execution_error_if_condition_has_wrong_type(
            self):
        condition = "5 > 6"
        with self.assertRaises(ExecutionError) as context:
            self.virtual_machine._eval_condition(condition, Mock())
        self.assertIn(
            "Wrong type evaluating condition",
            context.exception.args[0])

    def test_eval_variable_raises_execution_error_if_field_not_in_context(
            self):
        field, property = 'years', 'difference'
        variable = Variable(field, property)
        context = ComparisonResult(titles=ComparisonResult(similarity=90))
        with self.assertRaises(ExecutionError) as assert_context:
            self.virtual_machine._eval_variable(variable, context)
        self.assertIn(
            "Field '{0}' not in context".format(field),
            assert_context.exception.args[0])

    def test_eval_variable_raises_execution_error_if_property_not_in_context(
            self):
        field, property = 'years', 'difference'
        variable = Variable(field, property)
        context = ComparisonResult(years=ComparisonResult(are_same=True))
        with self.assertRaises(ExecutionError) as assert_context:
            self.virtual_machine._eval_variable(variable, context)
        self.assertIn(
            "Property '{0}.{1}' not in context".format(field, property),
            assert_context.exception.args[0])

    def test_run_returns_first_rule_with_true_condition_if_any_true(self):
        condition_1 = Condition(Variable('years', 'same'), OP_EQ, Value(True))
        condition_2 = Condition(Variable('years', 'diff'), OP_EQ, Value(2))
        condition_3 = Condition(Variable('years', 'diff'), OP_EQ, Value(3))
        rule_1 = Rule("R1", None, condition_1, Rule.Result.MATCH)
        rule_2 = Rule("R2", None, condition_2, Rule.Result.MISMATCH)
        rule_3 = Rule("R3", None, condition_3, Rule.Result.UNKNOWN)
        result = self.virtual_machine.run(
            [rule_1, rule_2, rule_3],
            ComparisonResult(
                years=ComparisonResult(
                    same=False,
                    diff=2,
                )
            ))
        self.assertEqual(rule_2, result)

    def test_run_returns_none_if_no_true_conditions(self):
        condition_1 = Condition(Variable('years', 'same'), OP_EQ, Value(True))
        condition_2 = Condition(Variable('years', 'diff'), OP_EQ, Value(2))
        condition_3 = Condition(Variable('years', 'diff'), OP_EQ, Value(3))
        rule_1 = Rule("R1", None, condition_1, Rule.Result.MATCH)
        rule_2 = Rule("R2", None, condition_2, Rule.Result.MISMATCH)
        rule_3 = Rule("R3", None, condition_3, Rule.Result.UNKNOWN)
        result = self.virtual_machine.run(
            [rule_1, rule_2, rule_3],
            ComparisonResult(
                years=ComparisonResult(
                    same=False,
                    diff=4,
                )
            ))
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
