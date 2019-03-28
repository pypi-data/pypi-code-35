import numpy as np
from navipy.maths import tools
import unittest


class TestTools(unittest.TestCase):
    def test_vectornorm(self):
        a = tools.vector_norm([2, 3.0, 8.0, 5])
        self.assertTrue(np.allclose(a, [ 10.099504]))

    def test_inversematrix(self):
        a = tools.inverse_matrix([[1, 2], [3, 4]])
        self.assertTrue(np.allclose(a, [[-2. ,  1. ],[ 1.5, -0.5]]))

    def test_concatenate_matrices(self):
        a = tools.concatenate_matrices([[1,2, 4], [3.0,4, 7], [5, 6, 4], [7, 8, 2.0]])
        self.assertTrue(np.allclose(a, [[ 1.,  2.,  4.],
                                        [ 3.,  4.,  7.],
                                        [ 5.,  6.,  4.],
                                        [ 7.,  8.,  2.]]))

    def test_angle_between_vectors(self):
        vector_0 = np.array([1.20, 2.4, 5.0])
        vector_1 = np.array([5, 6, 8.0])
        val = tools.angle_between_vectors(vector_0, vector_1)
        self.assertTrue(np.allclose(val, 0.31096949112250771))


if __name__ == '__main__':
    unittest.main()