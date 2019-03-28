from navipy.sensors.renderer import BlenderRender
from navipy.maths.euler import matrix, from_matrix
from navipy.maths.quaternion import from_matrix as from_quat_matrix
import pandas as pd
import numpy as np
import unittest


class TestBlenderRender_renderer(unittest.TestCase):
    def setUp(self):
        """
        Prepare for the test
        """
        self.conventions = ['xyz', 'xzy', 'yzx', 'yxz', 'zxy', 'zyx']
        self.renderer = BlenderRender()

    def test_diff_euler_2_euler(self):
        """
        Test if images rendered from two different conventions match \
        one another
        """
        for convention in self.conventions:
            index = pd.MultiIndex.from_tuples(
                [('location', 'x'), ('location', 'y'),
                 ('location', 'z'), (convention, 'alpha_0'),
                 (convention, 'alpha_1'), (convention, 'alpha_2')])
            posorient = pd.Series(index=index)
            posorient.loc['location']['x'] = 0
            posorient.loc['location']['y'] = 0
            posorient.loc['location']['z'] = 1
            posorient.loc[convention]['alpha_0'] = np.pi/4
            posorient.loc[convention]['alpha_1'] = np.pi/7
            posorient.loc[convention]['alpha_2'] = np.pi/3

            a, b, c = posorient.loc[convention]
            matorient = matrix(a, b, c, axes=convention)

            image_ref = self.renderer.scene(posorient)

            for convention2 in self.conventions:
                index2 = pd.MultiIndex.from_tuples(
                    [('location', 'x'), ('location', 'y'),
                     ('location', 'z'), (convention2, 'alpha_0'),
                     (convention2, 'alpha_1'), (convention2, 'alpha_2')])
                posorient2 = pd.Series(index=index2)
                posorient2.loc['location'][:] = posorient.loc['location'][:]
                # An orientation matrix need to be calculated from
                # the euler angle of the convention of 'reference'
                # so that it can be decompase in another convention
                at, bt, ct = from_matrix(matorient, axes=convention2)
                posorient2.loc[convention2] = [at, bt, ct]
                image2 = self.renderer.scene(posorient2)
                np.testing.assert_allclose(image2, image_ref)

    def test_euler_2_quaternion(self):
        convention2 = 'quaternion'
        index2 = pd.MultiIndex.from_tuples(
            [('location', 'x'), ('location', 'y'),
             ('location', 'z'), (convention2, 'q_0'),
             (convention2, 'q_1'), (convention2, 'q_2'), (convention2, 'q_3')],
            names=['position', 'orientation'])
        posorient2 = pd.Series(index=index2)

        for convention in self.conventions:
            index = pd.MultiIndex.from_tuples(
                [('location', 'x'), ('location', 'y'),
                 ('location', 'z'), (convention, 'alpha_0'),
                 (convention, 'alpha_1'), (convention, 'alpha_2')])
            posorient = pd.Series(index=index)
            posorient.loc['location']['x'] = 0
            posorient.loc['location']['y'] = 0
            posorient.loc['location']['z'] = 1
            posorient.loc[convention]['alpha_0'] = np.pi/4
            posorient.loc[convention]['alpha_1'] = np.pi/7
            posorient.loc[convention]['alpha_2'] = np.pi/3

            a, b, c = posorient.loc[convention]
            matorient = matrix(a, b, c, axes=convention)

            image_ref = self.renderer.scene(posorient)

            posorient2.loc['location'][:] = posorient.loc['location'][:]
            # An orientation matrix need to be calculated from
            # the euler angle of the convention of 'reference'
            # so that it can be decompase in another convention
            at, bt, ct, dt = from_quat_matrix(matorient)
            posorient2.loc[convention2] = [at, bt, ct, dt]
            image2 = self.renderer.scene(posorient2)
            np.testing.assert_allclose(image2, image_ref, atol=1.2)
    """
    def test_quaternion_2_euler(self):
        convention = 'quaternion'
        index = pd.MultiIndex.from_tuples(
            [('location', 'x'), ('location', 'y'),
             ('location', 'z'), (convention, 'q_0'),
             (convention, 'q_1'), (convention, 'q_2'), (convention, 'q_3')],
            names=['position', 'orientation'])
        posorient = pd.Series(index=index)
        posorient = pd.Series(index=index)
        posorient.loc['location']['x'] = 0
        posorient.loc['location']['y'] = 0
        posorient.loc['location']['z'] = 1
        posorient.loc[convention]['q_0'] = np.pi/4
        posorient.loc[convention]['q_1'] = np.pi/7
        posorient.loc[convention]['q_2'] = np.pi/3
        posorient.loc[convention]['q_3'] = np.pi/2

        a, b, c, d = posorient.loc[convention]
        matorient = quat_matrix([a, b, c, d])

        image_ref = self.renderer.scene(posorient)

        for convention2 in conventions:
            index2 = pd.MultiIndex.from_tuples(
                [('location', 'x'), ('location', 'y'),
                 ('location', 'z'), (convention, 'alpha_0'),
                 (convention, 'alpha_1'), (convention, 'alpha_2')])
            posorient2.loc['location'][:] = posorient.loc['location'][:]


            at, bt, ct = from_quat_matrix(matorient, convention2)
            posorient2.loc['location'][:] = posorient.loc['location'][:]
            # An orientation matrix need to be calculated from
            # the euler angle of the convention of 'reference'
            # so that it can be decompase in another convention
            at, bt, ct, dt = from_quat_matrix(matorient)
            posorient2.loc[convention2] = [at, bt, ct]
            image2 = self.renderer.scene(posorient2)
            np.testing.assert_allclose(image2, self.image_ref, atol=1.2)
    """
