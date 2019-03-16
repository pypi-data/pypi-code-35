# This files serves to fix the coverage.py issues for producing
# coverage reports on TravisCI, which are then uploaded on Codecov.io


# REF: Testing with the "unittest" module.
# e.g. can put below code in enhancesa/tests/tests.py
# from unittest import TestCase
# import enhancesa
# from enhancesa.command_line import main

# # The hello() module
# class Testhello(TestCase):
#     def test_is_string(self):
#         s = enhancesa.hello()
#         self.assertTrue(isinstance(s, str))

# # The command_line in / folder
# class TestConsole(TestCase):
#     def test_basic(self):
#         main()