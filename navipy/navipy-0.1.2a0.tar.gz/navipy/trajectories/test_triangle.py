"""
"""
import unittest
import numpy as np
import pandas as pd
from navipy.trajectories.triangle import Triangle


class TestTriangle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.apex0 = pd.Series(data=np.random.rand(3),
                              index=['x', 'y', 'z'],
                              dtype=float)
        cls.apex1 = pd.Series(data=np.random.rand(3),
                              index=['x', 'y', 'z'],
                              dtype=float)
        cls.apex2 = pd.Series(data=np.random.rand(3),
                              index=['x', 'y', 'z'],
                              dtype=float)

    def test_init_notpandas_first(self):

        with self.assertRaises(TypeError):
            Triangle(np.random.rand(3), self.apex1, self.apex2)

    def test_init_notpandas_second(self):
        with self.assertRaises(TypeError):
            Triangle(self.apex0, np.random.rand(3), self.apex2)

    def test_init_notarray_third(self):
        with self.assertRaises(TypeError):
            Triangle(self.apex0, self.apex1, np.random.rand(3))

    def test_init_not3el_first(self):
        apex_false = pd.Series(index=['x', 'y'])
        with self.assertRaises(IOError):
            Triangle(apex_false, self.apex1, self.apex2)

    def test_init_not3el_second(self):
        apex_false = pd.Series(index=['x', 'y'])
        with self.assertRaises(IOError):
            Triangle(self.apex0, apex_false, self.apex2)

    def test_init_not3el_third(self):
        apex_false = pd.Series(index=['x', 'y'])
        with self.assertRaises(IOError):
            Triangle(self.apex0, self.apex1, apex_false)

    def test_init_notfloat_first(self):
        apex_false = pd.Series(index=['x', 'y', 'z'],
                               dtype=object)
        with self.assertRaises(IOError):
            Triangle(apex_false, self.apex1, self.apex2)

    def test_init_notfloat_second(self):
        apex_false = pd.Series(index=['x', 'y', 'z'],
                               dtype=object)
        with self.assertRaises(IOError):
            Triangle(self.apex0, apex_false, self.apex2)

    def test_init_notfloat_third(self):
        apex_false = pd.Series(index=['x', 'y', 'z'],
                               dtype=object)
        with self.assertRaises(IOError):
            Triangle(self.apex0, self.apex1, apex_false)

    def test_init(self):
        triangle = Triangle(self.apex0, self.apex1, self.apex2)
        condition = np.allclose(triangle.apexes.apex0, self.apex0)
        condition &= np.allclose(triangle.apexes.apex1, self.apex1)
        condition &= np.allclose(triangle.apexes.apex2, self.apex2)
        self.assertTrue(condition)

    def test_center_of_mass(self):
        triangle = Triangle(self.apex0, self.apex1, self.apex2)
        cm = triangle.center_of_mass()
        cm_test = (self.apex0 + self.apex1 + self.apex2) / 3
        np.testing.assert_allclose(cm, cm_test)

    def test_apexes2vectors(self):
        """The vectors are from one apex to the other in a directed \
manner. apex0 -> apex1 -> apex2. So the sum of all vector \
should be zero
        """
        triangle = Triangle(self.apex0, self.apex1, self.apex2)
        vec = triangle.apexes2vectors()
        np.testing.assert_allclose(vec.sum(axis=1).values, [0, 0, 0])

    def test_apexes2edges_norm(self):
        triangle = Triangle(self.apex0, self.apex1, self.apex2)
        en = triangle.apexes2edges_norm()
        test_norm = np.sqrt(np.sum((self.apex0 - self.apex1)**2))
        self.assertAlmostEqual(en.loc[(0, 1)], test_norm)

    def test_medians(self):
        """The median intersect should be at the middle of an edge
        """
        triangle = Triangle(self.apex0, self.apex1, self.apex2)
        md = triangle.medians()
        test_apex1 = np.sqrt(np.sum((md.loc[:, 0] - self.apex1)**2))
        test_apex2 = np.sqrt(np.sum((md.loc[:, 0] - self.apex2)**2))
        self.assertAlmostEqual(test_apex1, test_apex2)


if __name__ == '__main__':
    unittest.main()
