import os
import unittest
from unittest import mock
from unittest.mock import Mock

from lark import Lark
from lark.exceptions import VisitError

from mucho.dsl.compiler.transformer import RulesTransformer
from mucho.dsl.compiler.transformer.model import OP_AND, OP_OR, OP_EQ
from mucho.dsl.compiler.transformer.model import (
    Value, Variable, Condition, Rule)
from mucho.comparison.comparator import (
    DimensionProperty, DimensionComparator, EntityComparator)


class TitlesComparator(DimensionComparator):
    similarity = DimensionProperty(
        description="Similarity between titles, between 0 and 100")
    are_exact = DimensionProperty(description="Titles are exact")


class YearsComparator(DimensionComparator):
    difference = DimensionProperty(
        description="Difference in years",
        resolver='get_difference')
    are_same = DimensionProperty(
        description="Tells whether the years are same or not")


class AVWorkComparator(EntityComparator):
    titles = TitlesComparator(description="Titles")
    years = YearsComparator(description="Release years")


class RulesTransformerTestCase(unittest.TestCase):
    GRAMMAR_FILE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', '..', '..', '..',
        'mucho', 'dsl', 'compiler', 'grammar', 'rules.lrk',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser_condor = self._get_parser(start='condor')
        self.parser_rules = self._get_parser(start='rules')
        self.comparator = AVWorkComparator()
        self.transformer = RulesTransformer(self.comparator)

    def _get_parser(self, start):
        return Lark(open(self.GRAMMAR_FILE), start=start)

    def _transform_input_string(self, input_string, start='condor'):
        parser = self.parser_condor if start == 'condor' else self.parser_rules
        tree = parser.parse(input_string)
        return self.transformer.transform(tree)

    def _mock_rule(self, rule, func=lambda e: e):
        return mock.patch.object(self.transformer, rule, func)

    def _mock_comparators(self, fields, properties=()):
        comparators = dict()
        for field in fields:
            comparators[field] = Mock(properties=properties)
        return mock.patch.object(self.comparator, '_comparators', comparators)

    def _mock_comparator(self, comparator):
        return mock.patch.object(self.transformer, '_comparator', comparator)

    def test_rule_value_returns_equivalent_value_object(self):
        value = Value(89.75)
        input_string = """
        titles.similarity = {value}
        """.format(value=value.value)
        with mock.patch.object(self.transformer, 'cond', lambda e: e):
            result = self._transform_input_string(input_string)
            self.assertEqual(
                value, result[2],
                "The Value object should be equivalent to the value"
            )

    def test_rule_variable_raises_transformation_error_if_field_is_unknown(
            self):
        input_string = """
        titles.unknown
        """
        with self._mock_rule('cond'), self._mock_comparators([]):
            with self.assertRaises(VisitError) as context:
                self._transform_input_string(input_string)
            self.assertIn(
                "Unknown dimension 'titles'", context.exception.args[0],
                "The message of the exception should include the field name"
            )

    def test_rule_variable_raises_keyerror_if_property_is_unknown(self):
        input_string = """
        titles.unknown
        """
        with self._mock_rule('cond'), self._mock_comparators(['titles'], []):
            with self.assertRaises(VisitError) as context:
                self._transform_input_string(input_string)
            self.assertIn(
                "Unknown property 'unknown'", context.exception.args[0],
                "The message of the exception should include the property name"
            )

    def test_rule_variable_returns_equivalent_variable_object(self):
        variable = Variable("titles", "similarity")
        input_string = """
        {field}.{property}
        """.format(field=variable.field, property=variable.property)
        with self._mock_rule('cond'), self._mock_comparators(
                [variable.field], [variable.property]):
            result = self._transform_input_string(input_string)
            self.assertEqual(
                variable,
                result[0],
                "The Variable object should be equivalent to the variable"
            )

    def test_rule_variable_does_not_raise_transformation_error_if_field_is_unknown_but_no_comparator_is_set(
            self):
        input_string = """
        titles.unknown
        """
        with self._mock_comparator(None):
            try:
                self._transform_input_string(input_string)
            except VisitError:
                self.fail(
                    "VisitError should not be raised for a transformation "
                    "without comparator")

    def test_rule_cond_returns_condition_variable_eq_value_true_if_variable(
            self):
        variable = Variable("titles", "similarity")
        input_string = """
        {field}.{property}
        """.format(field=variable.field, property=variable.property)
        with self._mock_rule('variable', lambda e: variable):
            result = self._transform_input_string(input_string)
            self.assertEqual(
                Condition(variable, OP_EQ, Value(True)),
                result,
                "The Condition object should be equivalent to the condition"
            )

    def test_rule_cond_returns_condition_variable_op_value_if_comparison(self):
        variable = Variable("titles", "similarity")
        value = Value(87.93)
        input_string = """
        {field}.{property} = {value}
        """.format(
            field=variable.field,
            property=variable.property,
            value=value.value)
        with self._mock_rule('variable', lambda e: variable):
            result = self._transform_input_string(input_string)
            self.assertEqual(
                Condition(variable, OP_EQ, value), result,
                "The Condition object should be equivalent to the condition"
            )

    def test_rule_cond_returns_condition_if_nested(self):
        variable = Variable("titles", "similarity")
        input_string = """
        ({field}.{property})
        """.format(
            field=variable.field,
            property=variable.property)
        with self._mock_rule('variable', lambda e: variable):
            result = self._transform_input_string(input_string)
            self.assertEqual(
                Condition(variable, OP_EQ, Value(True)), result,
                "The Condition object should be equivalent to the condition"
            )

    def test_rule_cond_returns_negated_condition_if_not_variable(self):
        variable = Variable("titles", "similarity")
        input_string = """
        not {field}.{property}
        """.format(
            field=variable.field,
            property=variable.property)
        with self._mock_rule('variable', lambda e: variable):
            result = self._transform_input_string(input_string)
            self.assertEqual(
                Condition(variable, OP_EQ, Value(True), is_negated=True),
                result,
                "The Condition object should be equivalent to "
                "the negated condition"
            )

    def test_rule_cond_returns_condition_if_notx2_variable(self):
        variable = Variable("titles", "similarity")
        input_string = """
        not not {field}.{property}
        """.format(
            field=variable.field,
            property=variable.property)
        with self._mock_rule('variable', lambda e: variable):
            result = self._transform_input_string(input_string)
            self.assertEqual(
                Condition(variable, OP_EQ, Value(True), is_negated=False),
                result,
                "The Condition object should be equivalent to "
                "the negated condition"
            )

    def test_rule_cond_returns_negated_condition_if_notx3_variable(self):
        variable = Variable("titles", "similarity")
        input_string = """
        not not not {field}.{property}
        """.format(
            field=variable.field,
            property=variable.property)
        with self._mock_rule('variable', lambda e: variable):
            result = self._transform_input_string(input_string)
            self.assertEqual(
                Condition(variable, OP_EQ, Value(True), is_negated=True),
                result,
                "The Condition object should be equivalent to "
                "the negated condition"
            )

    def test_rule_cond_returns_negated_condition_if_not_var_op_val(self):
        variable = Variable("titles", "similarity")
        value = Value(87.93)
        input_string = """
        not {field}.{property} = {value}
        """.format(
            field=variable.field,
            property=variable.property,
            value=value.value)
        with self._mock_rule('variable', lambda e: variable):
            result = self._transform_input_string(input_string)
            self.assertEqual(
                Condition(variable, OP_EQ, value, is_negated=True), result,
                "The Condition object should be equivalent to "
                "the negated condition"
            )

    def test_rule_cond_returns_condition_if_notx2_var_op_val(self):
        variable = Variable("titles", "similarity")
        value = Value(87.93)
        input_string = """
        not not {field}.{property} = {value}
        """.format(
            field=variable.field,
            property=variable.property,
            value=value.value)
        with self._mock_rule('variable', lambda e: variable):
            result = self._transform_input_string(input_string)
            self.assertEqual(
                Condition(variable, OP_EQ, value, is_negated=False), result,
                "The Condition object should be equivalent to "
                "the negated condition"
            )

    def test_rule_cond_returns_negated_condition_if_notx3_var_op_val(self):
        variable = Variable("titles", "similarity")
        value = Value(87.93)
        input_string = """
        not not not {field}.{property} = {value}
        """.format(
            field=variable.field,
            property=variable.property,
            value=value.value)
        with self._mock_rule('variable', lambda e: variable):
            result = self._transform_input_string(input_string)
            self.assertEqual(
                Condition(variable, OP_EQ, value, is_negated=True), result,
                "The Condition object should be equivalent to "
                "the negated condition"
            )

    def test_rule_cond_returns_negated_condition_if_not_nested(self):
        variable = Variable("titles", "similarity")
        input_string = """
        not ({field}.{property})
        """.format(
            field=variable.field,
            property=variable.property)
        with self._mock_rule('variable', lambda e: variable):
            result = self._transform_input_string(input_string)
            self.assertEqual(
                Condition(variable, OP_EQ, Value(True), is_negated=True), result,
                "The Condition object should be equivalent to "
                "the negated condition"
            )

    def test_rule_cond_returns_condition_if_notx2_nested(self):
        variable = Variable("titles", "similarity")
        input_string = """
        not not ({field}.{property})
        """.format(
            field=variable.field,
            property=variable.property)
        with self._mock_rule('variable', lambda e: variable):
            result = self._transform_input_string(input_string)
            self.assertEqual(
                Condition(variable, OP_EQ, Value(True), is_negated=False), result,
                "The Condition object should be equivalent to the condition"
            )

    def test_rule_cond_returns_negated_condition_if_notx3_nested(self):
        variable = Variable("titles", "similarity")
        input_string = """
        not not not ({field}.{property})
        """.format(
            field=variable.field,
            property=variable.property)
        with self._mock_rule('variable', lambda e: variable):
            result = self._transform_input_string(input_string)
            self.assertEqual(
                Condition(variable, OP_EQ, Value(True), is_negated=True), result,
                "The Condition object should be equivalent to "
                "the negated condition"
            )

    def test_rule_condand_returns_condition_if_cond(self):
        variable = Variable("years", "are_same")
        condition = Condition(variable, OP_EQ, Value(True))
        input_string = """
        {field}.{property}
        """.format(field=variable.field, property=variable.property)
        with self._mock_rule('cond', lambda e: condition),\
                self._mock_rule('condor', lambda e: e[0]):
            result = self._transform_input_string(input_string)
            self.assertEqual(
                condition, result,
                "The Condition object should be equivalent to the condition"
            )

    def test_rule_condand_returns_condition_cond_and_cond_if_and(self):
        variable = Variable("years", "are_same")
        condition = Condition(variable, OP_EQ, Value(True))
        input_string = """
        {field}.{property} and {field}.{property}
        """.format(field=variable.field, property=variable.property)
        with self._mock_rule('cond', lambda e: condition),\
                self._mock_rule('condor', lambda e: e[0]):
            result = self._transform_input_string(input_string)
            self.assertEqual(
                Condition(condition, OP_AND, condition), result,
                "The Condition object should be equivalent to the condition"
            )

    def test_rule_condor_returns_condition_if_cond(self):
        variable = Variable("years", "are_same")
        condition = Condition(variable, OP_EQ, Value(True))
        input_string = """
        {field}.{property}
        """.format(field=variable.field, property=variable.property)
        with self._mock_rule('condand', lambda e: condition):
            result = self._transform_input_string(input_string)
            self.assertEqual(
                condition, result,
                "The Condition object should be equivalent to the condition"
            )

    def test_rule_condor_returns_condition_cond_or_cond_if_or(self):
        variable = Variable("years", "are_same")
        condition = Condition(variable, OP_EQ, Value(True))
        input_string = """
        {field}.{property} or {field}.{property}
        """.format(field=variable.field, property=variable.property)
        with self._mock_rule('condand', lambda e: condition):
            result = self._transform_input_string(input_string)
            self.assertEqual(
                Condition(condition, OP_OR, condition), result,
                "The Condition object should be equivalent to the condition"
            )

    def test_rule_rules_returns_rule_with_correct_id_desc_result(self):
        id, desc, result = "Rule1", "This is the rule", Rule.Result.MATCH
        condition = Mock()
        rule = Rule(id, desc, condition, result)
        input_string = """
        {id}: {desc}
        years.are_same => {result}
        """.format(id=id, desc=desc, result=result.value.lower())
        with self._mock_rule('condor', lambda e: condition):
            result = self._transform_input_string(input_string, start='rules')
            self.assertEqual(rule, result[0])

    def test_rule_rules_returns_rule_with_none_desc_if_empty_desc(self):
        id, result = "Rule1", Rule.Result.MATCH
        condition = Mock()
        rule = Rule(id, None, condition, result)
        input_string = """
        Rule1: 
        years.are_same => match
        """.format(id=id, result=result.value.lower())
        with self._mock_rule('condor', lambda e: condition):
            result = self._transform_input_string(input_string, start='rules')
            self.assertEqual(rule, result[0])

    def test_raises_compilation_error_if_duplicate_rule_id(self):
        input_string = """
        Rule1: This is the first rule
        titles.similarity > 85.50 and years.are_same => match
        
        Rule2: This is the second rule
        titles.similarity < 50 => mismatch
        
        Rule1: This is the third rule (id is duplicate)
        years.difference > 10 => mismatch
        """
        with self._mock_rule('condor', lambda e: Mock()):
            with self.assertRaises(VisitError) as context:
                self._transform_input_string(input_string, start='rules')
            self.assertIn(
                "Rule id 'Rule1' already exists: (line 2, column 9) and "
                "(line 8, column 9)",
                context.exception.args[0])

    def test_does_not_raise_error_if_duplicate_rule_id_in_diff_compilations(
            self):
        input_string_1 = """
        Rule1: This is the first rule
        titles.similarity > 85.50 and years.are_same => match
        
        Rule2: This is the second rule
        titles.similarity < 50 => mismatch
        """
        input_string_2 = """
        Rule1: This is the third rule (id is duplicate)
        years.difference > 10 => mismatch
        """
        with self._mock_rule('condor', lambda e: Mock()):
            self._transform_input_string(input_string_1, start='rules')
            try:
                self._transform_input_string(input_string_2, start='rules')
            except VisitError:
                self.fail(
                    "VisitError raised when no duplicate rule ids")

if __name__ == '__main__':
    unittest.main()
