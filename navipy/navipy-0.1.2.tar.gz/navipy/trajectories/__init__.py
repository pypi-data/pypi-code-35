"""
  Trajectory in navipy
"""
import pandas as pd
import numpy as np
from navipy.maths import constants as mconst
from navipy.maths import quaternion as htq
from navipy.maths import euler as hte
from navipy.maths import homogeneous_transformations as htf
from navipy.errorprop import propagate_error
from .transformations import markers2translate, markers2euler
from navipy.tools.plots import get_color_dataframe
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa F401
from multiprocessing import Pool
from functools import partial
import time
from scipy import signal
from scipy.interpolate import CubicSpline
import warnings


def posorient_columns(convention):
    toreturn = [('location', 'x'),
                ('location', 'y'),
                ('location', 'z')]
    if convention == 'quaternion':
        for a in range(4):
            toreturn.append((convention, 'q_{}'.format(a)))
    else:
        for a in range(3):
            toreturn.append((convention, 'alpha_{}'.format(a)))
    return toreturn


def velocities_columns(convention):
    toreturn = []
    # Prepend d on dimention for derivative
    for it1, it2 in posorient_columns(convention):
        toreturn.append((it1, 'd' + it2))
    return toreturn


def _markers2position(x, kwargs):
    mark0 = pd.Series(x[: 3], index=['x', 'y', 'z'])
    mark1 = pd.Series(x[3: 6], index=['x', 'y', 'z'])
    mark2 = pd.Series(x[6:], index=['x', 'y', 'z'])
    triangle_mode = kwargs['triangle_mode']
    euler_axes = kwargs['euler_axes']
    correction = kwargs['correction']
    return markers2translate(mark0, mark1, mark2,
                             triangle_mode, euler_axes, correction)


def _markers2angles(x, kwargs):
    mark0 = pd.Series(x[:3], index=['x', 'y', 'z'])
    mark1 = pd.Series(x[3:6], index=['x', 'y', 'z'])
    mark2 = pd.Series(x[6:], index=['x', 'y', 'z'])
    triangle_mode = kwargs['triangle_mode']
    euler_axes = kwargs['euler_axes']
    correction = kwargs['correction']
    return markers2euler(mark0, mark1, mark2,
                         triangle_mode, euler_axes, correction)


def _markerstransform(index_i, trajectory,
                      homogeneous_markers, rotation_mode):
    row = trajectory.loc[index_i]
    angles = row.loc[rotation_mode].values
    translate = row.loc['location'].values
    trans_mat = htf.compose_matrix(angles=angles,
                                   translate=translate,
                                   axes=rotation_mode)
    tmarker = trans_mat.dot(homogeneous_markers)
    tmarker = pd.DataFrame(data=tmarker,
                           index=homogeneous_markers.index,
                           columns=homogeneous_markers.columns)
    # We do not need w
    tmarker = tmarker.loc[['x', 'y', 'z'], :].unstack()
    tmarker.name = index_i
    return tmarker


def _invmarkerstransform(index_i, trajectory,
                         homogeneous_markers, rotation_mode):
    row = trajectory.loc[index_i]
    angles = row.loc[rotation_mode].values
    translate = row.loc['location'].values
    trans_mat = htf.compose_matrix(angles=angles,
                                   translate=translate,
                                   axes=rotation_mode)
    tmarker = np.linalg.inv(trans_mat).dot(homogeneous_markers)
    tmarker = pd.DataFrame(data=tmarker,
                           index=homogeneous_markers.index,
                           columns=homogeneous_markers.columns)
    # We do not need w
    tmarker = tmarker.loc[['x', 'y', 'z'], :].unstack()
    tmarker.name = index_i
    return tmarker


