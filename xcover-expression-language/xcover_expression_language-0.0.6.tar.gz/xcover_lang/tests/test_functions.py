from unittest import TestCase

from xcover_lang.utils import eval_expr


class VariableTestCase(TestCase):

    def test_assignment(self):
        expr = '''
        a = 1
        b = "string"
        c = {"foo": "bar"}
        d = [1, 2, 3]
        '''
        r, context = eval_expr(expr)

        self.assertEqual(context['a'], 1)
        self.assertEqual(context['b'], 'string')
        self.assertDictEqual(context['c'], {"foo": 'bar'})


class BuiltInFunctionTestCase(TestCase):
    def test_min(self):
        result, _ = eval_expr('min(2, 0)')
        self.assertEqual(result, 0)

    def test_max(self):
        result, _ = eval_expr('max(2, 0)')
        self.assertEqual(result, 2)

    def test_count(self):
        result, _ = eval_expr('count([1, 2, 3])')
        self.assertEqual(result, 3)

    def test_membership_testing(self):
        result, _ = eval_expr('"UK" in ["UK", "US"]')
        self.assertTrue(result)
        result, _ = eval_expr('"UK" in ["US"]')
        self.assertFalse(result)

    def test_if_cond_inline_test(self):
        self.assertEqual(eval_expr(
            '''
            if_cond(1 == 1, "yes", "no")
            '''
        )[0], "yes")

    def test_multiple_if_conditions(self):
        context = eval_expr(
            '''
            variable1 = if_cond(1 == 1, "yes", "no")
            variable2 = if_cond(variable1 == "yes", "yes2", "no2")
            '''
        )[1]
        expected = {'variable2': 'yes2'}
        self.assertTrue(set(expected.items()).issubset(set(context.items())))

    def test_if_cond_code_block_test(self):
        self.assertEqual(eval_expr(
            '''
            a = 1
            b = 2
            result = if_cond(a == b, "yes", "no")
            '''
        )[1]['result'], "no")

        # Test "and" in expression and False assignment
        # Return a number instead of a string
        self.assertEqual(eval_expr(
            '''
            a = 1
            b = False
            result = if_cond(a and b, "yes", 1)
            '''
        )[1]['result'], 1)

    def test_reduce_sum(self):
        """
        reduce_sum computes the sum of an attribute over a list of objects
        """
        result, context = eval_expr(
            '''
            dic = [{"value": 1}, {"value": 2}]
            result = reduce_sum(dic, "value")
            '''
        )
        self.assertEqual(3, context['result'])

    def test_number_of_days_without_params(self):
        """
        compares the number of days between two dates
        """
        result, context = eval_expr('''result = number_of_days("2017-01-10", "2017-01-20")''')
        self.assertEqual(10, context['result'])

    def test_number_of_days_with_only_rounding_params(self):
        """
        compares the number of days between two dates
        """
        result, context = eval_expr('''result = number_of_days("2017-01-10 11:00:00", "2017-01-11 10:00:00", round = "up")''')
        self.assertEqual(1, context['result'])

    def test_number_of_days_with_params(self):
        """
        compares the number of days between two dates
        """
        result, context = eval_expr('''result = number_of_days("2017-01-10", "2017-01-20", format = "YYYY-MM-DD", round = "up")''')
        self.assertEqual(10, context['result'])

    def test_number_of_days_rounding_up(self):
        result, context = eval_expr('''result = number_of_days("2017-01-10 11:00:00", "2017-01-11 10:00:00", format = "YYYY-MM-DD HH:mm:ss", round = "up")''')
        self.assertEqual(1, context['result'])

    def test_number_of_days_rounding_down(self):
        result, context = eval_expr('''result = number_of_days("2017-01-10 11:00:00", "2017-01-11 10:00:00", format = "YYYY-MM-DD HH:mm:ss", round = "down")''')
        self.assertEqual(0, context['result'])


