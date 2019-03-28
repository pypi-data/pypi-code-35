import unittest
import numpy as np
import pandas as pd
from navipy.maths import constants as htconst
from navipy.trajectories import Trajectory


class TestTrajectoryTransform(unittest.TestCase):
    def test_forwardreverse(self):
        # Build an equilateral triangle
        markers = pd.Series(data=0,
                            index=pd.MultiIndex.from_product([
                                [0, 1, 2],
                                ['x', 'y', 'z']]))
        markers.loc[(0, 'x')] = -1
        markers.loc[(2, 'y')] = np.sin(np.pi / 3)
        markers.loc[(1, 'y')] = -np.sin(np.pi / 3)
        markers.loc[(1, 'x')] = np.cos(np.pi / 3)
        markers.loc[(2, 'x')] = np.cos(np.pi / 3)
        markers.index.name = None
        # Create a random trajectory
        trajectory = Trajectory(indeces=np.arange(10),
                                rotconv='xyz')
        trajectory.x = 100 * (np.random.rand(trajectory.shape[0]) - 0.5)
        trajectory.y = 100 * (np.random.rand(trajectory.shape[0]) - 0.5)
        trajectory.z = 100 * (np.random.rand(trajectory.shape[0]) - 0.5)
        trajectory.alpha_0 = 2 * np.pi * \
            (np.random.rand(trajectory.shape[0]) - 0.5)
        trajectory.alpha_1 = 2 * np.pi * \
            (np.random.rand(trajectory.shape[0]) - 0.5)
        trajectory.alpha_2 = 2 * np.pi * \
            (np.random.rand(trajectory.shape[0]) - 0.5)
        # Create test trajectory
        traj_test = Trajectory(indeces=np.arange(10),
                               rotconv='xyz')
        # Devide by two the second anle, because of gimbal lock
        col = (trajectory.rotation_mode, 'alpha_1')
        trajectory.loc[:, col] = trajectory.loc[:, col] / 2
        # forward
        for euler_axes in list(htconst._AXES2TUPLE.keys()):
            trajectory.rotation_mode = euler_axes
            traj_test.rotation_mode = euler_axes
            transformed_markers = trajectory.body2world(markers)
            # reverse
            for triangle_mode in ['x-axis=median-from-0',
                                  'y-axis=1-2']:
                traj_test.from_markers(transformed_markers,
                                       triangle_mode)
                np.testing.assert_array_almost_equal(
                    trajectory.astype(float),
                    traj_test.astype(float))

    def test_velocity(self):
        pass

    def test_traveldist(self):
        indeces = np.linspace(0, 2*np.pi, 2000)
        radius = 5
        mytraj = Trajectory(indeces=indeces, rotconv='zyx')
        mytraj.x = radius*np.cos(indeces)
        mytraj.y = radius*np.sin(indeces)
        mytraj.z = 0
        # The length of function above
        # is equal to perimeter of the circle
        # 2*pi*r
        travel_dist_theo = 2*np.pi*radius
        travel_dist = mytraj.traveled_distance()
        np.testing.assert_almost_equal(
            travel_dist, travel_dist_theo, decimal=4)
        # Test with nans
        mytraj.iloc[[15, 50, 90], :] = np.nan
        travel_dist = mytraj.traveled_distance()
        np.testing.assert_almost_equal(
            travel_dist, travel_dist_theo, decimal=4)

    def test_sinuosity(self):
        indeces = np.linspace(0, np.pi, 1000)
        radius = 5
        mytraj = Trajectory(indeces=indeces, rotconv='zyx')
        mytraj.x = radius*np.cos(indeces)
        mytraj.y = radius*np.sin(indeces)
        mytraj.z = 0
        # The length  of function above
        # is equal to half the perimeter of the circle
        # pi*r
        # the sinuosity will be equal to:
        sinuosity_theo = np.pi*radius/(2*radius)
        sinuosity = mytraj.sinuosity()
        np.testing.assert_almost_equal(sinuosity, sinuosity_theo, decimal=4)


if __name__ == '__main__':
    unittest.main()
