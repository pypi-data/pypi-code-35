"""
Generate a trajectory

# An agent trajectory is defined by the position and orientation of \
the agent along the time t. The agent is flying in the direction of \
its orientation at a given speed

The trajectory can then be used to test:

* saccade extraction
* optic-flow calculation
* point of pivoting, ...

For practical purposes, the trajectory will stored in a pandas \
DataFrame, index by frame number (equivalent to time), and \
having for columns:

* 'x','y','z', representating the agent position
* 'alpha_0','alpha_1','alpha_2', the three euler angles
* 'facing_x','facing_x','facing_y', the facing direction of the agent

"""

from navipy.maths.euler import matrix
from scipy.stats import norm
import numpy as np
import pandas as pd
from navipy.trajectories import Trajectory


def yawpitchroll(yaw, pitch, roll):
    return matrix(yaw, pitch, roll, axes='zyx')[:3, :3]


def generate_trajectory(starting_point, speed, yaw, pitch, roll):
    """
        generate a trajectory starting from the starting_point, and \
flying at speed (plausibly changing over time),
        and rotating in the world according to yaw,pitch,roll

        starting_point is 1x3 vector
        speed is a Nx1 vector
        yaw is a Nx1 vector
        pitch is a Nx1 vector
        roll is a Nx1 vector

        here N is the number of time point
    """
    assert starting_point.shape[0] == 3, \
        'starting_point should have a size of 3'
    assert speed.shape[0] == yaw.shape[0], \
        'speed and yaw should have the same number of point'
    assert speed.shape[0] == pitch.shape[0], \
        'speed and pitch should have the same number of point'
    assert speed.shape[0] == roll.shape[0], \
        'speed and roll should have the same number of point'

    trajectory = Trajectory(indeces=np.arange(speed.shape[0]),
                            rotconv='zyx')
    trajectory.loc[0, 'location'] = starting_point
    for i in trajectory.index[1:]:
        speed_orient = np.dot(yawpitchroll(
            yaw[i - 1], pitch[i - 1], roll[i - 1]),
            np.array([[speed[i - 1]], [0], [0]]))[:, 0]
        for ii, col in enumerate(['x', 'y', 'z']):
            trajectory.loc[i, ('location', col)] = \
                trajectory.loc[i - 1, ('location', col)] \
                + speed_orient[ii]
    trajectory.alpha_0 = yaw
    trajectory.alpha_1 = pitch
    trajectory.alpha_2 = roll
    return trajectory


def generate_saccade(sac_amplitude):
    """
    return a list of angle, here the sum is the saccade amplitude

    % original cyberfly uses 8 templates derived from behavioural data.
    width of the template: linear regression on the sacc templates used
    in original cyberfly

    see Jens Lindemann 2005
    """
    # Calculate the saccade length
    sac_len = np.abs(sac_amplitude) * 28.6 + 23.4

    # create a gaussian velocity profile. sigma=0.35 fits the original
    # templates
    gw = norm.pdf(np.linspace(-1, 1, sac_len), 0, 0.35)
    # scale to the angular amplitude
    saccade_seq = (gw / np.sum(gw)) * sac_amplitude

    return saccade_seq


