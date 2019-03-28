from navipy.sensors.renderer import BlenderRender
from navipy.maths.euler import matrix, from_matrix
from navipy.maths.quaternion import from_matrix as quat_matrix
import pandas as pd
import numpy as np
import unittest
import pkg_resources
import tempfile
from navipy.database import DataBase


class TestBlenderRender_renderer(unittest.TestCase):
    def setUp(self):
        """
        Prepare for the test
        """
        convention = 'xyz'
        index = pd.MultiIndex.from_tuples(
            [('location', 'x'), ('location', 'y'),
             ('location', 'z'), (convention, 'alpha_0'),
             (convention, 'alpha_1'), (convention, 'alpha_2')])
        self.posorient = pd.Series(index=index)
        self.posorient.loc['location']['x'] = 0
        self.posorient.loc['location']['y'] = 0
        self.posorient.loc['location']['z'] = 1
        self.posorient.loc[convention]['alpha_0'] = np.pi / 4
        self.posorient.loc[convention]['alpha_1'] = np.pi / 7
        self.posorient.loc[convention]['alpha_2'] = np.pi / 3

        convention = self.posorient.index.get_level_values(0)[-1]
        a, b, c = self.posorient.loc[convention]
        self.matorient = matrix(a, b, c, axes=convention)

        self.renderer = BlenderRender()
        self.image_ref = self.renderer.scene(self.posorient)

    def test_diff_euler_xyz2yzx(self):
        """
        Test if images rendered from two different conventions match \
        one another
        """
        convention = 'yzx'
        index = pd.MultiIndex.from_tuples(
            [('location', 'x'), ('location', 'y'),
             ('location', 'z'), (convention, 'alpha_0'),
             (convention, 'alpha_1'), (convention, 'alpha_2')])
        posorient2 = pd.Series(index=index)
        posorient2.loc['location'][:] = self.posorient.loc['location'][:]
        # An orientation matrix need to be calculated from
        # the euler angle of the convention of 'reference'
        # so that it can be decompase in another convention
        at, bt, ct = from_matrix(self.matorient, axes=convention)
        posorient2.loc[convention] = [at, bt, ct]
        image2 = self.renderer.scene(posorient2)
        np.testing.assert_allclose(image2, self.image_ref)

    def test_euler_xyz_2_quaternion(self):
        convention = 'quaternion'
        index = pd.MultiIndex.from_tuples(
            [('location', 'x'), ('location', 'y'),
             ('location', 'z'), (convention, 'q_0'),
             (convention, 'q_1'), (convention, 'q_2'), (convention, 'q_3')],
            names=['position', 'orientation'])
        posorient2 = pd.Series(index=index)
        posorient2.loc['location'][:] = self.posorient.loc['location'][:]
        # An orientation matrix need to be calculated from
        # the euler angle of the convention of 'reference'
        # so that it can be decompase in another convention
        at, bt, ct, dt = quat_matrix(self.matorient)
        posorient2.loc[convention] = [at, bt, ct, dt]
        image2 = self.renderer.scene(posorient2)
        np.testing.assert_allclose(image2, self.image_ref, atol=1.2)

    def test_gridrender(self):
        """
        Test the rendering on 5x5 grid
        """
        x = np.linspace(-0.5, 0.5, 5)
        y = np.linspace(-0.5, 0.5, 5)
        z = [3]
        alpha_0 = [0]
        rotconv = 'zyx'
        db_reffilename = pkg_resources.resource_filename(
            'navipy', 'resources/database.db')
        db_ref = DataBase(db_reffilename, mode='r')
        tfile = tempfile.NamedTemporaryFile()
        outputfile = tfile.name+'.db'
        self.renderer.render_ongrid(outputfile,
                                    x, y, z, alpha_0,
                                    rotconv=rotconv)
        db = DataBase(outputfile, mode='r')
        posorients = db_ref.posorients
        for row_i, posorient in posorients.iterrows():
            refscene = db_ref.scene(posorient)
            try:
                scene = db.scene(posorient)
            except ValueError:
                msg = 'Scene has not been found {}'.format(db.posorients)
                msg += '\n{}'.format(posorient)
                self.assertEqual(False, True, msg)
            np.testing.assert_allclose(scene, refscene, atol=1)
