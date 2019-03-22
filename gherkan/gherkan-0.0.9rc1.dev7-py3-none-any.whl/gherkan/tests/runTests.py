import unittest
import gherkan.utils.constants as c
import os
"""
This code will gather and run all the tests in this directory. Files with tests must start with the "test_" prefix.
"""

unittest.TestCase.host = "localhost"
unittest.TestCase.port = 5000

loader = unittest.TestLoader()
testSuite = loader.discover(os.path.dirname(os.path.abspath(__file__)))

testRunner = unittest.TextTestRunner(verbosity=2)
testRunner.run(testSuite)
