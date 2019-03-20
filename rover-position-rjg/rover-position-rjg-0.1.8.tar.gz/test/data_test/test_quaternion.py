import math
import unittest
from json import loads

from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector


class QuaternionTest(unittest.TestCase):
    def test_get_w(self):
        quaternion = Quaternion(1, 2, 3, 4)
        self.assertEqual(quaternion.w, 1)

    def test_get_i(self):
        quaternion = Quaternion(1, 2, 3, 4)
        self.assertEqual(quaternion.i, 2)

    def test_get_j(self):
        quaternion = Quaternion(1, 2, 3, 4)
        self.assertEqual(quaternion.j, 3)

    def test_get_k(self):
        quaternion = Quaternion(1, 2, 3, 4)
        self.assertEqual(quaternion.k, 4)

    def test_equal(self):
        one = Quaternion(1, 2, 3, 4)
        copy = Quaternion(1, 2, 3, 4)
        self.assertTrue(one == one)
        self.assertTrue(one == copy)
        self.assertTrue(copy == one)
        self.assertFalse(one == Quaternion(10, 2, 3, 4))
        self.assertFalse(one == Quaternion(1, 20, 3, 4))
        self.assertFalse(one == Quaternion(1, 2, 30, 4))
        self.assertFalse(one == Quaternion(1, 2, 3, 40))
        self.assertFalse(one == Quaternion(4, 3, 2, 1))
        self.assertFalse(one == 'str')

    def test_not_equal(self):
        one = Quaternion(1, 2, 3, 4)
        copy = Quaternion(1, 2, 3, 4)
        self.assertFalse(one != one)
        self.assertFalse(one != copy)
        self.assertFalse(copy != one)
        self.assertTrue(one != Quaternion(10, 2, 3, 4))
        self.assertTrue(one != Quaternion(1, 20, 3, 4))
        self.assertTrue(one != Quaternion(1, 2, 30, 4))
        self.assertTrue(one != Quaternion(1, 2, 3, 40))
        self.assertTrue(one != 'str')

    def test_identity(self):
        identity = Quaternion.identity()
        self.assertEqual(identity, Quaternion(1, 0, 0, 0))

    def test_repr(self):
        a = Quaternion(123, 1, 2.45, 3.56789)
        self.assertEqual('[123,1,2.45,3.56789]', repr(a))

    def test_magnitude(self):
        a = Quaternion(1, 2, 3, 4)
        self.assertAlmostEqual(5.4772, a.magnitude(), 4)

    def test_normalise(self):
        a = Quaternion(1, 2, 3, 4)
        mag = a.magnitude()
        expected = Quaternion(1/mag, 2/mag, 3/mag, 4/mag)
        self.assertEqual(expected, a.normalise())

    def test_to_json(self):
        q = Quaternion(123, 1, 2.45, 3.56789)
        actual = q.to_json()
        self.assertEqual('{"w":123, "i":1, "j":2.45, "k":3.56789}', actual)

    def test_from_json(self):
        dictionary = loads('{"w":123, "i":1, "j":2.45, "k":3.56789}')
        q = Quaternion.from_json(dictionary)
        self.assertEqual(Quaternion(123, 1, 2.45, 3.56789), q)

    def test_hamilton_product(self):
        # Using right hand rule.
        vector = Quaternion(0, 3, 1, 2)
        h = math.sqrt(0.5)
        # Yaw 90 degrees anticlockwise
        self.assert_rotation(vector, Quaternion(h, 0, h, 0), Quaternion(0, 2, 1, -3))
        # Yaw 180 degrees anticlockwise
        self.assert_rotation(vector, Quaternion(0, 0, 1, 0), Quaternion(0, -3, 1, -2))
        # Yaw 270 degrees anticlockwise, pitch up 90 degrees
        self.assert_rotation(vector, Quaternion(0.5, -0.5, -0.5, 0.5), Quaternion(0, -2, 3, -1))

    def assert_rotation(self, vector: Quaternion, rotation: Quaternion, expected: Quaternion):
        step1 = rotation @ vector
        _r = Quaternion(rotation.w, -rotation.i, -rotation.j, -rotation.k)
        result = step1 @ _r
        self.assertEqual(result, expected)

    def test_negate_unit_quaternion(self):
        q = Quaternion(0.5, 0.5, 0.5, 0.5)
        recip = -q
        self.assertEqual(Quaternion(1, 0, 0, 0), q@recip)

    def test_negate_quaternion(self):
        q = Quaternion(2, 1, 1, 1)
        mag = q.magnitude()
        self.assertEqual(Quaternion(2/mag, -1/mag, -1/mag, -1/mag), -q)

    # Note that these rotations are a good way to test an attitude
    # filter such as Madgwick. Pose the pi and check that the output
    # quaternion is as expected. Note that the negative quaternion
    # is identical. i.e.g Q(h, 0, 0, h) == Q(-h, 0, 0, -h)
    def test_rotate(self):
        vector = Vector([3, 2, 1])
        h = math.sqrt(0.5)
        self.assertEqual(vector, Quaternion(-1, 0, 0, 0).rotate(vector))
        # Roll
        # Roll clockwise 90 around x
        self.assertEqual(Vector([3, -1, 2]), Quaternion(h, h, 0, 0).rotate(vector))
        # Roll anti-clockwise 90 around x
        self.assertEqual(Vector([3, 1, -2]), Quaternion(h, -h, 0, 0).rotate(vector))
        # Roll 180 around x
        self.assertEqual(Vector([3, -2, -1]), Quaternion(0, 1, 0, 0).rotate(vector))
        # Pitch
        # Pitch clockwise 90 around y
        self.assertEqual(Vector([1, 2, -3]), Quaternion(h, 0, h, 0).rotate(vector))
        # Pitch anti-clockwise 90 around y
        self.assertEqual(Vector([-1, 2, 3]), Quaternion(h, 0, -h, 0).rotate(vector))
        # Pitch 180 around y
        self.assertEqual(Vector([-3, 2, -1]), Quaternion(0, 0, 1, 0).rotate(vector))
        # Yaw
        # Yaw clockwise 90 around z
        self.assertEqual(Vector([-2, 3, 1]), Quaternion(h, 0, 0, h).rotate(vector))
        # Yaw anti-clockwise 90 around z
        self.assertEqual(Vector([2, -3, 1]), Quaternion(h, 0, 0, -h).rotate(vector))
        # Yaw 180 degrees
        self.assertEqual(Vector([-3, -2, 1]), Quaternion(0, 0, 0, -1).rotate(vector))
        # Mixed
        # Yaw 270 degrees clockwise, pitch up 90 degrees
        self.assertEqual(Vector([2, -1, -3]), Quaternion(0.5, 0.5, 0.5, -0.5).rotate(vector))

    def test_from_tait_bryan_angles(self):
        angles = Vector([-17.713189297728253, 39.565186250908496, -85.72963126025222])
        expected = Quaternion(0.716928656601421, 0.12130574419231988, 0.34366893987004193, -0.5942978020641088)
        self.assertEqual(expected, Quaternion.from_tait_bryan(angles))

    def test_from_tait_bryan_angles_radians(self):
        angles_in_radians = Vector([-0.3091535, 0.6905428, -1.4962643])
        expected = Quaternion(0.716928656601421, 0.12130574419231988, 0.34366893987004193, -0.5942978020641088)
        self.assertEqual(expected, Quaternion.from_tait_bryan_radians(angles_in_radians))

    def test_to_tait_bryan(self):
        q = Quaternion(0.716928656601421, 0.12130574419231988, 0.34366893987004193, -0.5942978020641088)
        expected = Vector([-17.713189297728253, 39.565186250908496, -85.72963126025222])
        self.assertEqual(expected, q.to_tait_bryan())

    def test_to_tait_bryan_radians(self):
        q = Quaternion(0.716928656601421, 0.12130574419231988, 0.34366893987004193, -0.5942978020641088)
        expected = Vector([-0.3091535, 0.6905428, -1.4962643])
        self.assertEqual(expected, q.to_tait_bryan_radians())

    def test_round_trip_tait_bryan_angles(self):
        angles = Vector([-17.713189297728253, 39.565186250908496, -85.72963126025222])
        q = Quaternion.from_tait_bryan(angles)
        self.assertEqual(angles, q.to_tait_bryan())

    def test_round_trip_tait_bryan_radians_angles(self):
        angles = Vector([0.5, 0.3, -1.1])
        q = Quaternion.from_tait_bryan_radians(angles)
        self.assertEqual(angles, q.to_tait_bryan_radians())

    def test_round_trip_proper_zxz_euler_angles(self):
        v = Vector([-17.713189297728253, 39.565186250908496, -85.72963126025222])
        q = Quaternion.from_euler(v)
        self.assertEqual(v, Quaternion.to_euler(q))


if __name__ == '__main__':
    unittest.main()
