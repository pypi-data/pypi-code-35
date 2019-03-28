"""
   Tools for markers
"""
from scipy import signal
from scipy.interpolate import interp1d
import pandas as pd
import numpy as np
from navipy import tools as tratools
import fastdtw
from navipy.trajectories import Trajectory


def averaged_trajectory(alltraj):
    """ Calculate an average trajectory

    Trajectories are aligned by using dynamic time wraping (dtw). \
The alignment is relative to the first trajectory in the list. Therefore \
the average trajectory will have the same length that the first trajectory.

    Aligned trajectory are aligned as follow. The mean of average position \
corresponding to the time of the first trajectory devided by the number of \
trajectory are summed over all trajectory. For the orientation, the circular \
mean is used according to `Statistics on Sphere` Geoffrey S. Watson 1983.

    :param alltraj: A list of trajectories
    :returns: An average trajectory
    """
    rotconv = alltraj[0].rotation_mode
    traj_1 = alltraj[0].dropna().values
    avg_traj = traj_1.copy()
    avg_traj[:, 0:3] /= len(alltraj)
    for traj_2 in alltraj[1:]:
        traj_2 = traj_2.dropna().values
        x = np.array(traj_1[:, [0, 1, 2]], dtype='float')
        y = np.array(traj_2[:, [0, 1, 2]], dtype='float')
        test = fastdtw.fastdtw(x, y)

        # average
        for ii, group in pd.DataFrame(test[1]).groupby(0):
            # average position
            avg_traj[ii, 0:3] += np.mean(traj_2[group.loc[:, 1],
                                                0:3], axis=0) / len(alltraj)
            # average angles
            # see Statistics On Spheres", Geoffrey S. Watson,
            # University of Arkansas Lecture Notes
            # in the Mathematical Sciences, 1983 John Wiley & Son
            for kk in range(3, 6):
                sinsum = np.sum(np.sin(traj_2[group.loc[:, 1], kk]), axis=0)
                cossum = np.sum(np.cos(traj_2[group.loc[:, 1], kk]), axis=0)
                sinsum += np.sin(avg_traj[ii, kk])
                cossum += np.cos(avg_traj[ii, kk])
                avg_traj[ii, kk] = np.arctan2(sinsum, cossum)

    return Trajectory().from_array(avg_traj, rotconv=rotconv)


def interpolate_markers(markers, kind='cubic'):
    """
       Interpolate marker position where Nan are
    """
    columns = markers.columns
    markers_inter = markers.copy()
    for col in columns:
        y = markers_inter.loc[:, col]
        valid_y = y.dropna()
        valid_t = valid_y.index
        nan_y = y.isnull().nonzero()[0]

        func = interp1d(valid_t, valid_y, kind='cubic')
        markers_inter.loc[nan_y, col] = func(nan_y)
    return markers_inter


def filter_markers(markers, cutfreq, order):
    if cutfreq < order:
        raise ValueError(
            'cutoffrequency {} can not be lower than order {}'.format(
                cutfreq, order))
    nyquist = markers.index.name / 2
    if cutfreq > nyquist:
        raise ValueError(
            'cutoffrequency {} can not be higher than Nyquist freq {}'.format(
                cutfreq, nyquist))
    b, a = signal.butter(order, cutfreq / nyquist)

    columns = markers.columns
    markers_filt = markers.copy()
    for col in columns:
        markers_filt.loc[:, col] = signal.filtfilt(b, a, markers.loc[:, col])
    return markers_filt


def extract_sacintersac(trajectory, thresholds):
    """
        add a intersaccade and saccade index the trajectory
        therefore intersaccade, and saccade columns will be added
        to the trajectory dataframe
    """
    # assign
    saccade_intersaccde = pd.DataFrame(index=trajectory.index,
                                       columns=['intersaccade',
                                                'saccade',
                                                'smooth_angvel'])

    # calculate velocity
    velocity = trajectory.velocity()
    angvel = np.sqrt(
        np.sum(velocity.loc[:, ['dalpha_0',
                                'dalpha_1',
                                'dalpha_2']]**2,
               axis=1))
    # find block of nonan
    block_nonandf = tratools.extract_block_nonans(angvel)
    block_nonandf = block_nonandf.astype(int)
    # print(block_nonandf)

    sac_number = 0
    intersac_number = 0
    for i, curr_blocknonan in block_nonandf.iterrows():
        current_item = np.arange(
            curr_blocknonan.start_th1, curr_blocknonan.end_th1)
        if len(current_item) < 1:
            continue
        # extract block
        data = angvel[current_item].abs()
        block_df = tratools.extract_block(data, thresholds)

        sac_e_p = current_item[0]
        for _, row in block_df.iterrows():
            sac_s = row.start_th2
            sac_e = row.end_th2
            # check boundary
            if sac_s < current_item[0]:
                sac_s = current_item[0]
            if sac_e > current_item[-1]:
                sac_e = current_item[-1]

            frame_s = np.arange(sac_s, sac_e).astype(int)
            frame_i = np.arange(sac_e_p, sac_s).astype(int)
            if len(frame_s) > 0:
                saccade_intersaccde.loc[frame_s,
                                        'saccade'] = sac_number
                sac_number += 1
            if len(frame_i) > 0:
                saccade_intersaccde.loc[frame_i,
                                        'intersaccade'] = intersac_number
                intersac_number += 1

            sac_e_p = sac_e

        frame_i = np.arange(sac_e_p, current_item[-1]).astype(int)
        if len(frame_i) > 0:
            saccade_intersaccde.loc[frame_i,
                                    'intersaccade'] = intersac_number
            intersac_number += 1

    return saccade_intersaccde, angvel