class Trajectory(pd.DataFrame):
    def __init__(self, rotconv='zyx', indeces=np.arange(1)):
        columns = self.__build_columns(rotconv)
        super().__init__(index=indeces, columns=columns, dtype=np.float)
        self.__rotconv = rotconv
        self.sampling_rate = 0

    def __build_columns(self, rotconv):
        if rotconv == 'quaternion':
            index = pd.MultiIndex.from_tuples(
                [('location', 'x'), ('location', 'y'),
                 ('location', 'z'), (rotconv, 'q_0'),
                    (rotconv, 'q_1'), (rotconv, 'q_2'),
                 (rotconv, 'q_3')])
        elif rotconv in mconst._AXES2TUPLE.keys():
            index = pd.MultiIndex.from_tuples(
                [('location', 'x'), ('location', 'y'),
                 ('location', 'z'), (rotconv, 'alpha_0'),
                    (rotconv, 'alpha_1'), (rotconv, 'alpha_2')])
        else:
            msg = 'convention for rotation {} is not suppored\n'
            msg += msg.format(rotconv)
            msg += 'the following convention are supported\n:'
            for rconv in mconst._AXES2TUPLE.keys():
                msg += '{}\n'.format(rconv)
            msg += 'quaternion\n'
            raise KeyError(msg)
        return index

    @property
    def rotation_mode(self):
        return self.__rotconv

    @rotation_mode.setter
    def rotation_mode(self, rotation_mode):
        """Convert current rotation_mode to a different one

        :param rotation_mode: the new rotation mode to be assigned
        """
        oldrotmod = self.rotation_mode
        neworient = pd.DataFrame(index=self.index,
                                 columns=self.__build_columns(rotation_mode),
                                 dtype=float)
        neworient.drop(inplace=True, labels='location', level=0, axis=1)
        for index_i, row in self.iterrows():
            if rotation_mode == 'quaternion':
                orient = htq.from_euler(row.angle_0,
                                        row.angle_1,
                                        row.angle_2,
                                        axes=oldrotmod)
            else:
                m = hte.matrix(ai=row.loc[(self.rotation_mode, 'alpha_0')],
                               aj=row.loc[(self.rotation_mode, 'alpha_1')],
                               ak=row.loc[(self.rotation_mode, 'alpha_2')],
                               axes=oldrotmod)
                orient = hte.from_matrix(m, axes=rotation_mode)
            neworient.loc[index_i, rotation_mode] = orient
        self.drop(inplace=True, labels=oldrotmod, level=0, axis=1)
        for col in neworient.columns:
            self[col] = neworient.loc[:, col]
        self.__rotconv = rotation_mode

    def facing_direction(self):
        """
        Return facing vector
        """
        facing = pd.DataFrame(index=self.index,
                              columns=['x', 'y', 'z'],
                              dtype=float)
        for i, row in self.iterrows():
            if self.rotation_mode == 'quaternion':
                mat = htq.matrix(row.loc[self.rotation_mode].values)
            else:
                mat = hte.matrix(row.loc[(self.rotation_mode, 'alpha_0')],
                                 row.loc[(self.rotation_mode, 'alpha_1')],
                                 row.loc[(self.rotation_mode, 'alpha_2')],
                                 axes=self.rotation_mode)[:3, :3]
            orient = np.dot(mat,
                            np.array([[1], [0], [0]]))[:, 0]
            facing.loc[i, ['x', 'y', 'z']] = orient
        return facing

    @property
    def sampling_rate(self):
        return self.__sampling_rate

    @sampling_rate.setter
    def sampling_rate(self, sampling_rate):
        self.__sampling_rate = sampling_rate

    @property
    def x(self):
        return self.loc[:, ('location', 'x')]

    @x.setter
    def x(self, x):
        self.loc[:, ('location', 'x')] = x

    @property
    def y(self):
        return self.loc[:, ('location', 'y')]

    @y.setter
    def y(self, y):
        self.loc[:, ('location', 'y')] = y

    @property
    def z(self):
        return self.loc[:, ('location', 'z')]

    @z.setter
    def z(self, z):
        self.loc[:, ('location', 'z')] = z

    def __get_alpha_i(self, alphai):
        if self.__rotconv != 'quaternion':
            return self.loc[:, (self.__rotconv, 'alpha_{}'.format(alphai))]
        else:
            msg = 'alpha_{0:} does not exist for quaternion (try q_{0:})'
            raise ValueError(msg.format(alphai))

    def __set_alpha_i(self, alphai, val):
        if self.__rotconv != 'quaternion':
            self.loc[:, (self.__rotconv, 'alpha_{}'.format(alphai))] = val
        else:
            msg = 'alpha_{0:} does not exist for quaternion (try q_{0:})'
            raise ValueError(msg.format(alphai))

    @property
    def alpha_0(self):
        return self.__get_alpha_i(0)

    @alpha_0.setter
    def alpha_0(self, alpha_0):
        self.__set_alpha_i(0, alpha_0)

    @property
    def alpha_1(self):
        return self.__get_alpha_i(1)

    @alpha_1.setter
    def alpha_1(self, alpha_1):
        self.__set_alpha_i(1, alpha_1)

    @property
    def alpha_2(self):
        return self.__get_alpha_i(2)

    @alpha_2.setter
    def alpha_2(self, alpha_2):
        self.__set_alpha_i(2, alpha_2)

    def __get_q_i(self, qi):
        if self.__rotconv == 'quaternion':
            return self.loc[:, (self.__rotconv, 'q_{}'.format(qi))]
        else:
            msg = 'q_{0:} does not exist for none quaternion (try alpha_{0:})'
            raise ValueError(msg.format(qi))

    def __set_q_i(self, qi, val):
        if self.__rotconv != 'quaternion':
            self.loc[:, (self.__rotconv, 'q_{}'.format(qi))] = val
        else:
            msg = 'q_{0:} does not exist for none quaternion (try alpha_{0:})'
            raise ValueError(msg.format(qi))

    @property
    def q_0(self):
        return self.__get_q_i(0)

    @q_0.setter
    def q_0(self, q_0):
        self.__set_q_i(0, q_0)

    @property
    def q_1(self):
        return self.__get_q_i(1)

    @q_1.setter
    def q_1(self, q_1):
        self.__set_q_i(1, q_1)

    @property
    def q_2(self):
        return self.__get_q_i(2)

    @q_2.setter
    def q_2(self, q_2):
        self.__set_q_i(2, q_2)

    @property
    def q_3(self):
        return self.__get_q_i(3)

    @q_3.setter
    def q_3(self, q_3):
        self.__set_q_i(3, q_3)

    # -------------------------------------------
    # ---------------- IO -----------------------
    # -------------------------------------------
    def read_csv(self, filename, sep=',', header=[0, 1], index_col=0):
        """ Load from a hdf file
        """
        df = pd.read_csv(filename, sep=sep,
                         header=[0, 1], index_col=0)
        self.from_dataframe(df)
        return self

    def read_hdf(self, filename):
        df = pd.read_hdf(filename)
        self.from_dataframe(df)
        return self

    def to_hdf(self, filename):
        df = pd.DataFrame(self)
        df.to_hdf(filename, key='posorients')

    def to_csv(self, filename):
        df = pd.DataFrame(self)
        df.to_csv(filename)

    # -------------------------------------------
    # ---------------- INITS FROM VAR------------
    # -------------------------------------------
    def from_array(self, nparray, rotconv, indeces=None):
        """ Assign trajectory from a numpy array
            N x 6 (rotconv = Euler angles)
            N x 7 (rotconv = quaternion)
        """
        # Check user input
        if not isinstance(nparray, np.ndarray):
            msg = 'nparray should be a np.ndarray and not {}'
            msg = msg.format(type(nparray))
            raise TypeError(msg)
        if indeces is None:
            indeces = np.arange(0, nparray.shape[0])
        if not isinstance(indeces, np.ndarray):
            msg = 'indeces should be a np.ndarray and not {}'
            msg = msg.format(type(indeces))
            raise TypeError(msg)
        if indeces.shape[0] != nparray.shape[0]:
            msg = 'indeces and nparray should have same number of rows'
            msg += '{}!={}'
            msg = msg.format(indeces.shape[0], nparray.shape[0])
            raise TypeError(msg)
        if rotconv == 'quaternion':
            if nparray.shape[1] != 7:
                msg = 'nparray should have size Nx7 and not {}'
                msg = msg.format(nparray.shape)
                raise ValueError(msg)
        elif rotconv in mconst._AXES2TUPLE.keys():
            if nparray.shape[1] != 6:
                msg = 'nparray should have size Nx6 and not {}'
                msg = msg.format(nparray.shape)
                raise ValueError(msg)
        columns = self.__build_columns(rotconv)
        super().__init__(index=indeces, columns=columns)
        self.__rotconv = rotconv
        # Position
        self.x = nparray[:, 0]
        self.y = nparray[:, 1]
        self.z = nparray[:, 2]
        # Orientation
        if self.__rotconv == 'quaternion':
            self.q_0 = nparray[:, 3]
            self.q_1 = nparray[:, 4]
            self.q_2 = nparray[:, 5]
            self.q_3 = nparray[:, 6]
        else:
            self.alpha_0 = nparray[:, 3]
            self.alpha_1 = nparray[:, 4]
            self.alpha_2 = nparray[:, 5]
        return self

    def from_dataframe(self, df, rotconv=None):
        """ Assign trajectory from a dataframe
        """
        if 'rotconv_id' in df.columns:
            rotconv = df.loc[:, 'rotconv_id']
            if not np.all(rotconv == rotconv.iloc[0]):
                raise ValueError('More than one rotconv detected')
            rotconv = rotconv.iloc[0]  # They are all the same :)
        elif isinstance(df.columns, pd.MultiIndex):
            if 'location' in df.columns.levels[0]:
                rotconv = df.columns.levels[0].drop('location')
                if len(rotconv) == 1:
                    rotconv = rotconv[0]
                else:
                    msg = 'Could not determine rotconv from columns header'
                    msg += '\n{}'.format(df.columns)
                    raise ValueError(msg)
            else:
                msg = 'Could not determine rotconv from columns header'
                msg += '\n{}'.format(df.columns)
                raise ValueError(msg)

        elif rotconv is None:
            msg = 'When dataframe does not contains rotconv_id,'
            msg += 'a convention should be given'
            raise ValueError(msg)

        indeces = df.index
        columns = self.__build_columns(rotconv)
        super().__init__(index=indeces, columns=columns)
        self.__rotconv = rotconv
        # Position
        if isinstance(df.columns, pd.MultiIndex):
            self.x = df.loc[:, ('location', 'x')]
            self.y = df.loc[:, ('location', 'y')]
            self.z = df.loc[:, ('location', 'z')]
        else:
            self.x = df.x
            self.y = df.y
            self.z = df.z
        # Orientation
        if self.__rotconv == 'quaternion':
            if isinstance(df.columns, pd.MultiIndex):
                self.q_0 = df.loc[:, (rotconv, 'q_0')]
                self.q_1 = df.loc[:, (rotconv, 'q_1')]
                self.q_2 = df.loc[:, (rotconv, 'q_2')]
                self.q_3 = df.loc[:, (rotconv, 'q_3')]
            else:
                self.q_0 = df.q_0
                self.q_1 = df.q_1
                self.q_2 = df.q_2
                self.q_3 = df.q_3
        else:
            if 'q_0' in df.columns:
                self.alpha_0 = df.q_0
            elif 'alpha_0' in df.columns:
                self.alpha_0 = df.alpha_0
            elif isinstance(df.columns, pd.MultiIndex):
                if 'q_0' in df.columns.levels[1]:
                    self.alpha_0 = df.loc[:, (rotconv, 'q_0')]
                elif 'alpha_0' in df.columns.levels[1]:
                    self.alpha_0 = df.loc[:, (rotconv, 'alpha_0')]
                else:
                    msg = 'df should contains q_0 or alpha_0'
                    msg += 'columns are:\n{}'.format(df.columns)
                    raise KeyError(msg)
            else:
                raise KeyError('df should contains q_0 or alpha_0')

            if 'q_1' in df.columns:
                self.alpha_1 = df.q_1
            elif 'alpha_1' in df.columns:
                self.alpha_1 = df.alpha_1
            elif isinstance(df.columns, pd.MultiIndex):
                if 'q_1' in df.columns.levels[1]:
                    self.alpha_1 = df.loc[:, (rotconv, 'q_1')]
                elif 'alpha_1' in df.columns.levels[1]:
                    self.alpha_1 = df.loc[:, (rotconv, 'alpha_1')]
                else:
                    msg = 'df should contains q_1 or alpha_1'
                    msg += 'columns are:\n{}'.format(df.columns)
                    raise KeyError(msg)
            else:
                raise KeyError('df should contains q_1 or alpha_1')

            if 'q_2' in df.columns:
                self.alpha_2 = df.q_2
            elif 'alpha_2' in df.columns:
                self.alpha_2 = df.alpha_2
            elif isinstance(df.columns, pd.MultiIndex):
                if 'q_2' in df.columns.levels[1]:
                    self.alpha_2 = df.loc[:, (rotconv, 'q_2')]
                elif 'alpha_2' in df.columns.levels[1]:
                    self.alpha_2 = df.loc[:, (rotconv, 'alpha_2')]
                else:
                    msg = 'df should contains q_2 or alpha_2'
                    msg += 'columns are:\n{}'.format(df.columns)
                    raise KeyError(msg)
            else:
                raise KeyError('df should contains q_2 or alpha_2')
        return self

    def from_markers(self, markers, triangle_mode, correction=np.eye(4),
                     error=None, markers_labels=[0, 1, 2]):
        indeces = markers.index
        # Reinit the pandas dataframe super class
        # because we now know the indeces
        super().__init__(index=indeces, columns=self.columns, dtype=float)
        # If error is provided, we can propagate the error
        if error is not None:
            self.trajectory_error = pd.DataFrame(data=np.nan,
                                                 index=self.index,
                                                 columns=self.columns)
        markers2use = markers.loc[:, markers_labels]
        markers2use = markers2use.dropna()
        mark0 = markers2use.loc[:, markers_labels[0]]
        mark1 = markers2use.loc[:, markers_labels[1]]
        mark2 = markers2use.loc[:, markers_labels[2]]
        x = np.zeros(9)  # 3points with x,y,z
        kwargs = {'triangle_mode': triangle_mode,
                  'euler_axes': self.rotation_mode,
                  'correction': correction}
        for index_i in markers2use.index:
            # Assign mark to pos
            x[0:3] = mark0.loc[index_i, ['x', 'y', 'z']].values
            x[3:6] = mark1.loc[index_i, ['x', 'y', 'z']].values
            x[6:] = mark2.loc[index_i, ['x', 'y', 'z']].values
            # Calculate position and orientation
            position = _markers2position(x, kwargs)
            orientation = _markers2angles(x, kwargs)
            # propagate error
            if error is not None:
                euclidian_error = error.loc[index_i]
                if not np.isnan(euclidian_error):
                    covar = euclidian_error * np.eye(9)
                    err_pos = propagate_error(_markers2position, x,
                                              covar, args=kwargs,
                                              epsilon=euclidian_error / 10)

                    err_angle = propagate_error(_markers2angles, x,
                                                covar, args=kwargs,
                                                epsilon=euclidian_error / 10)
                    self.trajectory_error.loc[index_i, 'location'] = \
                        np.diagonal(err_pos)
                    self.trajectory_error.loc[index_i, self.rotation_mode] \
                        = np.diagonal(err_angle)

            self.loc[index_i, 'location'] = position
            self.loc[index_i, self.rotation_mode] = orientation
        return self

    # -----------------------------------------------
    # ---------------- TRANSFORM --------------------
    # -----------------------------------------------
    def body2world(self, markers, indeces=None):
        """ Transform markers in body coordinate to world coordinate
        """
        if not isinstance(markers, pd.Series):
            msg = 'markers should be of type pd.Series and not'
            msg += ' {}'.format(type(markers))
            raise TypeError(msg)
        if not isinstance(markers.index, pd.MultiIndex):
            msg = 'markers should have a multiIndex index \n'
            msg += ' (i,"x"), (i,"y"),(i,"z")\n'
            msg += 'here i is the index of the marker'
            raise TypeError(msg)
        if indeces is None:
            # Looping through each time point along the trajectory
            indeces = self.index
        # More than one marker may be transformed
        # The marker are assume to be a multiIndex dataframe
        homogeneous_markers = markers.unstack()
        homogeneous_markers['w'] = 1
        # Make sure that columns are correctly ordered
        homogeneous_markers = homogeneous_markers[['x', 'y', 'z', 'w']]
        # Transpose because we apply homogeneous transformation
        # on the marker, and thus a 4x4 matrix on a 4xN matrix
        # here N is the number of markers
        homogeneous_markers = homogeneous_markers.transpose()
        # Looping throught the indeces
        # to get the homogeneous transformation from the position orientation
        # and then apply the transformed to the marker position
        with Pool() as p:
            result = p.map(
                partial(_markerstransform,
                        trajectory=self,
                        homogeneous_markers=homogeneous_markers,
                        rotation_mode=self.rotation_mode),
                indeces)
        # unwrap results
        indeces = [res.name for res in result]
        transformed_markers = pd.DataFrame(data=result,
                                           index=indeces,
                                           columns=markers.index,
                                           dtype=float)
        return transformed_markers

    def world2body(self, markers, indeces=None):
        """ Transform markers in world coordinate to body coordinate
        """
        msg = 'Prior to 12/09/2018:\n'
        msg += 'world2body was doing a reverse transformed\n'
        msg += 'Please use body2world instead'
        warnings.warn(msg)
        if not isinstance(markers, pd.Series):
            msg = 'markers should be of type pd.Series and not'
            msg += ' {}'.format(type(markers))
            raise TypeError(msg)
        if not isinstance(markers.index, pd.MultiIndex):
            msg = 'markers should have a multiIndex index \n'
            msg += ' (i,"x"), (i,"y"),(i,"z")\n'
            msg += 'here i is the index of the marker'
            raise TypeError(msg)
        if indeces is None:
            # Looping through each time point along the trajectory
            indeces = self.index
        # More than one marker may be transformed
        # The marker are assume to be a multiIndex dataframe
        homogeneous_markers = markers.unstack()
        homogeneous_markers['w'] = 1
        # Make sure that columns are correctly ordered
        homogeneous_markers = homogeneous_markers[['x', 'y', 'z', 'w']]
        # Transpose because we apply homogeneous transformation
        # on the marker, and thus a 4x4 matrix on a 4xN matrix
        # here N is the number of markers
        homogeneous_markers = homogeneous_markers.transpose()
        # Looping throught the indeces
        # to get the homogeneous transformation from the position orientation
        # and then apply the transformed to the marker position
        with Pool() as p:
            result = p.map(
                partial(_invmarkerstransform,
                        trajectory=self,
                        homogeneous_markers=homogeneous_markers,
                        rotation_mode=self.rotation_mode),
                indeces)
        # unwrap results
        indeces = [res.name for res in result]
        transformed_markers = pd.DataFrame(data=result,
                                           index=indeces,
                                           columns=markers.index,
                                           dtype=float)
        return transformed_markers

    def differentiate(self, periods=1):
        """differentiate the trajectory and rename columns as d+col

        :param periods: periods as in pd.diff()
        :returns: Diff of the trajectory
        :rtype: pd.DataFrame with MultiIndex

        """
        mytrajdiff = self.diff(periods=1)
        d = dict(zip(mytrajdiff.columns.levels[1],
                     ['d' + col for col in mytrajdiff.columns.levels[1]]))
        mytrajdiff = mytrajdiff.rename(columns=d, level=1)
        mytrajdiff.dropna().head()
        return mytrajdiff

    def velocity(self):
        """ Calculate the velocity on a trajectory
        """
        velocity = pd.DataFrame(index=self.index,
                                columns=['dx', 'dy', 'dz',
                                         'dalpha_0',
                                         'dalpha_1',
                                         'dalpha_2'],
                                dtype=float)
        diffrow = self.diff()
        velocity.loc[:, ['dx', 'dy', 'dz']] = diffrow.loc[:, 'location'].values
        # Look for true zeros in order to save time
        true_zeros = diffrow == 0
        diffrow[true_zeros] = np.nan
        velocity[true_zeros[self.rotation_mode]] = 0
        # Loop only on non true zeros
        for index_i in diffrow.loc[:, self.rotation_mode].dropna().index:
            row = self.loc[index_i, :]
            if self.rotation_mode == 'quaternion':
                raise NameError('Not implemented')
            else:
                rot = hte.angular_velocity(
                    ai=row.loc[(self.rotation_mode, 'alpha_0')],
                    aj=row.loc[(self.rotation_mode, 'alpha_1')],
                    ak=row.loc[(self.rotation_mode, 'alpha_2')],
                    dai=diffrow.loc[index_i, (self.rotation_mode,
                                              'alpha_0')],
                    daj=diffrow.loc[index_i, (self.rotation_mode,
                                              'alpha_1')],
                    dak=diffrow.loc[index_i, (self.rotation_mode,
                                              'alpha_2')],
                    axes=self.rotation_mode)
            velocity.loc[index_i, ['dalpha_0',
                                   'dalpha_1',
                                   'dalpha_2']] = rot.squeeze()
        return velocity

    def traveled_distance(self):
        """ Calculate the travel distance

        Note that Nans are linearly interpolated
        """
        # We remove nans between section
        # and then calculate the velocity
        # it is equivalent to interpolate between non-nan blocks
        subtraj = self.location.dropna().reset_index().drop('index', axis=1)
        if subtraj.dropna().shape[0] < 2:
            print('Trajectory has less than 2 non nans points')
            return np.nan
        # only location is of relevance
        velocity = subtraj.astype(float).diff()
        speed = np.sqrt(velocity.x**2 + velocity.y**2 + velocity.z**2)
        travel_dist = np.sum(speed)
        return travel_dist

    def sinuosity(self, shortest_dist=None):
        """ Calculate the sinosity
        Sinusity is defined as:
              Travelled distance
           S=--------------------
               Shortest distance

        Note that Nans are linearly interpolated

        :param shortest_dist: Assign shortest distance (default\
 None the shortest distance is equal to the bee line between \
first and last no-nan point.
        """
        travel_dist = self.traveled_distance()
        if shortest_dist is None:
            # we need to calculate the shortest distance
            # assuming the direct line
            firstpoint = self.location.dropna().iloc[0, :]
            lastpoint = self.location.dropna().iloc[-1, :]
            shortest_dist = lastpoint-firstpoint
            shortest_dist = np.sqrt(
                shortest_dist.x**2 + shortest_dist.y**2 + shortest_dist.z**2)
        # sanity check
        # the travelled distance can not be shorter than the shortest distance
        if shortest_dist > travel_dist:
            msg = "Travel distance is shorter than the shortest distance"
            msg += "\n {}>{}".format(shortest_dist, travel_dist)
            raise NameError(msg)
        return travel_dist/shortest_dist
    # --------------------------------------------
    # ---------------- FILTER --------------------
    # --------------------------------------------

    def filtfilt(self, order, cutoff, padlen=None):
        """
        Filter the trajectory with order and cutoff by
        using a lowpass filter twice (forward and backward)
        to correct for phase shift

        :param order: the order of the lowpass filter. Either a number \
or a pandas series. The series should be multiindexed as the columns of \
the trajectory.
        :param cutoff: cut off frequency in Hz if sampling rate is known\
otherwise relative to the Nyquist frequency. Either a number or a pandas \
series.
        """
        if self.sampling_rate > 0:
            nyquist = self.__sampling_rate / 2
            cutoff /= nyquist
        if isinstance(order, (int, float)):
            order = pd.Series(data=order, index=self.columns)
        if isinstance(cutoff, (int, float)):
            cutoff = pd.Series(data=cutoff, index=self.columns)
        subtraj = self.consecutive_blocks()
        for trajno_nan in subtraj:
            indeces = trajno_nan.index
            for col in self.columns:
                b, a = signal.butter(order.loc[col], cutoff.loc[col])
                if padlen is None:
                    padlen = 3 * max(len(a), len(b))
                if trajno_nan.shape[0] <= padlen:
                    self.loc[indeces, col] *= np.nan
                else:
                    if col[0] == 'location':
                        self.loc[indeces, col] = signal.filtfilt(
                            b, a,
                            trajno_nan.loc[:, col],
                            padlen=padlen).astype(float)
                    else:
                        self.loc[indeces, col] = signal.filtfilt(
                            b, a,
                            np.unwrap(trajno_nan.loc[:, col]),
                            padlen=padlen).astype(float)

    def fillna(self, method='Cubic'):
        """ fillna with a given method
        """
        customs_method = ['Cubic']
        if not (method in customs_method):
            # fall back to pandas fillna function
            return self.fillna(method)
        # Start implementing customs_method
        if method == 'Cubic':
            for col in self.loc[:, 'location'].columns:
                values = self.loc[:, ('location', col)]
                validtime = values.dropna().index
                validvalues = values.dropna().values
                cs = CubicSpline(validtime, validvalues)
                time = self.index
                self.loc[:, ('location', col)] = cs(time)
            # for the angles we first do a ffill and then
            # unwrap and interpolate on the unwrap angles
            rotconv = self.rotation_mode
            for col in self.loc[:, rotconv].columns:
                values = self.loc[:, (rotconv, col)]
                validtime = values.dropna().index
                unwrapvalues = np.unwrap(values.fillna(method='ffill'))
                validvalues = unwrapvalues[validtime]
                cs = CubicSpline(validtime, validvalues)
                time = self.index
                self.loc[:, (rotconv, col)] = cs(time)
            return self

        else:
            msg = 'Method {} is not supported.'
            msg += 'please use method supported by pd.fillna'
            msg += ' or one of the following methods {}'
            msg = msg.format(method, customs_method)
            raise NameError(msg)

    # --------------------------------------------
    # ---------------- EXTRACT -------------------
    # --------------------------------------------

    def consecutive_blocks(self):
        """ Return a list of subtrajectory withtout nans
        """
        # get a numpy array from the trajectory,
        # because we are using numpy arrays later
        np_traj = self.values
        np_traj = np.hstack([self.index[:, np.newaxis], np_traj])
        # Look for row containing at least one nan
        nonans = np.any(np.isnan(np_traj), axis=1)
        # spliting the trajectory according to nan location
        events = np.split(np_traj, np.where(nonans)[0])

        # removing NaN entries
        events = [ev[~np.any(np.isnan(ev), axis=1)]
                  for ev in events if isinstance(ev, np.ndarray)]
        # removing empty DataFrames
        subtraj = [Trajectory().from_dataframe(self.loc[ev[:, 0]])
                   for ev in events if ev.size > 0]
        return subtraj
    # -------------------------------------------
    # ---------------- PLOTS --------------------
    # -------------------------------------------

    def lollipops(self, ax=None,
                  colors=None, step_lollipop=1,
                  offset_lollipop=0, lollipop_marker='o',
                  linewidth=1, lollipop_tail_width=1, lollipop_tail_length=1,
                  lollipop_head_size=1, stickdir='backward',
                  plotcoords=['x', 'y', 'z']
                  ):
        """ lollipops plot

        create a lollipop plot for the trajectory with its associated \
        direction. Handels missing frames by leaving
        gaps in the lollipop plot. However indices of the colors, trajectory

        **Note** Gap in the index of the trajectory dataframe, will \
        lead to gap in the plotted trajectory and the color bar will \
        therefore miss some values (otherwise the color-coded frames \
        will not be linear)

        :param ax: is a matplotlib axes with 3d projection
        :param trajectory: is a pandas dataframe with columns \
                    ['x','y','z', 'euler_0','euler_1','euler_2']
        :param euler_axes: the axes rotation convention \
                    (see homogenous.transformations for details)
        :param colors: is a pandas dataframe with columns \
                       ['r','g','b','a'] and indexed as trajectory. \
                       (default: time is color coded)
        :param step_lollipop: number of frames between two lollipops
        :param offset_lollipop: the first lollipop to be plotted
        :param lollipop_marker: the head of the lollipop
        :param linewidth: The width of the line connecting lollipops
        :param lollipop_tail_width: The width of the lollipop stick
        :param lollipop_tail_length: The length of the lollipop stick
        :param lollipop_head_size: The size of the lollipop
        :param stickdir: The direction of the stick of the animal \
(backward or forward)
        :param plotcoords: the dimension to plots, e.g. ['x','y','z'] for 3d plots \
['x','y'] for a 2d plot
        """
        # import time
        t_start = time.time()
        if ax is None:
            if len(plotcoords) == 3:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
            elif len(plotcoords) == 2:
                fig = plt.figure()
                ax = fig.add_subplot(111)
        if (len(plotcoords) != 2) and (len(plotcoords) != 3):
            msg = 'plotcoords need to contains 2 or 3 elements'
            msg += ' for 2d and 3d plots respectively'
            raise ValueError(msg)
        if ax.name == '3d':
            plotcoords = ['x', 'y', 'z']
        elif len(plotcoords) > 2:
            plotcoords = plotcoords[:2]

        # Start computing for direction
        direction = self.facing_direction()
        if colors is None:
            timeseries = pd.Series(data=self.index,
                                   index=self.index)
            colors, sm = get_color_dataframe(timeseries)
        # Create a continuous index from trajectory
        frames = np.arange(self.index.min(), self.index.max() + 1)
        # Select indeces to save time
        indeces = frames[offset_lollipop::step_lollipop]
        # Calculate agent tail direction
        # use function in trajectory to get any point bodyref to worldref
        tailmarker = pd.Series(data=0,
                               index=pd.MultiIndex.from_product(
                                   [[0],
                                    ['x', 'y', 'z']]))
        if stickdir == 'forward':
            tailmarker.loc[0, 'x'] = lollipop_tail_length
        else:
            tailmarker.loc[0, 'x'] = -lollipop_tail_length
        tail = self.body2world(tailmarker, indeces=indeces)
        tail = tail.loc[:, 0]
        # Plot the agent trajectory
        # - loop through consecutive point
        # - Two consecutive point are associated with the color
        # of the first point
        x = self.loc[:, ('location', 'x')]
        y = self.loc[:, ('location', 'y')]
        z = self.loc[:, ('location', 'z')]
        print(time.time() - t_start)
        t_start = time.time()
        line = dict()
        line['x'] = self.x
        line['y'] = self.y
        line['z'] = self.z
        if isinstance(colors, pd.DataFrame):
            # Each segment will be plotted with a different color
            # we therefore need to loop through all points
            # in the trajectory, a rather long process
            for frame_i, frame_j in zip(frames[:-1], frames[1:]):
                # Frames may be missing in trajectory,
                # and therefore can not be plotted
                if (frame_i in self.index) and \
                   (frame_j in self.index) and \
                   (frame_i in self.index):
                    color = [colors.r[frame_i], colors.g[frame_i],
                             colors.b[frame_i], colors.a[frame_i]]
                    # Create the line to plot
                    line['x'] = [x[frame_i], x[frame_j]]
                    line['y'] = [y[frame_i], y[frame_j]]
                    line['z'] = [z[frame_i], z[frame_j]]
                    # Actual plot command
                    if len(plotcoords) == 3:
                        ax.plot(xs=line['x'], ys=line['y'], zs=line['z'],
                                color=color, linewidth=linewidth)
                    else:
                        # len(plotcoords) == 2 because check earlier
                        ax.plot(line[plotcoords[0]], line[plotcoords[1]],
                                color=color, linewidth=linewidth)

        else:
            # Actual plot command
            if len(plotcoords) == 3:
                ax.plot(xs=line['x'], ys=line['y'], zs=line['z'],
                        color=colors, linewidth=linewidth)
            else:
                # len(plotcoords) == 2 because check earlier
                ax.plot(line[plotcoords[0]], line[plotcoords[1]],
                        color=colors, linewidth=linewidth)
        print(time.time() - t_start)
        t_start = time.time()
        # Plot the lollipop
        # - loop through the frames with a step of step_lollipop
        # - The lollipop is colored with the color of this frame
        # - Each lollipop is composed of a marker,
        # a point on the agent trajectory
        #   and a line representing the body (anti facing direction)
        for frame_i in indeces:
            # Frames may be missing in trajectory,
            # and therefore can not be plotted
            if (frame_i in self.index) and  \
                    (frame_i in direction.index):
                if isinstance(colors, pd.DataFrame):
                    if frame_i not in colors.index:
                        continue
                    color = [colors.r[frame_i], colors.g[frame_i],
                             colors.b[frame_i], colors.a[frame_i]]
                else:
                    color = colors
                # Create the line to plot
                line['x'] = [self.x[frame_i],
                             tail.x[frame_i]]
                line['y'] = [self.y[frame_i],
                             tail.y[frame_i]]
                line['z'] = [self.z[frame_i],
                             tail.z[frame_i]]
                # Actual plot command
                if len(plotcoords) == 3:
                    ax.plot(xs=line['x'], ys=line['y'], zs=line['z'],
                            color=color, linewidth=lollipop_tail_width)
                    ax.plot(xs=[line['x'][0]],
                            ys=[line['y'][0]],
                            zs=[line['z'][0]],
                            color=color,
                            marker=lollipop_marker,
                            markersize=lollipop_head_size)
                else:
                    # len(plotcoords) == 2 because check earlier
                    ax.plot(line[plotcoords[0]], line[plotcoords[1]],
                            color=color, linewidth=lollipop_tail_width)
                    ax.plot([line[plotcoords[0]][0]],
                            [line[plotcoords[1]][0]],
                            color=color,
                            marker=lollipop_marker,
                            markersize=lollipop_head_size)
        print(time.time() - t_start)
