import numpy as np
from navipy.maths import coordinates
import unittest
from navipy.maths.coordinates import cartesian_to_spherical
from navipy.maths.coordinates import cartesian_to_spherical_vectors


class TestCoordinates(unittest.TestCase):

    def test_cartesian_to_spherical(self):
        elevation,azimuth, rad = coordinates.cartesian_to_spherical(2,3, 4)
        self.assertEqual(elevation,0.83721500315481356)
        self.assertEqual(azimuth,0.98279372324732905)
        self.assertEqual(rad, 5.3851648071345037)

    def test_cartesian_to_spherical_vectors(self):
        for a, b in [(None, 2), (3, None)]:
            with self.assertRaises(ValueError):
                coordinates.cartesian_to_spherical_vectors(a,b)


        for c,d in [((3.0,2),([5, 6.0])),(([4.0, 2]),(4, 3))]:
            with self.assertRaises(TypeError):
                coordinates.cartesian_to_spherical_vectors(c, d)

        for g,h in [((3.0,2, 4),(1.0, 5, 6.0)),((4.0,4,  2),(4, 5.0, 3))]:
            with self.assertRaises(TypeError):
                coordinates.cartesian_to_spherical_vectors(g,h)

            with self.assertRaises(Exception):
                coordinates.cartesian_to_spherical_vectors(g, h)



        with self.assertRaises(Exception):
            e = np.array([2, 4, 6, 8])
            f = np.array([2, 4, 6, 8, 3.0])
            coordinates.cartesian_to_spherical_vectors(e, f)

        with self.assertRaises(TypeError):
            a = np.array([None, 4, 'w'])
            b = np.array([2.0, None, 'w'])
            coordinates.cartesian_to_spherical_vectors(a, b)


if __name__ == '__main__':
    unittest.main()
