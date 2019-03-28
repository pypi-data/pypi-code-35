import unittest
from navipy.processing import mcode
import pandas as pd
import numpy as np
from navipy.trajectories import posorient_columns
from navipy.trajectories import velocities_columns
from navipy.scene import __spherical_indeces__


class OpticFlowTest(unittest.TestCase):
    """
    Test the geometrical computation of the optic flow
    """

    def setUp(self):
        """ Init vectors
        """
        convention = 'zyx'
        tuples_posvel = posorient_columns(convention)
        tuples_posvel.extend(velocities_columns(convention))
        index_posvel = pd.MultiIndex.from_tuples(tuples_posvel,
                                                 names=['position',
                                                        'orientation'])
        velocity = pd.Series(index=index_posvel, data=0)
        # Most test are independent of orientation and position
        velocity.loc[(convention, 'alpha_0')] = 2 * \
            np.pi * (np.random.rand() - 0.5)
        velocity.loc[(convention, 'alpha_1')] = np.pi * \
            (np.random.rand() - 0.5)
        velocity.loc[(convention, 'alpha_2')] = 2 * \
            np.pi * (np.random.rand() - 0.5)
        velocity.loc[('location', 'x')] = np.random.randn()
        velocity.loc[('location', 'y')] = np.random.randn()
        velocity.loc[('location', 'z')] = np.random.randn()
        self.velocity = velocity
        self.convention = convention

        # Init the viewing directions
        elevation = np.linspace(-np.pi / 2, np.pi / 2, 5)
        azimuth = np.linspace(-np.pi, np.pi, 11)
        [ma, me] = np.meshgrid(azimuth, elevation)
        imshape = me.shape
        viewing_directions = np.zeros((ma.shape[0], ma.shape[1], 2))
        viewing_directions[..., __spherical_indeces__['elevation']] = me
        viewing_directions[..., __spherical_indeces__['azimuth']] = ma
        self.viewing_directions = viewing_directions
        self.elevation = elevation
        self.azimuth = azimuth

        # Init a random scene
        scene = np.random.rand(imshape[0], imshape[1])
        self.scene = scene

    def test_distance(self):
        """
        The magnitude of the optic flow when the agent is moving \
close to object is larger than when it is moving (with the same velocity)\
far from them.
        Here we test this property.
        """
        vel = self.velocity.copy()
        # This is true for any translational motion
        vel.loc[('location', 'dx')] = np.random.randn()
        vel.loc[('location', 'dy')] = np.random.randn()
        vel.loc[('location', 'dz')] = np.random.randn()
        #
        rof, hof, vof =\
            mcode.optic_flow(self.scene,
                             self.viewing_directions,
                             vel)
        hnorm = np.sqrt(hof**2 + vof ** 2)
        # Add abs tol because we compare to zero
        np.testing.assert_allclose(rof, np.zeros_like(rof), atol=1e-7)
        # Calculate second optic flow, with objects further away form agent
        rof_further, hof_further, vof_further =\
            mcode.optic_flow(self.scene + 1,
                             self.viewing_directions,
                             vel)
        hnorm_further = np.sqrt(hof_further**2 + vof_further**2)
        # Add abs tol because we compare to zero
        np.testing.assert_allclose(rof_further,
                                   np.zeros_like(rof_further), atol=1e-7)
        # The translational optic flow norm should be small
        # i.e. for norm equal to zero
        valid = (hnorm != 0) & (hnorm_further != 0)
        np.testing.assert_array_less(hnorm_further[valid], hnorm[valid])

    def test_xyplane_only(self):
        """
        When the agent is moving along in the plane x,y, the gOF
along the vertical gOF is ull at null elevation
        """
        vel = self.velocity.copy()
        # This is true for any x-y translational motion
        vel.loc[('location', 'dx')] = np.random.randn()
        vel.loc[('location', 'dy')] = np.random.randn()
        vel.loc[('location', 'dz')] = 0
        # but in the coordinate of the bee
        # by setting euler angles to zero, the axis of the
        # bee coordinate system and the world one match
        vel.loc[(self.convention, 'alpha_0')] = 0
        vel.loc[(self.convention, 'alpha_1')] = 0
        vel.loc[(self.convention, 'alpha_2')] = 0

        # Calculate gOF
        rof, hof, vof =\
            mcode.optic_flow(self.scene,
                             self.viewing_directions,
                             vel)
        # Add abs tol because we compare to zero
        np.testing.assert_allclose(rof, np.zeros_like(rof), atol=1e-7)
        # At null elevation only this is true
        vof_el = vof[self.elevation == 0, :]
        np.testing.assert_allclose(vof_el, np.zeros_like(vof_el), atol=1e-7)

    def test_yaw_rot(self):
        """
        The optic for a rotation around the z-axis in the \
yaw-pitch-roll (zyx) convention has vertical gOF equal to zero
        """
        vel = self.velocity.copy()
        vel.loc[(self.convention, 'dalpha_0')] = np.random.rand()
        rof, hof, vof = mcode.optic_flow(self.scene,
                                         self.viewing_directions,
                                         vel)
        # Add abs tol because we compare to zero
        np.testing.assert_allclose(rof, np.zeros_like(rof), atol=1e-7)
        np.testing.assert_allclose(vof, np.zeros_like(vof), atol=1e-7)
