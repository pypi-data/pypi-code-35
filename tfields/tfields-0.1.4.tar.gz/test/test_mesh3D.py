import tfields
import numpy as np
import unittest
import sympy  # NOQA: F401
import os
import sys
THIS_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(THIS_DIR)))
from test_core import Base_Check


class Sphere_Test(Base_Check, unittest.TestCase):
    def setUp(self):
        self._inst = tfields.Mesh3D.grid(
                (1, 1, 1),
                (-np.pi, np.pi, 12),
                (-np.pi / 2, np.pi / 2, 12),
                coord_sys='spherical')
        self._inst.transform('cartesian')
        self._inst[:, 1] += 2

    def test_cut_split(self):
        x, y, z = sympy.symbols('x y z')
        halfed = self._inst.cut(x + 1./100*y > 0, at_intersection='split')

if __name__ == '__main__':
    unittest.main()
