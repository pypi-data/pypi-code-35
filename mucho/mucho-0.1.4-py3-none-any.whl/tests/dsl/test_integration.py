import os
import unittest

from lark import Lark

from mucho.dsl.compiler import Compiler
from mucho.dsl.compiler import CompilationError
from mucho.dsl.virtualmachine import VirtualMachine, ExecutionError
from mucho.comparison.comparator import (
    EntityComparator, DimensionComparator, DimensionProperty)
from mucho.comparison.result import ComparisonResult


class TitlesComparator(DimensionComparator):
    similarity_max = DimensionProperty()

    def resolve_similarity_max(self, src, trg):
        pass


class YearsComparator(DimensionComparator):
    are_same = DimensionProperty()
    difference = DimensionProperty()

    def resolve_are_same(self, str, trg):
        pass

    def resolve_difference(self, str, trg):
        pass


class WorksComparator(EntityComparator):
    titles = TitlesComparator()
    years = YearsComparator()


class InterpreterTestCase(unittest.TestCase):
    GRAMMAR_FILE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', '..', 'classifiers', 'rulebased',
        'compiler', 'grammar', 'rules.lrk',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.compiler = Compiler(comparator=WorksComparator())
        self.virtual_machine = VirtualMachine()

    def _get_parser(self, start):
        return Lark(open(self.GRAMMAR_FILE), start=start)

    def _interpret(self, text, result):
        rules = self.compiler.compile(text)
        return self.virtual_machine.run(rules, result)

    def _generate_comparison_result(self, values):
        result = ComparisonResult()
        for field_property, value in values.items():
            field, property = field_property.split('.')
            result_field = getattr(result, field, None)
            if not result_field:
                result_field = ComparisonResult()
                setattr(result, field, result_field)
            setattr(result_field, property, value)
        return result

    def test_variable_boolean_with_false_is_false(self):
        comparison_result = self._generate_comparison_result({
            'years.are_same': False,
        })
        text = """
        R1:
        years.are_same
        => match
        """
        self.assertIsNone(self._interpret(text, comparison_result))

    def test_variable_boolean_with_true_is_true(self):
        comparison_result = self._generate_comparison_result({
            'years.are_same': True,
        })
        text = """
        R1:
        years.are_same
        => match
        """
        self.assertEqual("R1", self._interpret(text, comparison_result).id)

    def test_negated_variable_boolean_with_true_is_false(self):
        comparison_result = self._generate_comparison_result({
            'years.are_same': True,
        })
        text = """
        R1:
        not years.are_same
        => match
        """
        self.assertIsNone(self._interpret(text, comparison_result))

    def test_variable_int_with_0_is_false(self):
        comparison_result = self._generate_comparison_result({
            'years.difference': 0,
        })
        text = """
        R1:
        years.difference
        => match
        """
        self.assertIsNone(self._interpret(text, comparison_result))

    def test_negated_variable_int_with_0_is_true(self):
        comparison_result = self._generate_comparison_result({
            'years.difference': 0,
        })
        text = """
        R1:
        not years.difference
        => match
        """
        self.assertEqual('R1', self._interpret(text, comparison_result).id)

    def test_variable_int_with_ne0_is_false(self):
        comparison_result = self._generate_comparison_result({
            'years.difference': 2,
        })
        text = """
        R1:
        years.difference
        => match
        """
        self.assertIsNone(self._interpret(text, comparison_result))

    def test_variable_float_with_0_is_false(self):
        comparison_result = self._generate_comparison_result({
            'years.difference': 0.0,
        })
        text = """
        R1:
        years.difference
        => match
        """
        self.assertIsNone(self._interpret(text, comparison_result))

    def test_negated_variable_float_with_0_is_true(self):
        comparison_result = self._generate_comparison_result({
            'years.difference': 0.0,
        })
        text = """
        R1:
        not years.difference
        => match
        """
        self.assertEqual('R1', self._interpret(text, comparison_result).id)

    def test_variable_float_with_ne0_is_false(self):
        comparison_result = self._generate_comparison_result({
            'years.difference': 2.0,
        })
        text = """
        R1:
        years.difference
        => match
        """
        self.assertIsNone(self._interpret(text, comparison_result))

    def test_variable_nested_boolean_with_false_is_false(self):
        comparison_result = self._generate_comparison_result({
            'years.are_same': False,
        })
        text = """
        R1:
        (years.are_same)
        => match
        """
        self.assertIsNone(self._interpret(text, comparison_result))

    def test_negated_variable_nested_boolean_with_false_is_true(self):
        comparison_result = self._generate_comparison_result({
            'years.are_same': False,
        })
        text = """
        R1:
        not (years.are_same)
        => match
        """
        self.assertEqual('R1', self._interpret(text, comparison_result).id)

    def test_variable_nested_boolean_with_true_is_true(self):
        comparison_result = self._generate_comparison_result({
            'years.are_same': True,
        })
        text = """
        R1:
        (years.are_same)
        => match
        """
        self.assertEqual("R1", self._interpret(text, comparison_result).id)

    def test_comparison_with_eq_with_true_is_true(self):
        comparison_result = self._generate_comparison_result({
            'years.difference': 2,
        })
        text = """
        R1:
        years.difference = 2
        => match
        """
        self.assertEqual("R1", self._interpret(text, comparison_result).id)

    def test_negated_comparison_with_eq_with_true_is_false(self):
        comparison_result = self._generate_comparison_result({
            'years.difference': 2,
        })
        text = """
        R1:
        not years.difference = 2
        => match
        """
        self.assertIsNone(self._interpret(text, comparison_result))

    def test_comparison_with_eqeq_with_true_is_true(self):
        comparison_result = self._generate_comparison_result({
            'years.difference': 2,
        })
        text = """
        R1:
        years.difference == 2
        => match
        """
        self.assertEqual("R1", self._interpret(text, comparison_result).id)

    def test_comparison_with_eq_with_false_is_false(self):
        comparison_result = self._generate_comparison_result({
            'years.difference': 2,
        })
        text = """
        R1:
        years.difference = 3
        => match
        """
        self.assertIsNone(self._interpret(text, comparison_result))

    def test_comparison_with_eqeq_with_false_is_false(self):
        comparison_result = self._generate_comparison_result({
            'years.difference': 2,
        })
        text = """
        R1:
        years.difference == 3
        => match
        """
        self.assertIsNone(self._interpret(text, comparison_result))

    def test_comparison_nested_with_eq_with_true_is_true(self):
        comparison_result = self._generate_comparison_result({
            'years.difference': 2,
        })
        text = """
        R1:
        (years.difference = 2)
        => match
        """
        self.assertEqual("R1", self._interpret(text, comparison_result).id)

    def test_and_with_false_false_is_false(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 88.55,
            'years.difference': 2,
        })
        text = """
        R1:
        titles.similarity_max = 88.50 and years.difference > 2
        => match
        """
        self.assertIsNone(self._interpret(text, comparison_result))

    def test_and_with_false_true_is_false(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 88.55,
            'years.difference': 2,
        })
        text = """
        R1:
        titles.similarity_max = 88.50 and years.difference >= 2
        => match
        """
        self.assertIsNone(self._interpret(text, comparison_result))

    def test_and_with_negated_false_true_is_true(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 88.55,
            'years.difference': 2,
        })
        text = """
        R1:
        not titles.similarity_max = 88.50 and years.difference >= 2
        => match
        """
        self.assertEqual('R1', self._interpret(text, comparison_result).id)

    def test_and_with_true_false_is_false(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 88.55,
            'years.difference': 2,
        })
        text = """
        R1:
        titles.similarity_max > 88.50 and years.difference < 2
        => match
        """
        self.assertIsNone(self._interpret(text, comparison_result))

    def test_and_with_true_true_is_true(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 88.55,
            'years.difference': 2,
        })
        text = """
        R1:
        titles.similarity_max > 88.50 and years.difference = 2
        => match
        """
        self.assertEqual("R1", self._interpret(text, comparison_result).id)

    def test_or_with_false_false_is_false(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 88.55,
            'years.difference': 2,
        })
        text = """
        R1:
        titles.similarity_max = 88.50 or years.difference > 2
        => match
        """
        self.assertIsNone(self._interpret(text, comparison_result))

    def test_or_with_false_not_false_is_true(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 88.55,
            'years.difference': 2,
        })
        text = """
        R1:
        titles.similarity_max = 88.50 or not years.difference > 2
        => match
        """
        self.assertEqual('R1', self._interpret(text, comparison_result).id)

    def test_or_with_false_true_is_true(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 88.55,
            'years.difference': 2,
        })
        text = """
        R1:
        titles.similarity_max = 88.50 or years.difference >= 2
        => match
        """
        self.assertEqual("R1", self._interpret(text, comparison_result).id)

    def test_or_with_true_false_is_true(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 88.55,
            'years.difference': 2,
        })
        text = """
        R1:
        titles.similarity_max > 88.50 or years.difference < 2
        => match
        """
        self.assertEqual("R1", self._interpret(text, comparison_result).id)

    def test_or_with_true_true_is_true(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 88.55,
            'years.difference': 2,
        })
        text = """
        R1:
        titles.similarity_max > 88.50 or years.difference = 2
        => match
        """
        self.assertEqual("R1", self._interpret(text, comparison_result).id)

    def test_and_has_higher_precedence_than_or(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 88.55,
            'years.are_same': False,
            'years.difference': 2,
        })
        text = """
        R1:
        titles.similarity_max > 88.50
        or years.difference = 2
        and years.are_same
        => match
        """
        self.assertEqual("R1", self._interpret(text, comparison_result).id)

    def test_nested_has_higher_precedence_than_and(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 88.55,
            'years.are_same': False,
            'years.difference': 2,
        })
        text = """
        R1:
        (titles.similarity_max > 88.50 or years.difference = 2)
        and years.are_same => match
        """
        self.assertIsNone(self._interpret(text, comparison_result))

    def test_not_has_higher_precedence_than_or(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 88.55,
            'years.are_same': False,
            'years.difference': 2,
        })
        text = """
        R1:
        not titles.similarity_max = 88.5 or years.difference = 2
        => match
        """
        self.assertEqual('R1', self._interpret(text, comparison_result).id)

    def test_nested_has_higher_precedence_than_not(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 88.55,
            'years.are_same': False,
            'years.difference': 2,
        })
        text = """
        R1:
        not (titles.similarity_max = 100 and years.difference = 3)
        => match
        """
        self.assertEqual('R1', self._interpret(text, comparison_result).id)

    def test_unknown_var_field_raises_error(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 88.55,
            'years.are_same': False,
            'years.difference': 2,
        })
        text = """
        R1:
        (titles.similarity_max > 88.50 or years.difference = 2)
        and directors.are_same
        => unknown
        """
        with self.assertRaises(CompilationError) as assert_context:
            self._interpret(text, comparison_result)
        self.assertIn(
            "Unknown dimension 'directors'",
            assert_context.exception.args[0])

    def test_unknown_var_property_raises_error(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 88.55,
            'years.are_same': False,
            'years.difference': 2,
        })
        text = """
        R1:
        (titles.similarity_max > 88.50 or years.difference = 2)
        and years.are_similar
        => match
        """
        with self.assertRaises(CompilationError) as assert_context:
            self._interpret(text, comparison_result)
        self.assertIn(
            "Unknown property 'are_similar'",
            assert_context.exception.args[0])

    def test_out_of_context_var_field_raises_error(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 88.55,
        })
        text = """
        R1:
        (titles.similarity_max > 88.50 or years.difference = 2)
        and years.are_same
        => mismatch
        """
        with self.assertRaises(ExecutionError) as assert_context:
            self._interpret(text, comparison_result)
        self.assertEqual(
            "Field 'years' not in context",
            assert_context.exception.args[0])

    def test_out_of_context_var_property_raises_error(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 88.55,
            'years.difference': 2,
        })
        text = """
        R1:
        (titles.similarity_max > 88.50 or years.difference = 2)
        and years.are_same
        => match
        """
        with self.assertRaises(ExecutionError) as assert_context:
            self._interpret(text, comparison_result)
        self.assertEqual(
            "Property 'years.are_same' not in context",
            assert_context.exception.args[0])

    def test_interpret_returns_first_rule_with_true_condition_if_any(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 55.45,
            'years.difference': 8,
            'years.are_same': False,
        })
        text = """
        R1: Exact match
        titles.similarity_max >= 85.5 and years.are_same => match
        
        R2: Fuzzy match
        titles.similarity_max >= 85.5 => unknown
        
        R3: Mismatch
        titles.similarity_max < 60 and years.difference > 5 => mismatch
        """
        result = self._interpret(text, comparison_result)
        self.assertEqual(result.id, "R3")

    def test_interpret_returns_none_if_no_true_rules(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 65.45,
            'years.difference': 8,
            'years.are_same': False,
        })
        text = """
        R1: Exact match
        titles.similarity_max >= 85.5 and years.are_same => match
        
        R2: Fuzzy match
        titles.similarity_max >= 85.5 => unknown
        
        R3: Mismatch
        titles.similarity_max < 60 and years.difference > 5 => mismatch
        """
        result = self._interpret(text, comparison_result)
        self.assertIsNone(result)

    def test_raises_transformation_error_if_duplicate_rule_ids(self):
        comparison_result = self._generate_comparison_result({
            'titles.similarity_max': 65.45,
            'years.difference': 8,
            'years.are_same': False,
        })
        text = """
        R1: Exact match
        titles.similarity_max >= 85.5 and years.are_same => match
        
        R2: Fuzzy match
        titles.similarity_max >= 85.5 => unknown
        
        R1: Mismatch
        titles.similarity_max < 60 and years.difference > 5 => mismatch
        """
        with self.assertRaises(CompilationError) as context:
            self._interpret(text, comparison_result)
        self.assertEqual("Rule id 'R1' already exists: (line 2, column 9) "
                         "and (line 8, column 9)", context.exception.args[0])

if __name__ == '__main__':
    unittest.main()
