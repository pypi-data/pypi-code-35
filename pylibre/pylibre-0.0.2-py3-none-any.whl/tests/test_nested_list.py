from unittest import TestCase
from unittest.mock import patch
import sys
# from StringIO import StringIO
from io import StringIO
from niekas import NestedList, Note


class MyTestCase(TestCase):
    def test_tmp(self):
        self.assertEqual(1, 1.)
    def test_tmpw(self):
        self.assertEqual(1, 1.)

    def test_print_value(self):
        sys.stdout = StringIO()

        value = 'Hello world!'
        print(value, end='')

        self.assertEqual(sys.stdout.getvalue(), value)
        sys.stdout = sys.__stdout__

    @patch('os.popen')
    def test_print_value(self, popen_mock):
        sys.stdout = StringIO()
        popen_mock.return_value = StringIO('36 143\n')
        nl = NestedList('tests/fixtures/notes.txt')
        nl.show_list()
        expected = '[ ] '.join(['Vienas\n', 'Du\n', 'Trys'])
        result = sys.stdout.getvalue()
        self.assertEqual(result, expected)
        sys.stdout = sys.__stdout__
        print('Expected:\n', expected)
        print('Result:\n', result)
