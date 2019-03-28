import unittest
import numpy as np
from navipy.maths import random
from navipy.maths.tools import vector_norm


class TestRandom(unittest.TestCase):
    def test__rotation_matrix(self):
        rotation = random.rotation_matrix()
        self.assertTrue(np.allclose(np.dot(rotation.T, rotation),
                                    np.identity(4)))

    def test_random_quaternion(self):
        quaternion = random.quaternion()
        self.assertTrue(np.allclose(1, vector_norm(quaternion)))

        with self.assertRaises(Exception):
           quaternion2 = np.random.rand(4)
           random.quaternion(quaternion2)


if __name__ == '__main__':
    unittest.main()
