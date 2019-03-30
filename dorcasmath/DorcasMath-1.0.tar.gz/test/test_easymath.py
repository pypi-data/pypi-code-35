from easy_math import math
from unittest import TestCase

class TestEasyMath(TestCase):
    def test_add(self):
        self.assertEqual(2, math.add(1, 1))
        self.assertEqual(30, math.add(15, 15))
    def test_division(self):
        self.assertEqual(4, math.division(8, 2))
        self.assertEqual(1, math.division(9, 9))
    def test_modular(self):
        self.assertEqual(0, math.modular(4, 4))
        self.assertEqual(1, math.modular(6, 5))
    def test_multiplication(self):
        self.assertEqual(9, math.multiplication(3,3))
        self.assertEqual(625, math.multiplication(25,25))
        self.assertEqual(0, math.multiplication(0,0))