def saccadic_data(intersac_length_f=lambda n: 50 + np.floor(
        10 * np.random.rand(n)),
    intersac_drifty_f=lambda n: (
        3 * np.pi / 180) * (2 * (np.random.rand(n) - 0.5)),
        intersac_driftp_f=lambda n: (
        0 * np.pi / 180) * (2 * (np.random.rand(n) - 0.5)),
        intersac_driftr_f=lambda n: (
        0 * np.pi / 180) * (2 * (np.random.rand(n) - 0.5)),
        sac_y_f=lambda n: (
        np.pi / 2) * (2 * (np.random.rand(n) - 0.5)),
        sac_p_f=lambda n: (
        np.pi / 2) * (2 * (np.random.rand(n) - 0.5)),
        sac_r_f=lambda n: (
        np.pi / 2) * (2 * (np.random.rand(n) - 0.5)),
        number_sac=10):
    """
        generate a yaw pitch, roll from random saccadic input

        intersac_length_f a function of n (number of saccade), \
being the length of the intersaccade
        intersac_drifty_f a function of n, being the residual yaw-rotation
        intersac_driftp_f a function of n, being the residual pitch-rotation
        intersac_driftr_f a function of n, being the residual roll-rotation

        sac_y_f a function of n, being the yaw amplitude of the saccade
        sac_p_f a function of n, being the pitch amplitude of the saccade
        sac_r_f a function of n, being the rol amplitude of the saccade
    """
    # create data frame sumarising saccadic data
    saccade_df = pd.DataFrame(index=np.arange(number_sac),
                              columns=['intersac_length',
                                       'intersac_drifty_f',
                                       'intersac_driftp_f',
                                       'intersac_driftr_f',
                                       'sac_y_f',
                                       'sac_p_f',
                                       'sac_r_f'])
    # populate intersaccadic length
    saccade_df.intersac_length = intersac_length_f(number_sac)
    # populate intersaccadic residual rotation
    saccade_df.intersac_drifty_f = intersac_drifty_f(number_sac)
    saccade_df.intersac_driftp_f = intersac_driftp_f(number_sac)
    saccade_df.intersac_driftr_f = intersac_driftr_f(number_sac)
    # populate saccade properties
    saccade_df.sac_y_f = sac_y_f(number_sac)
    saccade_df.sac_p_f = sac_p_f(number_sac)
    saccade_df.sac_r_f = sac_r_f(number_sac)

    yaw = np.zeros(1)
    pitch = np.zeros(1)
    roll = np.zeros(1)

    for i, row in saccade_df.iterrows():
        # calculate intersaccadic residual rotation
        yaw_inter = np.linspace(0, row.intersac_drifty_f, row.intersac_length)
        pitch_inter = np.linspace(
            0, row.intersac_driftp_f, row.intersac_length)
        roll_inter = np.linspace(0, row.intersac_driftr_f, row.intersac_length)
        # update yaw,pitch,roll
        yaw = np.hstack((yaw,  yaw[-1] + yaw_inter))
        pitch = np.hstack((pitch, pitch[-1] + pitch_inter))
        roll = np.hstack((roll, roll[-1] + roll_inter))
        # calculate saccade
        yaw_sac = generate_saccade(row.sac_y_f)
        pitch_sac = generate_saccade(row.sac_p_f)
        roll_sac = generate_saccade(row.sac_r_f)
        # find longest
        if (len(yaw_sac) >= len(pitch_sac)) and\
           (len(yaw_sac) >= len(roll_sac)):
            # yaw is longest
            pitch_sac = yaw_sac * np.sum(pitch_sac) / np.sum(yaw_sac)
            roll_sac = yaw_sac * np.sum(roll_sac) / np.sum(yaw_sac)
        elif (len(pitch_sac) >= len(yaw_sac)) and\
             (len(pitch_sac) >= len(roll_sac)):
            # pitch is longest
            yaw_sac = pitch_sac * np.sum(yaw_sac) / np.sum(pitch_sac)
            roll_sac = pitch_sac * np.sum(roll_sac) / np.sum(pitch_sac)
        elif (len(roll_sac) >= len(yaw_sac)) and\
             (len(roll_sac) >= len(pitch_sac)):
            # roll is longest
            yaw_sac = roll_sac * np.sum(yaw_sac) / np.sum(roll_sac)
            pitch_sac = roll_sac * np.sum(pitch_sac) / np.sum(roll_sac)
        else:
            mgs = 'Error in saccade generation, '
            mgs += 'can not find the longest saccade'
            raise NameError(mgs)
        # update yaw,pitch,roll
        yaw = np.hstack((yaw, yaw[-1] + np.cumsum(yaw_sac)))
        pitch = np.hstack((pitch, pitch[-1] + np.cumsum(pitch_sac)))
        roll = np.hstack((roll, roll[-1] + np.cumsum(roll_sac)))

    return yaw, pitch, roll, saccade_df


def saccadic_traj(intersac_length_f=lambda n: 50 + np.floor(
        10 * np.random.rand(n)),
    intersac_drifty_f=lambda n: (
    3 * np.pi / 180) * (2 * (np.random.rand(n) - 0.5)),
    intersac_driftp_f=lambda n: (
    0 * np.pi / 180) * (2 * (np.random.rand(n) - 0.5)),
    intersac_driftr_f=lambda n: (
    0 * np.pi / 180) * (2 * (np.random.rand(n) - 0.5)),
    sac_y_f=lambda n: (np.pi / 2) *
    (2 * (np.random.rand(n) - 0.5)),
    sac_p_f=lambda n: (np.pi / 2) *
    (2 * (np.random.rand(n) - 0.5)),
    sac_r_f=lambda n: (np.pi / 2) *
    (2 * (np.random.rand(n) - 0.5)),
        number_sac=10):
    # generate fake saccadic data
    yaw, pitch, roll, saccade_df = saccadic_data(intersac_length_f,
                                                 intersac_drifty_f,
                                                 intersac_driftp_f,
                                                 intersac_driftr_f,
                                                 sac_y_f,
                                                 sac_p_f, sac_r_f,
                                                 number_sac)
    speed = 1 + np.zeros(len(yaw))
    starting_point = np.array([0, 0, 0])
    # calculate trajectory
    trajectory = generate_trajectory(starting_point,
                                     speed, yaw, pitch, roll)
    return trajectory, saccade_df
