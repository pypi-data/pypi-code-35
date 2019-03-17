import os
import unittest

from lark import Lark
from lark.exceptions import UnexpectedCharacters, ParseError


class RulesGrammarTestCase(unittest.TestCase):
    GRAMMAR_FILE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', '..', '..', '..',
        'mucho', 'dsl', 'compiler', 'grammar', 'rules.lrk',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser_condor = Lark(open(self.GRAMMAR_FILE), start='condor')
        self.parser_rules = Lark(open(self.GRAMMAR_FILE), start='rules')

    def assert_is_variable_in_tree(self, variable_name, tree, msg=None):
        field, property = variable_name.split('.')
        self.assertEqual(
            1,
            len(list(tree.find_pred(
                lambda node: len(node.children) == 2
                and getattr(node.children[0], 'value', None) == field
                and getattr(node.children[1], 'value', None) == property
            ))),
            msg)

    def test_accept_isolated_variables(self):
        input_string = """
        titles.similarity
        """
        try:
            self.parser_condor.parse(input_string)
        except (UnexpectedCharacters, ParseError):
            self.fail("Grammar should accept an isolated variable")

    def test_accept_negated_variable(self):
        input_string = """
        not types.are_episode
        """
        try:
            self.parser_condor.parse(input_string)
        except (UnexpectedCharacters, ParseError):
            self.fail("Grammar should accept negated variables")

    def test_accept_n_negated_variable(self):
        input_string = """
        not not not types.are_episode
        """
        try:
            self.parser_condor.parse(input_string)
        except (UnexpectedCharacters, ParseError):
            self.fail("Grammar should accept negated variables")

    def test_raise_if_variables_do_not_contain_dot(self):
        input_string = """
        titles
        """
        with self.assertRaises(ParseError) as context:
            self.parser_condor.parse(input_string)
        self.assertIn(
            "Expecting a terminal of: [Terminal('DOT')]",
            context.exception.args[0],
            "Grammar should not accept variables without dot"
        )

    def test_raise_if_variables_contain_2_dots(self):
        input_string = """
        titles.similarity.max
        """
        with self.assertRaises(UnexpectedCharacters) as context:
            self.parser_condor.parse(input_string)

    def test_raise_if_isolated_value_are_float_numbers(self):
        input_string = """
        5.37
        """
        with self.assertRaises(UnexpectedCharacters) as context:
            self.parser_condor.parse(input_string)

    def test_raise_if_isolated_values_are_int_number(self):
        input_string = """
        5
        """
        with self.assertRaises(UnexpectedCharacters) as context:
            self.parser_condor.parse(input_string)

    def test_accept_comparisons_between_variables_and_values(self):
        input_string = """
        titles.similarity = 5.37
        """
        try:
            self.parser_condor.parse(input_string)
        except (UnexpectedCharacters, ParseError):
            self.fail("Grammar should accept an variable-value comparisons")

    def test_accept_negated_comparisons_between_variables_and_values(self):
        input_string = """
        not titles.similarity = 5.37
        """
        try:
            self.parser_condor.parse(input_string)
        except (UnexpectedCharacters, ParseError):
            self.fail(
                "Grammar should accept negated variable-value comparisons")

    def test_accept_n_negated_comparisons_between_variables_and_values(self):
        input_string = """
        not not not titles.similarity = 5.37
        """
        try:
            self.parser_condor.parse(input_string)
        except (UnexpectedCharacters, ParseError):
            self.fail(
                "Grammar should accept negated variable-value comparisons")

    def test_raise_if_comparisons_between_values_and_variables(self):
        input_string = """
        5.37 = titles.similarity
        """
        with self.assertRaises(UnexpectedCharacters) as context:
            self.parser_condor.parse(input_string)

    def test_accept_logical_conditions_with_and(self):
        input_string = """
        titles.similarity >= 90 and years.are_same
        """
        try:
            self.parser_condor.parse(input_string)
        except (UnexpectedCharacters, ParseError):
            self.fail("Grammar should accept logical conditions with and")

    def test_accept_logical_conditions_with_or(self):
        input_string = """
        titles.similarity >= 90 or years.are_same
        """
        try:
            self.parser_condor.parse(input_string)
        except (UnexpectedCharacters, ParseError):
            self.fail("Grammar should accept logical conditions with or")

    def test_accept_nested_logical_conditions(self):
        input_string = """
        (years.are_same or years.difference = 1)
        """
        try:
            self.parser_condor.parse(input_string)
        except (UnexpectedCharacters, ParseError):
            self.fail("Grammar should accept nested logical conditions")

    def test_accept_negated_nested_logical_conditions(self):
        input_string = """
        not (years.are_same or years.difference = 1)
        """
        try:
            self.parser_condor.parse(input_string)
        except (UnexpectedCharacters, ParseError):
            self.fail("Grammar should accept nested logical conditions")

    def test_accept_n_negated_nested_logical_conditions(self):
        input_string = """
        not not not (years.are_same or years.difference = 1)
        """
        try:
            self.parser_condor.parse(input_string)
        except (UnexpectedCharacters, ParseError):
            self.fail("Grammar should accept nested logical conditions")

    def test_logical_and_has_higher_precedence_than_logical_or(self):
        input_string = """
        titles.similarity >= 90 or years.are_same and years.difference = 1
        """
        tree = self.parser_condor.parse(input_string)
        operand_left = tree.children[0]
        operand_right = tree.children[1]
        self.assert_is_variable_in_tree(
            'titles.similarity', operand_left,
            'Logical OR should no have higher precedence than AND')
        self.assert_is_variable_in_tree(
            'years.are_same', operand_right,
            'Logical OR should no have higher precedence than AND')
        self.assert_is_variable_in_tree(
            'years.difference', operand_right,
            'Logical OR should no have higher precedence than AND')

    def test_nested_has_higher_precedence_than_logical_and(self):
        input_string = """
        (titles.similarity >= 90 or years.are_same) and years.difference = 1
        """
        tree = self.parser_condor.parse(input_string)
        operand_left = tree.children[0].children[0]
        operand_right = tree.children[0].children[1]
        self.assert_is_variable_in_tree(
            'titles.similarity', operand_left,
            'Logical OR should no have higher precedence than AND')
        self.assert_is_variable_in_tree(
            'years.are_same', operand_left,
            'Logical OR should no have higher precedence than AND')
        self.assert_is_variable_in_tree(
            'years.difference', operand_right,
            'Logical OR should no have higher precedence than AND')

    def test_logical_not_has_higher_precedence_than_logical_and(self):
        input_string = """
        not titles.similarity >= 90 and years.are_same
        """
        tree = self.parser_condor.parse(input_string)
        operand_left = tree.children[0].children[0]
        operand_right = tree.children[0].children[1]
        self.assert_is_variable_in_tree(
            'titles.similarity', operand_left,
            'Logical NOT should have higher precedence than AND')
        self.assert_is_variable_in_tree(
            'years.are_same', operand_right,
            'Logical NOT should have higher precedence than AND')

    def test_logical_and_is_left_associative(self):
        input_string = """
        titles.similarity >= 90 and years.are_same and years.difference = 1
        """
        tree = self.parser_condor.parse(input_string)
        operand_left = tree.children[0].children[0]
        operand_right = tree.children[0].children[1]
        self.assert_is_variable_in_tree(
            'titles.similarity', operand_left,
            'Logical AND should be left-associative')
        self.assert_is_variable_in_tree(
            'years.are_same', operand_left,
            'Logical AND should be left-associative')
        self.assert_is_variable_in_tree(
            'years.difference', operand_right,
            'Logical AND should be left-associative')

    def test_logical_or_is_left_associative(self):
        input_string = """
        titles.similarity >= 90 or years.are_same or years.difference = 1
        """
        tree = self.parser_condor.parse(input_string)
        operand_left = tree.children[0]
        operand_right = tree.children[1]
        self.assert_is_variable_in_tree(
            'titles.similarity', operand_left,
            'Logical OR should be left-associative')
        self.assert_is_variable_in_tree(
            'years.are_same', operand_left,
            'Logical OR should be left-associative')
        self.assert_is_variable_in_tree(
            'years.difference', operand_right,
            'Logical OR should be left-associative')

    def test_rule_must_have_id(self):
        input_string = """
        titles.similarity >= 90 => match
        """
        with self.assertRaises(UnexpectedCharacters):
            self.parser_rules.parse(input_string)

    def test_rule_must_have_newline_after_header(self):
        input_string = """
        R1: titles.similarity >= 90 => match
        """
        with self.assertRaises(ParseError) as context:
            self.parser_rules.parse(input_string)
        self.assertIn("Unexpected end of input", context.exception.args[0])

    def test_rule_must_have_implies(self):
        input_string = """
        R1:
        titles.similarity == 90
        """
        with self.assertRaises(ParseError) as context:
            self.parser_rules.parse(input_string)
        self.assertIn("Unexpected end of input", context.exception.args[0])

    def test_rule_must_have_allowed_result_after_implies(self):
        input_string = """
        R1:
        titles.similarity >= 90 => half match
        """
        with self.assertRaises(UnexpectedCharacters):
            self.parser_rules.parse(input_string)

    def test_accept_rules_with_result_match_after_implies(self):
        input_string = """
        R1:
        titles.similarity >= 90 => match
        """
        try:
            tree = self.parser_rules.parse(input_string)
            self.assertEqual(1, len(tree.children))
        except (UnexpectedCharacters, ParseError):
            self.fail("Grammar should accept rules with match after implies")

    def test_accept_rules_with_result_mismatch_after_implies(self):
        input_string = """
        R1:
        titles.similarity >= 90 => mismatch
        """
        try:
            tree = self.parser_rules.parse(input_string)
            self.assertEqual(1, len(tree.children))
        except (UnexpectedCharacters, ParseError):
            self.fail(
                "Grammar should accept rules with mismatch after implies")

    def test_accept_rules_with_result_unknown_after_implies(self):
        input_string = """
        R1:
        titles.similarity >= 90 => unknown
        """
        try:
            tree = self.parser_rules.parse(input_string)
            self.assertEqual(1, len(tree.children))
        except (UnexpectedCharacters, ParseError):
            self.fail(
                "Grammar should accept rules with unknown after implies")

    def test_accept_rules_without_description(self):
        input_string = """
        R1:
        titles.similarity >= 90 => match
        """
        try:
            tree = self.parser_rules.parse(input_string)
            self.assertEqual(1, len(tree.children))
        except (UnexpectedCharacters, ParseError):
            self.fail("Grammar should accept rules without description")

    def test_accept_rules_with_description(self):
        input_string = """
        R1: The first rule to test
        titles.similarity >= 90 => match
        """
        try:
            tree = self.parser_rules.parse(input_string)
            self.assertEqual(1, len(tree.children))
        except (UnexpectedCharacters, ParseError):
            self.fail("Grammar should accept rules with description")

    def test_accept_rules_with_implies_symbol_1(self):
        input_string = """
        R1:
        titles.similarity >= 90 => match
        """
        try:
            tree = self.parser_rules.parse(input_string)
            self.assertEqual(1, len(tree.children))
        except (UnexpectedCharacters, ParseError):
            self.fail("Grammar should accept rules with implies symbol '=>'")

    def test_accept_rules_with_implies_symbol_2(self):
        input_string = """
        R1:
        titles.similarity >= 90 ⇒ match
        """
        try:
            tree = self.parser_rules.parse(input_string)
            self.assertEqual(1, len(tree.children))
        except (UnexpectedCharacters, ParseError):
            self.fail("Grammar should accept rules with implies symbol '⇒'")

    def test_accept_several_rules_without_newline_separator(self):
        input_string = """
        R1:
        titles.similarity >= 90 ⇒ match R2: Second rule
        years.diff <=2 and titles.similarity >= 85.50 => match
        """
        try:
            tree = self.parser_rules.parse(input_string)
            self.assertEqual(2, len(tree.children))
        except (UnexpectedCharacters, ParseError):
            self.fail("Grammar should accept rules without newline separator")

    def test_accept_several_rules_with_newline_separator(self):
        input_string = """
        R1:
        titles.similarity >= 90 ⇒ match

        R2: Second rule
        years.diff <=2 and titles.similarity >= 85.50 => match
        """
        try:
            tree = self.parser_rules.parse(input_string)
            self.assertEqual(2, len(tree.children))
        except (UnexpectedCharacters, ParseError):
            self.fail("Grammar should accept rules with newline separator")

    def test_rules_with_and_without_newline_separator_are_equivalent(self):
        input_string_without_separator = """
        R1:
        titles.similarity >= 90 ⇒ match R2: Second rule
        years.diff <=2 and titles.similarity >= 85.50 => match
        """
        input_string_with_separator = """
        R1:
        titles.similarity >= 90 ⇒ match

        R2: Second rule
        years.diff <=2 and titles.similarity >= 85.50 => match
        """
        try:
            tree_1 = self.parser_rules.parse(input_string_without_separator)
            tree_2 = self.parser_rules.parse(input_string_with_separator)
            self.assertEqual(tree_1, tree_2)
        except (UnexpectedCharacters, ParseError):
            self.fail(
                "Same rules with/without newline separator are equivalent")

    def test_accept_rules_containing_newline_separator(self):
        input_string = """
        R1:
        titles.similarity >= 90
        ⇒ match

        R2: Second rule
        years.diff <=2
        and titles.similarity >= 85.50

        => match
        """
        try:
            tree = self.parser_rules.parse(input_string)
            self.assertEqual(2, len(tree.children))
        except (UnexpectedCharacters, ParseError):
            self.fail(
                "Grammar should accept rules containing newline separator")

    def test_accept_comments(self):
        input_string = """
        # First rule of the file
        R1:
        titles.similarity >= 90
        ⇒ match
        
        # Second rule of the file that
        # test the difference between
        # years
        R2: Second rule
        years.diff <=2
        and titles.similarity >= 85.50

        => match
        """
        try:
            tree = self.parser_rules.parse(input_string)
            self.assertEqual(2, len(tree.children))
        except (UnexpectedCharacters, ParseError):
            self.fail("Grammar should accept comments")


if __name__ == '__main__':
    unittest.main()
