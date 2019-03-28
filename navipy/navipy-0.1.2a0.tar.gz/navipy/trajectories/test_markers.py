import unittest
import numpy as np
import pandas as pd
from navipy.maths.homogeneous_transformations import compose_matrix
from navipy.trajectories import transformations as mtf
from navipy.trajectories.triangle import Triangle


class TestMarkersTransform(unittest.TestCase):
    def setUp(self):
        # Build an equilateral triangle
        self.markers = pd.Series(data=0,
                                 index=pd.MultiIndex.from_product(
                                     [[0, 1, 2], ['x', 'y', 'z']]))
        self.markers.loc[(0, 'x')] = -1
        self.markers.loc[(2, 'y')] = np.sin(np.pi / 3)
        self.markers.loc[(1, 'y')] = -np.sin(np.pi / 3)
        self.markers.loc[(1, 'x')] = np.cos(np.pi / 3)
        self.markers.loc[(2, 'x')] = np.cos(np.pi / 3)
        self.equilateral = Triangle(self.markers.loc[0],
                                    self.markers.loc[1],
                                    self.markers.loc[2])

    def random_apex(self):
        return pd.Series(data=np.random.rand(3),
                         index=['x', 'y', 'z'])

    def test_normalise_vec(self):
        vec = np.random.rand(10)
        vec = mtf.normalise_vec(vec)
        self.assertAlmostEqual(np.linalg.norm(vec), 1)

    def test_triangle2bodyaxis(self):
        for cmode in ['x-axis=median-from-0',
                      'y-axis=1-2']:
            origin, x_axis, y_axis, z_axis = \
                mtf.triangle2bodyaxis(self.equilateral,
                                      mode=cmode)
            np.testing.assert_allclose(origin, [0, 0, 0],
                                       atol=1e-07,
                                       err_msg='origin&mode ' + cmode)
            np.testing.assert_allclose(x_axis, [1, 0, 0],
                                       atol=1e-07,
                                       err_msg='x-axis&mode ' + cmode)
            np.testing.assert_allclose(y_axis, [0, 1, 0],
                                       atol=1e-07,
                                       err_msg='y-axis&mode ' + cmode)
            np.testing.assert_allclose(z_axis, [0, 0, 1],
                                       atol=1e-07,
                                       err_msg='z-axis&mode ' + cmode)

    def test_triangle2bodyaxis_wrongmode(self):
        """Certain mode are not supported"""
        apex0 = self.random_apex()
        apex1 = self.random_apex()
        apex2 = self.random_apex()
        triangle = Triangle(apex0, apex1, apex2)
        mode = 'Thisisafakemodeandshouldfail'
        with self.assertRaises(KeyError):
            mtf.triangle2bodyaxis(triangle, mode)

    def test_triangle2bodyaxis_cross(self):
        """The cross product of x-axis and y-axis should \
        be the same than the z-axis"""
        apex0 = self.random_apex()
        apex1 = self.random_apex()
        apex2 = self.random_apex()
        triangle = Triangle(apex0, apex1, apex2)
        for mode in mtf._modes:
            _, x_axis, y_axis, z_axis = \
                mtf.triangle2bodyaxis(triangle, mode)
            np.testing.assert_almost_equal(np.cross(x_axis, y_axis), z_axis)

    def test_triangle2bodyaxis_ortho(self):
        """Determinant of frame should be 1, it is a rotation matrix"""
        apex0 = self.random_apex()
        apex1 = self.random_apex()
        apex2 = self.random_apex()
        triangle = Triangle(apex0, apex1, apex2)
        for mode in mtf._modes:
            _, x_axis, y_axis, z_axis = \
                mtf.triangle2bodyaxis(triangle, mode)
            frame = mtf.bodyaxistransformations(
                x_axis, y_axis, z_axis)
            np.testing.assert_almost_equal(np.linalg.det(frame), 1)

    def test_markers2decompose(self):
        apex0 = self.random_apex()
        apex1 = self.random_apex()
        apex2 = self.random_apex()
        euler_axes = 'xyz'
        for triangle_mode in mtf._modes:
            scale, shear, angles, translate, perspective =\
                mtf.markers2decompose(
                    apex0, apex1, apex2, triangle_mode, euler_axes)
            np.testing.assert_almost_equal(scale, [1, 1, 1])
            np.testing.assert_almost_equal(shear, [0, 0, 0])
            np.testing.assert_almost_equal(perspective, [0, 0, 0, 1])

    def test_twomarker2euler(self):
        mark0 = pd.Series(data=0, index=['x', 'y', 'z'])
        for axis_alignement, euler_axes in zip(['x-axis', 'z-axis', 'y-axis'],
                                               ['zyx', 'yxz', 'zxy']):
            angles = np.pi * (np.random.rand(3) - 0.5)
            angles[0] *= 2
            angles[2] *= 2
            index = euler_axes.find(axis_alignement[0])
            if index < 0:
                continue
            known_angle = angles[index].copy()

            triangle_mode = 'x-axis=median-from-0'
            transform = compose_matrix(angles=angles,
                                       axes=euler_axes)
            equilateral = Triangle(self.markers.loc[0],
                                   self.markers.loc[1],
                                   self.markers.loc[2])
            equilateral.transform(transform)
            origin, x_axis, y_axis, z_axis = mtf.triangle2bodyaxis(
                equilateral, triangle_mode)
            if axis_alignement == 'x-axis':
                mark1 = pd.Series(x_axis, index=['x', 'y', 'z'])
            elif axis_alignement == 'y-axis':
                mark1 = pd.Series(y_axis, index=['x', 'y', 'z'])
            elif axis_alignement == 'z-axis':
                mark1 = pd.Series(z_axis, index=['x', 'y', 'z'])
            angles_estimate = mtf.twomarkers2euler(
                mark0, mark1, axis_alignement, known_angle, euler_axes)
            np.testing.assert_allclose(
                angles, angles_estimate, rtol=1e-02, atol=1e-02)


if __name__ == '__main__':
    unittest.main()
