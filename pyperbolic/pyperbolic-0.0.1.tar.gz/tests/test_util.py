"""Test for util module"""


import unittest
from pyperbolic import util


class UtilTests(unittest.TestCase):
    def test_pyperbolic_error(self):
        with self.assertRaises(util.PyperbolicError):
            raise util.PyperbolicError('Sample error')
