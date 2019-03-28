"""
Function for camera calibrations
"""
import pandas as pd
import numpy as np
import cv2
import os
from navipy.io import ivfile
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa F401


def concatenate_manhattan_2d3d(manhattan_3d, manhattan_2d):
    """ Join 3D and 2D points for pose estimation """
    if not isinstance(manhattan_2d, pd.DataFrame):
        raise TypeError('manhattan_2d should be a DataFrame')
    if not isinstance(manhattan_3d, pd.DataFrame):
        raise TypeError('manhattan_3d should be a DataFrame')
    d = {'three_d': manhattan_3d, 'two_d': manhattan_2d}
    manhattan_3d2d = pd.concat(d.values(), axis=1, keys=d.keys())
    manhattan_3d2d = manhattan_3d2d.astype(float)
    return manhattan_3d2d


def objects_points_from_manhattan(manhattan_3d2d):
    """return objects points from a join manhatta

    .. seealso: concatenate_manhattan_2d3d
    """
    if not isinstance(manhattan_3d2d, pd.DataFrame):
        raise TypeError('manhattan_3d2d should be a DataFrame')
    return manhattan_3d2d.dropna().loc[:, 'three_d']\
                                  .loc[:, ['x', 'y', 'z']].values


def image_points_from_manhattan(manhattan_3d2d):
    """return image points from a joined manhattan

    .. seelso: concatenate_manhattan_2d3d
    """
    if not isinstance(manhattan_3d2d, pd.DataFrame):
        raise TypeError('manhattan_3d2d should be a DataFrame')
    return manhattan_3d2d.dropna().loc[:, 'two_d'].loc[:, ['x', 'y']].values


def compose_from_vectors(rvec, tvec):
    """return camera pose from rotation and translation vectors
    """
    r = cv2.Rodrigues(rvec)[0]
    camera_pose = np.hstack((r, tvec))
    camera_pose = np.vstack((camera_pose, [0, 0, 0, 1]))
    return camera_pose


def camera_pose(manhattan_2d, manhattan_3d, camera_intrinsics):
    """solvePnP with 3D-2D points correspondance.

    The camera intrinsics have to be known appriori
    """
    camera_matrix = camera_intrinsics['intrinsic_matrix']
    distcoeffs = camera_intrinsics['distortion']

    manhattan_2d3d = concatenate_manhattan_2d3d(manhattan_3d, manhattan_2d)
    objects_points = objects_points_from_manhattan(manhattan_2d3d)
    image_points = image_points_from_manhattan(manhattan_2d3d)

    retval, rvec, tvec = cv2.solvePnP(
        objects_points, image_points, camera_matrix, distcoeffs)

    return compose_from_vectors(rvec, tvec)


def calibrates_extrinsic(filenames,
                         manhattan_3d,
                         cameras_intrinsics,
                         corner_th=-1,
                         manhattan_3d_key='manhattan'):
    """Calibrate from files.

    :param filenames: a list of ivfile name with manhattan markers
    :param file_manhattan_3d: hdf file with manhattan_3d_key to load \
containing a pandas dataframe with x,y,z coordinates of each points.
    :param cameras_intrinsics: a list of camera intrinsics
    :param corner_th: a threshold for points to be ignored on the top\
 right image corner (useful when certain points are not visible)
    :param manhattan_3d_key: the key to load the manhattan_3d \
(default: manhattan)
    """
    cameras_extrinsics = dict()
    for cam_i, cfile in filenames.items():
        _, ext = os.path.splitext(cfile)
        if ext == '.tra':
            manhattan_2d = ivfile.manhattan(cfile, corner_th)
        elif ext == '.csv':
            manhattan_2d = pd.read_csv(cfile,
                                       names=['x', 'y'],
                                       header=0)
            idx = (manhattan_2d.x < corner_th) & (manhattan_2d.y < corner_th)
            manhattan_2d.x[idx] = np.nan
            manhattan_2d.y[idx] = np.nan
        else:
            msg = 'FileType not understood (only .tra, .csv are supported)'
            raise ValueError(msg)
        cameras_extrinsics[cam_i] = dict()
        cameras_extrinsics[cam_i]['pose'] = camera_pose(
            manhattan_2d, manhattan_3d, cameras_intrinsics[cam_i])
    return cameras_extrinsics


def plot_manhattan(manhattan_3d, figsize=(15, 15), unit=None):
    """Plot a manhattan dataframe

    :param manhattan_3d: x,y,z coordinates of each tower
    :param figsize: figure size
    :returns: figure and axis handles

    """
    if unit is None:
        try:
            unit = manhattan.unit
        except AttributeError as e:
            pass
    if unit is None:
        unit = 'no-unit'

    fig = plt.figure(figsize=figsize)
    ax0 = fig.add_subplot(221)
    ax1 = fig.add_subplot(223)
    ax3 = fig.add_subplot(224)
    for ax, col_i, col_j in zip([ax1, ax0, ax3],
                                ['x', 'x', 'z'],
                                ['y', 'z', 'y']):
        ax.plot(manhattan_3d.loc[:, col_i], manhattan_3d.loc[:, col_j], 'ko')
        ax.set_xlabel('{} [{}]'.format(col_i, unit))
        ax.set_ylabel('{} [{}]'.format(col_j, unit))
        ax.axis('equal')

    # Annotate
    for row_i, row_val in manhattan_3d.iterrows():
        shift = [10, 10]
        xy = row_val.loc[['x', 'y']]
        xytext = xy - 2 * ((xy > 0) - 0.5) * shift
        ax1.annotate('{}'.format(row_i), xy, xytext)

    ax4 = fig.add_subplot(222, projection='3d')
    for i, row in manhattan_3d.iterrows():
        ax4.plot([row.x, row.x],
                 [row.y, row.y],
                 [0, row.z], 'k-.')
    ax4.set_xlabel('{} [{}]'.format('x', unit))
    ax4.set_ylabel('{} [{}]'.format('y', unit))
    ax4.set_zlabel('{} [{}]'.format('z', unit))
    return fig, [ax0, ax1, ax3, ax4]
