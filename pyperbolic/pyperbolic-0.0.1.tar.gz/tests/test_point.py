"""Test for util module"""


import numpy
import unittest
from pyperbolic.point import Point
from pyperbolic import util


class PointTests(unittest.TestCase):
    def test_construct_points(self):
        p1 = Point(1, 2, 3)
        p2 = Point(numpy.array([4, 5, 6]))
        p3 = Point([1, 2, 3])
        with self.assertRaises(util.PyperbolicError):
            Point('a', 'b', 'c') # invalid

    def test_coercion(self):
        p = Point(1, 2, 3)
        p2 = p + (3, 4, 5)
        p3 = 4*p
        self.assertIsInstance(p2, Point)
        self.assertIsInstance(p3, Point)

    def test_point_addition(self):
        p1 = Point(1, 2, 3)
        p2 = Point(4, 3, 7)
        p3 = p1 + p2
        self.assertEqual(str(p3), "(5, 5, 10)")

    def test_scalar_multiplication(self):
        p = Point(1, 2, 3)
        p2 = 3*p
        self.assertEqual(str(p2), "(3, 6, 9)")
