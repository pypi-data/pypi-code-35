import math
import unittest
from json import loads

from rover_position_rjg.data.vector import Vector


class VectorTest(unittest.TestCase):
    def test_zero(self):
        vector = Vector.zero()
        self.assertEqual(vector, Vector([0, 0, 0]))

    def test_one(self):
        vector = Vector.one()
        self.assertEqual(vector, Vector([1, 1, 1]))

    def test_get_x(self):
        vector = Vector([1, 2, 3])
        self.assertEqual(vector.x, 1)

    def test_get_y(self):
        vector = Vector([1, 2, 3])
        self.assertEqual(vector.y, 2)

    def test_get_z(self):
        vector = Vector([1, 2, 3])
        self.assertEqual(vector.z, 3)

    def test_magnitude(self):
        vector = Vector([1, 2, 3])
        self.assertEqual(math.sqrt(1 + 4 + 9), vector.magnitude())

    def test_equal(self):
        one = Vector([1, 2, 3])
        copy = Vector([1, 2, 3])
        self.assertTrue(one == one)
        self.assertTrue(one == copy)
        self.assertTrue(copy == one)
        self.assertFalse(one == Vector([2, 2, 3]))
        self.assertFalse(one == Vector([1, 3, 3]))
        self.assertFalse(one == Vector([1, 2, 4]))
        self.assertFalse(one == 'str')

    def test_not_equal(self):
        one = Vector([1, 2, 3])
        copy = Vector([1, 2, 3])
        self.assertFalse(one != one)
        self.assertFalse(one != copy)
        self.assertFalse(copy != one)
        self.assertTrue(one != Vector([2, 2, 3]))
        self.assertTrue(one != Vector([1, 3, 3]))
        self.assertTrue(one != Vector([1, 2, 4]))
        self.assertTrue(one != 'str')

    def test_add(self):
        a = Vector([1, 2, 3])
        b = Vector([10, 11, 12])
        c = a + b
        self.assertEqual(11, c.x)
        self.assertEqual(13, c.y)
        self.assertEqual(15, c.z)

    def test_subtract(self):
        a = Vector([1, 2, 3])
        b = Vector([1, 3, 1])
        c = a - b
        self.assertEqual(0, c.x)
        self.assertEqual(-1, c.y)
        self.assertEqual(2, c.z)

    def test_multiply(self):
        a = Vector([1, 2, 3])
        actual = a * 1.5
        self.assertEqual(Vector([1.5, 3, 4.5]), actual)

    def test_divide(self):
        a = Vector([1, 2, 3])
        actual = a / 2
        self.assertEqual(Vector([0.5, 1.0, 1.5]), actual)

    def test_scale(self):
        a = Vector([1, 2, 3])
        b = Vector([3, -3, 4])
        c = a.scale(b)
        self.assertEqual(3, c.x)
        self.assertEqual(-6, c.y)
        self.assertEqual(12, c.z)

    def test_repr(self):
        a = Vector([1, 2.45, 3.56789])
        self.assertEqual('[1,2.45,3.56789]', repr(a))

    def test_str(self):
        a = Vector([1234.56789, 2.450, 3.56789])
        self.assertEqual('[1234.5679, 2.4500, 3.5679]', str(a))

    def test_to_json(self):
        v = Vector([1, 2, 3])
        actual = v.to_json()
        self.assertEqual('{"x":1, "y":2, "z":3}', actual)

    def test_from_json(self):
        obj = loads('{"x":1.5, "y":2.5, "z":3.5}')
        v = Vector.from_json(obj)
        self.assertEqual(Vector([1.5, 2.5, 3.5]), v)

    def test_enu_to_ned(self):
        enu = Vector([3, 2, 1])
        ned = enu.enu_to_ned()
        self.assertEqual(Vector([2, 3, -1]), ned)

    def test_ned_to_enu(self):
        ned = Vector([2, 3, -1])
        enu = ned.ned_to_enu()
        self.assertEqual(Vector([3, 2, 1]), enu)

    def test_less_than(self):
        v = Vector.zero()
        self.assertTrue(v < Vector([0.1, 0.1, 0.1]))
        self.assertFalse(v < Vector.zero())
        self.assertFalse(v < Vector([-0.1, -0.1, -0.1]))
        self.assertFalse(v < Vector([-0.1, 0.1, 0.1]))
        self.assertFalse(v < Vector([0.1, -0.1, 0.1]))
        self.assertFalse(v < Vector([0.1, 0.1, -0.1]))

    def test_greater_than(self):
        v = Vector.zero()
        self.assertTrue(v > Vector([-0.1, -0.1, -0.1]))
        self.assertFalse(v > Vector.zero())
        self.assertFalse(v > Vector([0.1, 0.1, 0.1]))
        self.assertFalse(v > Vector([0.1, -0.1, -0.1]))
        self.assertFalse(v > Vector([-0.1, 0.1, -0.1]))
        self.assertFalse(v > Vector([-0.1, -0.1, 0.1]))


if __name__ == '__main__':
    unittest.main()
