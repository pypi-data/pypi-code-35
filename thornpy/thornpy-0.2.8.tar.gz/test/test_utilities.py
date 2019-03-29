"""Tests functions in the utilities module.

"""
import unittest
from thornpy import utilities
from test import *

class Test_Utilities(unittest.TestCase):

    def setUp(self):
        return

    def test_num_to_ith(self):
        ordinals = [utilities.num_to_ith(num) for num in TEST_INTEGERS]
        self.assertEqual(ordinals, TEST_EXPECTED_ORDINALS)

    def tearDown(self):
        return