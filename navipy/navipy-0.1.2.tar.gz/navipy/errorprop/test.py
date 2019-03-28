import unittest
import numpy as np
from navipy.errorprop import propagate_error, estimate_jacobian


def sincosine(x):
    return np.cos(x[0]+x[1]), np.sin(x[0]-x[1])


class TestErrorProp(unittest.TestCase):

    def test_cosine(self):
        fun = np.cos
        x = 2*(np.random.rand()-0.5)*np.pi
        covar = 2*(np.random.rand()-0.5)*np.pi / 10
        err = propagate_error(fun, x, covar)
        err_theo = np.abs(-np.sin(x))*covar
        self.assertAlmostEqual(err, err_theo)

    def test_sincosine(self):
        fun = sincosine
        x = 2*(np.random.rand(2)-0.5)*np.pi
        covar = 2*(np.random.rand(2, 2)-0.5)*np.pi / 10
        # Test jacobian
        jacobian_matrix = estimate_jacobian(fun, x)
        jacobian_matrix_theo = [[-np.sin(x[0]+x[1]), -np.sin(x[0]+x[1])],
                                [np.cos(x[0]-x[1]), -np.cos(x[0]-x[1])]]
        jacobian_matrix_theo = np.array(jacobian_matrix_theo)
        np.testing.assert_array_almost_equal(
            jacobian_matrix, jacobian_matrix_theo)

        # Test prop error
        err = propagate_error(fun, x, covar)
        s = np.sin(x[0]+x[1])
        c = np.cos(x[0]-x[1])
        d = covar[0, 0]
        e = covar[0, 1]
        f = covar[1, 0]
        g = covar[1, 1]
        err_theo = np.zeros((2, 2))
        err_theo[0, 0] = -s*(-d*s - f*s) - s*(-g*s - e*s)
        err_theo[0, 1] = c*(-d*s - f*s) - c*(-g*s - e*s)
        err_theo[1, 0] = -s*(c*d - c*f) - s*(c*e - c*g)
        err_theo[1, 1] = c*(c*d - c*f) - c*(c*e - c*g)
        np.testing.assert_array_almost_equal(err, err_theo)


if __name__ == '__main__':
    unittest.main()
