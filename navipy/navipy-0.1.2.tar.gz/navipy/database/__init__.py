"""

"""

import os
import numpy as np
import pandas as pd
import sqlite3
import io
from navipy.scene import is_numeric_array, check_scene
from navipy.maths import constants as mconst
from navipy.trajectories import Trajectory
from navipy.trajectories import posorient_columns
import logging
import numbers


def adapt_array(arr):
    """
    http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
    """
    if arr is None:
        raise ValueError('array must not be None')
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


def convert_array(text):
    if text is None:
        raise ValueError('text must not be None')
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


# Converts np.array to TEXT when inserting
sqlite3.register_adapter(np.ndarray, adapt_array)
# Converts TEXT to np.array when selecting
sqlite3.register_converter("array", convert_array)


class DataBase():
    """DataBase
    It creates three sql table on initialisation.
    """
    __float_tolerance = 1e-14

    def __init__(self, filename, mode='a',
                 channels=['R', 'G', 'B', 'D'], arr_dtype=np.uint8):
        """Initialisation of the database
        the first database is the image database to store the images
        the second database is the position_orientation database to
        store the position and orientations of the corresponding image
        the third database is the normalisation database that stores the
        ranges of the images.
        :param filename: filename of the database to be loaded, stored
                         created
               channels: channels for the images (Red,Green,Blue,Distance)
        :type filename: string
              channels: list
        """
        self._logger = logging.getLogger('navipy')
        self.__convention = None
        if not isinstance(filename, str):
            msg = 'filename should be a string'
            self._logger.exception(msg)
            raise TypeError(msg)
        _, ext = os.path.splitext(filename)
        if ext != '.db' and (filename != ':memory:'):
            msg = 'filename must have the .db extension'
            self._logger.exception(msg)
            raise NameError(msg)
        # We try to determine if we need to load or create
        # the database
        if (not os.path.exists(filename)) and mode == 'r':
            # The file does not exist, and we want to read
            # it. This is not possible
            msg = 'Cannot read database {}'
            msg = msg.format(filename)
            self._logger.exception(msg)
            raise NameError(msg)
        elif mode == 'w':
            # The file exist, and we want to write it
            # We need to create the database
            self._logger.info('WriteRead-mode')
            self.arr_dtype = arr_dtype
        elif mode == 'a':
            self._logger.info('AppendRead-mode')
            self.arr_dtype = arr_dtype
        else:
            # The file exist, and we want to either
            # write it or append data to it.
            # We need to load the database
            self._logger.info('ReadOnly-mode')
        self.mode = mode

        if not isinstance(channels, list):
            msg = 'nb_channel should be a list or np array'
            self._logger.exception(msg)
            raise TypeError(msg)
        for c in channels:
            if c is None:
                msg = 'channels must not be None'
                self._logger.exception(msg)
                raise ValueError(msg)
            if c is np.nan:
                msg = 'channels must not be of nan value'
                self._logger.exception(msg)
                raise ValueError(msg)
            if isinstance(c, list) or isinstance(c, np.ndarray):
                msg = 'channels must be single value'
                self._logger.exception(msg)
                raise ValueError(msg)
            if c not in ['R', 'G', 'B', 'D']:
                msg = 'channels must be either\
                                  R,G,B or D (Distance)'
                self._logger.exception(msg)
                raise ValueError(msg)
        self._logger.debug('database\nfilename: {}\nchannel: {}'.format(
            filename, channels))
        self.filename = filename
        self.channels = channels
        self.normalisation_columns = list()
        for chan_n in self.channels:
            self.normalisation_columns.append(str(chan_n) + '_max')
            self.normalisation_columns.append(str(chan_n) + '_min')
            self.normalisation_columns.append(str(chan_n) + '_range')

        self.tablecolumns = dict()
        self.tablecolumns['position_orientation'] = dict()
        self.tablecolumns['position_orientation']['x'] = 'real'
        self.tablecolumns['position_orientation']['y'] = 'real'
        self.tablecolumns['position_orientation']['z'] = 'real'
        self.tablecolumns['position_orientation']['q_0'] = 'real'
        self.tablecolumns['position_orientation']['q_1'] = 'real'
        self.tablecolumns['position_orientation']['q_2'] = 'real'
        self.tablecolumns['position_orientation']['q_3'] = 'real'
        self.tablecolumns['position_orientation']['frame_i'] = 'real'
        self.tablecolumns['position_orientation']['rotconv_id'] = 'string'
        self.tablecolumns['viewing_directions'] = dict()
        self.tablecolumns['viewing_directions']['data'] = 'array'
        self.tablecolumns['image'] = dict()
        self.tablecolumns['image']['data'] = 'array'
        self.tablecolumns['normalisation'] = dict()
        for col in self.normalisation_columns:
            self.tablecolumns['normalisation'][col] = 'real'

        if (self.mode in ['a', 'r']) and (os.path.exists(filename)):
            self._logger.info('Connect to database')

            self.db = sqlite3.connect(
                'file:' + filename + '?cache=shared', uri=True,
                detect_types=sqlite3.PARSE_DECLTYPES,
                timeout=10)
            self.db_cursor = self.db.cursor()
            # Check table
            self._logger.debug('Check tables')
            for tablename, _ in self.tablecolumns.items():
                if not self.table_exist(tablename):
                    msg = '{} does not contain a table\
                                    named {}'.format(filename, tablename)
                    self._logger.exception(msg)
                    raise Exception(msg)
        else:
            self._logger.info('Create database')
            self.db = sqlite3.connect(
                'file:' + filename + '?cache=shared', uri=True,
                detect_types=sqlite3.PARSE_DECLTYPES,
                timeout=10)
            self.db_cursor = self.db.cursor()
            # Create table
            self._logger.info('Create tables')
            for key, val in self.tablecolumns.items():
                columns = "(id integer primary key autoincrement"
                for colname, coltype in val.items():
                    columns += ' , ' + colname + ' ' + coltype
                columns += ')'
                self.db_cursor.execute(
                    "create table {} {}".format(key, columns))
            self.db.commit()
        self.__nbaz = None
        self.__nbel = None
        self.__viewing_dir = None

    @property
    def viewing_directions(self):
        if self.__viewing_dir is None:
            rowid = 1
            tablename = 'viewing_directions'
            self.db_cursor.execute(
                """
                SELECT data
                FROM {}
                WHERE (rowid=?)
                """.format(tablename), (rowid,))
            self.__viewing_dir = self.db_cursor.fetchone()[0]
            self.__viewing_dir = np.round(self.__viewing_dir, decimals=3)
        return self.__viewing_dir.copy()

    @viewing_directions.setter
    def viewing_directions(self, viewdir):
        """Get the viewing direction from images

        :param az_lim: (min,max) of the azimuth angles
        :param el_lim: (min,max) of the elevation angles
        :returns: viewing direction of every pixels
        :rtype: np.array

        """
        if self.__viewing_dir is None:
            msg = 'write viewing direction'
            self._logger.info(msg)
            if isinstance(viewdir, np.ndarray):
                tablename = 'viewing_directions'
                params = dict()
                params['rowid'] = 1
                params['data'] = viewdir
                self.insert_replace(tablename, params)
            else:
                msg = 'viewdir should be a numpy nd.array'
                msg += ' and not {}'.format(type(viewdir))
                self._logger.exception(msg)
                raise TypeError(msg)
        else:
            msg = 'viewing direction has already been set'
            self._logger.exception(msg)
            raise Exception(msg)

    def table_exist(self, tablename):
        """
        checks wether a table with name tablename exists in the database
        :param tablename: name of the table
        :type tablename: string
        :returns: validity
        :rtype: boolean
        """
        if not isinstance(tablename, str):
            msg = 'tablename should be a string'
            self._logger.exception(msg)
            raise TypeError(msg)
        self.db_cursor.execute(
            """
            SELECT count(*)
            FROM sqlite_master
            WHERE type='table' and name=?;
            """, (tablename,))
        return bool(self.db_cursor.fetchone())

    def check_data_validity(self, rowid):
        """
        checks wether all three tables in the database
        (images,position_orientation, normalisation) contain
        an entry with the given id.
        :param rowid: id to be checked
        :type rowid: int
        :returns: validity
        :rtype: boolean
        """
        if not isinstance(rowid, int):
            msg = 'rowid must be an integer'
            self._logger.exception(msg)
            raise TypeError(msg)
        if rowid <= 0:
            msg = 'rowid must be greater zero'
            self._logger.exception(msg)
            raise ValueError(msg)
        if rowid is np.nan:
            msg = 'rowid must not be nan'
            self._logger.exception(msg)
            raise ValueError(msg)
        self.db_cursor.execute(
            """
            SELECT count(*)
            FROM position_orientation
            WHERE rowid=?;
            """, (rowid,))
        valid = bool(self.db_cursor.fetchone()[0])
        self.db_cursor.execute(
            """
            SELECT count(*)
            FROM normalisation
            WHERE rowid=?;
            """, (rowid,))
        valid = valid and bool(self.db_cursor.fetchone()[0])
        self.db_cursor.execute(
            """
            SELECT count(*)
            FROM image
            WHERE rowid=?;
            """, (rowid,))
        valid = valid and bool(self.db_cursor.fetchone()[0])
        return valid

    def get_posid(self, posorient):
        """
        returns the id of a given position and orientation
        in the database
        :param posorient: position and orientation
             is a 1x6 vector containing:
             *in case of euler angeles the index should be
              ['location']['x']
              ['location']['y']
              ['location']['z']
              [convention][alpha_0]
              [convention][alpha_1]
              [convention][alpha_2]
             **where convention can be:
               xyz, xzy, yxz, yzx, zyx, zxy
             *in case of quaternions the index should be
              ['location']['x']
              ['location']['y']
              ['location']['z']
              [convention]['q_0']
              [convention]['q_1']
              [convention]['q_2']
              [convention]['q_3']
             **where convention can be:
               quaternion
        :type posorient: pd.Series
        :returns: id
        :rtype: int
        """
        if not isinstance(posorient, pd.Series):
            msg = 'posorient should be a pandas Series'
            self._logger.exception(msg)
            raise TypeError(msg)
        if posorient.empty:
            msg = 'position must not be empty'
            self._logger.exception(msg)
            raise Exception(msg)
        found_convention = False
        index = posorient.index
        if not isinstance(posorient.name, numbers.Number):
            msg = 'posorient.name should give the frame #\n'
            msg += ' posorient.name: {}\n'.format(posorient.name)
            msg += ' type(posorient.name): {}'.format(type(posorient.name))
            self._logger.exception(msg)
            raise Exception(msg)
        frame_i = posorient.name

        if isinstance(index, pd.MultiIndex):
            convention = index.levels[0][-1]
        else:
            msg = 'Old database without convention column'
            self._logger.warnings(msg)
            convention = 'xyz'
        if (convention in mconst._AXES2TUPLE.keys()) or \
           convention == 'quaternion':
            found_convention = True
        if not found_convention:
            msg = 'convention for rotation {} is not suppored\n'
            msg += msg.format(convention)
            msg += 'the following convention are supported\n:'
            for rconv in mconst._AXES2TUPLE.keys():
                msg += '{}\n'.format(rconv)
            msg += 'quaternion\n'
            self._logger.exception(msg)
            raise KeyError(msg)
        index_2ndlevel = posorient.index.get_level_values(1)
        # Check that the posorient contains valid columns
        # The user may be using alpha_ or q_
        # and we therefore want to be able to handle both type
        for val in ['x', 'y', 'z']:
            if val not in index_2ndlevel:
                msg = 'missing index {}'.format(val)
                self._logger.exception(msg)
                raise ValueError(msg)
        naming_map = list()
        for ii in range(3):
            if ('alpha_{}'.format(ii) not in index_2ndlevel) and \
               ('q_{}'.format(ii) not in index_2ndlevel):
                msg = 'missing index alpha_{0: } or q_{0: }'.format(ii)
                self._logger.exception(msg)
                raise ValueError(msg)
            elif ('alpha_{}'.format(ii) in index_2ndlevel) and \
                 ('q_{}'.format(ii) in index_2ndlevel):
                msg = 'posorient should contains either alphas or qs'
                self._logger.exception(msg)
                raise ValueError(msg)
            elif ('alpha_{}'.format(ii) in index_2ndlevel):
                naming_map.append('alpha_{}'.format(ii))
            else:
                naming_map.append('q_{}'.format(ii))
        if convention == 'quaternion':
            if 'q_3' not in index_2ndlevel:
                msg = 'missing index q_3'
                self._logger.exception(msg)
                raise ValueError(msg)
            else:
                naming_map.append('q_{}'.format(3))
        else:
            # q_3 is unnecessary for convention
            # different than quaternion. The value
            # should be set to nan, and wil therefore block during check of
            # any nan. We drop it now.
            if 'q_3' in index_2ndlevel:
                posorient.drop((convention, 'q_3'), inplace=True)
        if np.any(pd.isnull(posorient)):
            msg = 'posorient must not contain nan\n {}'.format(posorient)
            self._logger.exception(msg)
            raise ValueError(msg)
        where = ""
        where += """x>=? and x<=?"""
        where += """and y>=? and y<=?"""
        where += """and z>=? and z<=?"""
        where += """and q_0>=? and q_0<=?"""
        where += """and q_1>=? and q_1<=?"""
        where += """and q_2>=? and q_2<=?"""
        where += """and rotconv_id =?"""
        where += """and frame_i = ?"""
        params = (
            posorient['location']['x'] - self.__float_tolerance,
            posorient['location']['x'] + self.__float_tolerance,
            posorient['location']['y'] - self.__float_tolerance,
            posorient['location']['y'] + self.__float_tolerance,
            posorient['location']['z'] - self.__float_tolerance,
            posorient['location']['z'] + self.__float_tolerance,
            posorient[convention][naming_map[0]] - self.__float_tolerance,
            posorient[convention][naming_map[0]] + self.__float_tolerance,
            posorient[convention][naming_map[1]] - self.__float_tolerance,
            posorient[convention][naming_map[1]] + self.__float_tolerance,
            posorient[convention][naming_map[2]] - self.__float_tolerance,
            posorient[convention][naming_map[2]] + self.__float_tolerance,
            convention,
            frame_i)
        if convention == 'quaternion':
            where += """and q_3>=? and q_3<=?"""
            params = params + (
                posorient[convention][naming_map[3]] - self.__float_tolerance,
                posorient[convention][naming_map[3]] + self.__float_tolerance)
        self.db_cursor.execute(
            """
            SELECT count(*)
            FROM position_orientation
            WHERE {};""".format(where), params)
        exist = self.db_cursor.fetchone()[0]  # [0] because of tupple
        if bool(exist):
            self.db_cursor.execute(
                """
                SELECT rowid
                FROM position_orientation
                WHERE {};
                """.format(where), params)
            return self.db_cursor.fetchone()[0]
        elif (self.mode in ['a', 'w']):
            if convention != 'quaternion':
                self.db_cursor.execute(
                    """
                    INSERT
                    INTO position_orientation(x,y,z,q_0,q_1,q_2,q_3,rotconv_id,frame_i)
                    VALUES (?,?,?,?,?,?,?,?,?)
                    """, (
                        posorient['location']['x'],
                        posorient['location']['y'],
                        posorient['location']['z'],
                        posorient[convention]['alpha_0'],
                        posorient[convention]['alpha_1'],
                        posorient[convention]['alpha_2'],
                        np.nan,
                        convention, frame_i))
            else:
                self.db_cursor.execute(
                    """
                    INSERT
                    INTO position_orientation(x,y,z,q_0,q_1,q_2,rotconv_id,frame_i)
                    VALUES (?,?,?,?,?,?,?,?,?)
                    """, (
                        posorient['location']['x'],
                        posorient['location']['y'],
                        posorient['location']['z'],
                        posorient[convention]['q_0'],
                        posorient[convention]['q_1'],
                        posorient[convention]['q_2'],
                        posorient[convention]['q_3'],
                        convention, frame_i))
            rowid = self.db_cursor.lastrowid
            self.db.commit()
            return rowid
        else:
            msg = 'posorient not found \n {} \n {} \n {}'.format(
                posorient, where, params)
            self._logger.exception(msg)
            raise ValueError(msg)

    def iter_posorients(self):
        """Iter through all position orientation in the database
        """
        self.db_cursor.execute(
            """
                SELECT *
                FROM position_orientation
                """)

        columns_names = []
        for col in self.db_cursor.description:
            columns_names.append(col[0])
        for row in self.db_cursor:
            toyield = pd.Series(data=row, index=columns_names)
            toyield.name = toyield.id
            toyield.drop('id', inplace=True)
            yield toyield
    #
    # Access to single values
    #

    @property
    def rotation_convention(self):
        """ Return the convention of the database

        The database can technically contains more than one convention.
        Although it is discourage to do so, it is not forbidden.

        If more than one convention is found in the database, this function
        will issue awarning when more than one convention is present in the database.
        """
        posorient = pd.read_sql_query(
            "select * from position_orientation;", self.db)
        posorient.set_index('id', inplace=True)
        if self.__convention is None:
            # we need to assign it from the posorient
            if 'rotconv_id' in posorient.columns:
                rotconv = posorient.loc[:, 'rotconv_id']
                if np.all(rotconv == rotconv.iloc[0]):
                    self.__convention = rotconv.iloc[0]
                else:
                    self._logger.warning(
                        'More than one convention have been found in database')
                    self.__convention = None
            else:
                self._logger.warning("you are loading a database with old\
                                   conventions, it will be transformed\
                                   automatically into the new one")
                self.__convention = 'xyz'
        return self.__convention

    @property
    def posorients(self, indexby='frame_i'):
        """Return the position orientations of all points in the \
        database
        :params indexby: index posorients by 'frame_i' (default) or 'id'
        :returns: all position orientations
        :rtype: list of pd.Series
        """
        posorient = pd.read_sql_query(
            "select * from position_orientation;", self.db)
        if indexby in posorient.columns:
            posorient.set_index('frame_i', inplace=True)
        else:  # Handle older db version
            print('Could not index by {}'.format(indexby))
            posorient.set_index('id', inplace=True)
        if self.rotation_convention is not None:
            posorients = Trajectory()
            posorients.from_dataframe(posorient, rotconv=self.__convention)
        return posorients.astype(float)

    @property
    def normalisations(self):
        """Returns the normalised scenes of all points in the \
        database
        :returns: all position orientations
        :rtype: list of pd.Series
        """
        normal = pd.read_sql_query(
            "select * from normalisation;", self.db)
        normal.set_index('id', inplace=True)
        return normal

    #
    # Read from database
    #
    def read_posorient(self, posorient=None, rowid=None):
        """Read posorient with a given posorient or rowid

        :param posorient: pd.Series with MuliIndex
        :param rowid: integer, rowid of the database
        :returns: return posorient
        :rtype: pd.Series

        """
        if rowid is not None:
            if not isinstance(rowid, int):
                msg = 'rowid must be an integer'
                self._logger.exception(msg)
                raise TypeError(msg)
            if rowid <= 0:
                msg = 'rowid must be greater zero'
                self._logger.exception(msg)
                raise ValueError(msg)
            if rowid is np.nan:
                msg = 'rowid must not be nan'
                self._logger.exception(msg)
                raise ValueError(msg)
        if (posorient is None) and (rowid is None):
            msg = 'posorient and rowid can not be both None'
            self._logger.exception(msg)
            raise Exception(msg)
        if posorient is not None:
            rowid = self.get_posid(posorient)
        # Read pososition porientation
        tablename = 'position_orientation'
        toreturn = pd.read_sql_query(
            """
                SELECT *
                FROM {}
                WHERE (rowid={})
                """.format(tablename, rowid), self.db)
        toreturn = toreturn.loc[0, :]
        # if np.isnan(toreturn.frame)
        toreturn.name = toreturn.frame_i
        # toreturn.drop('id')
        # toreturn = toreturn.astype(float)
        posorient = None
        convention = toreturn.rotconv_id

        tuples = posorient_columns(convention)
        index = pd.MultiIndex.from_tuples(tuples)
        posorient = pd.Series(index=index)
        posorient['location']['x'] = toreturn.loc['x']
        posorient['location']['y'] = toreturn.loc['y']
        posorient['location']['z'] = toreturn.loc['z']

        if convention != 'quaternion':
            posorient[convention]['alpha_0'] = toreturn.loc['q_0']
            posorient[convention]['alpha_1'] = toreturn.loc['q_1']
            posorient[convention]['alpha_2'] = toreturn.loc['q_2']
            posorient.name = toreturn.name
        else:
            posorient[convention]['q_0'] = toreturn.loc['q_0']
            posorient[convention]['q_1'] = toreturn.loc['q_1']
            posorient[convention]['q_2'] = toreturn.loc['q_2']
            posorient[convention]['q_3'] = toreturn.loc['q_3']
            posorient.name = toreturn.name

        return posorient.astype(float)

    def scene(self, posorient=None, rowid=None):
        """Read an image at a given position-orientation or given id of row in the \
        database.
        :param posorient: is a 1x6 vector containing:
             *in case of euler angeles the index should be
              ['location']['x']
              ['location']['y']
              ['location']['z']
              [convention][alpha_0]
              [convention][alpha_1]
              [convention][alpha_2]
             **where convention can be:
               xyz, xzy, yxz, yzx, zyx, zxy
             *in case of quaternions the index should be
              ['location']['x']
              ['location']['y']
              ['location']['z']
              [convention]['q_0']
              [convention]['q_1']
              [convention]['q_2']
              [convention]['q_3']
             **where convention can be:
               quaternion
        :param rowid: an integer
        :returns: an image
        :rtype: numpy.ndarray
        """
        if rowid is not None:
            if not isinstance(rowid, int):
                msg = 'rowid must be an integer'
                self._logger.exception(msg)
                raise TypeError(msg)
            if rowid <= 0:
                msg = 'rowid must be greater zero'
                self._logger.exception(msg)
                raise ValueError(msg)
            if rowid is np.nan:
                msg = 'rowid must not be nan'
                self._logger.exception(msg)
                raise ValueError(msg)
            if (posorient is None) and (rowid is None):
                msg = 'posorient and rowid can not be both None'
                self._logger.exception(msg)
                raise Exception(msg)
            if posorient is not None:
                rowid = self.get_posid(posorient)
        if (posorient is None) and (rowid is None):
            msg = 'posorient and rowid can not be both None'
            self._logger.exception(msg)
            raise Exception(msg)
        if posorient is not None:
            rowid = self.get_posid(posorient)
        # Read images
        tablename = 'image'
        self.db_cursor.execute(
            """
                SELECT data
                FROM {}
                WHERE (rowid=?)
                """.format(tablename), (rowid,))
        image = self.db_cursor.fetchone()[0]
        # Check image size
        # and try to correct it whenever possible
        if not isinstance(image, np.ndarray):
            msg = 'image must be np.array'
            self._logger.exception(msg)
            raise TypeError(msg)
        if len(image.shape) > 3:
            if np.all(image.shape[3:] == np.ones_like(image.shape[3:])):
                image = image[:, :, :, 0]  # Other dim are useless
        if len(image.shape) != 3:
            msg = 'image should be 3D array'
            msg += 'image size is {}'.format(image.shape)
            self._logger.exception(msg)
            raise Exception(msg)
        # Read cmaxminrange
        tablename = 'normalisation'
        cmaxminrange = pd.read_sql_query(
            """
                SELECT *
                FROM {}
                WHERE (rowid={})
                """.format(tablename, rowid), self.db)
        if cmaxminrange.shape[0] != 1:
            msg = 'Error while reading normalisation factors'
            self._logger.exception(msg)
            raise Exception(msg)
        cmaxminrange = cmaxminrange.iloc[0, :]
        cmaxminrange.name = cmaxminrange.id
        cmaxminrange.drop('id')
        cmaxminrange = cmaxminrange.astype(float)
        toreturn = self.denormalise_image(image, cmaxminrange)
        toreturn = toreturn[..., np.newaxis]
        check_scene(toreturn)
        return toreturn
    #
    # Write
    #

    def insert_replace(self, tablename, params):
        if not isinstance(tablename, str):
            msg = 'table are named by string'
            self._logger.exception('table are named by string')
            raise TypeError(msg)
        if not isinstance(params, dict):
            msg = 'params should be dictionary columns:val'
            self._logger.exception(msg)
            raise TypeError(msg)
        params_list = list()
        columns_str = ''
        for key, val in params.items():
            columns_str += key + ','
            params_list.append(val)
        columns_str = columns_str[:-1]  # remove last comma
        if len(params_list) == 0:
            self._logger.warning('nothing to be done in {}'.format(tablename))
            return
        questionsmarks = '?'
        for _ in range(1, len(params_list)):
            questionsmarks += ',?'
        self._logger.info('Insert image')
        self.db_cursor.execute(
            """
            INSERT OR REPLACE
            INTO {} ({})
            VALUES ({})
            """.format(tablename,
                       columns_str,
                       questionsmarks),
            tuple(params_list)
        )
        self.db.commit()

    def write_image(self, posorient, image):
        """stores an image in the database. Automatically
        calculates the cminmax range from the image and
        channels.
        :param posorient: is a 1x6 vector containing:
             *in case of euler angeles the index should be
              ['location']['x']
              ['location']['y']
              ['location']['z']
              [convention][alpha_0]
              [convention][alpha_1]
              [convention][alpha_2]
             **where convention can be:
               xyz, xzy, yxz, yzx, zyx, zxy
             *in case of quaternions the index should be
              ['location']['x']
              ['location']['y']
              ['location']['z']
              [convention]['q_0']
              [convention]['q_1']
              [convention]['q_2']
              [convention]['q_3']
             **where convention can be:
               quaternion
        :param image: image to be stored
        :type image: np.ndarray
        :type posorient: pd.Series
        """
        normed_im, cmaxminrange = self.normalise_image(image, self.arr_dtype)
        rowid = self.get_posid(posorient)
        # Write image
        tablename = 'image'
        params = dict()
        params['rowid'] = rowid
        params['data'] = normed_im
        self.insert_replace(tablename, params)
        #
        tablename = 'normalisation'
        params = dict()
        params['rowid'] = rowid
        for chan_n in self.normalisation_columns:
            params[chan_n] = cmaxminrange.loc[chan_n]
        self.insert_replace(tablename, params)
    #
    # Image processing
    #

    def denormalise_image(self, image, cmaxminrange):
        """denomalises an image
        :param image: the image to be denormalised
        :param cmaxminrange: new range of the denormalised image
        :type image: np.ndarray
        :type cmaxminrange: pd.Series
        :returns: denormalised image
        :rtype: numpy.ndarray
        """
        if not isinstance(image, np.ndarray):
            msg = 'image must be np.array'
            self._logger.exception(msg)
            raise TypeError(msg)
        if len(image.shape) != 3:
            msg = 'image should be 3D array'
            self._logger.exception(msg)
            raise Exception(msg)
        if image.shape[2] != len(self.channels):
            msg = 'image does not have the required'
            msg += 'number of channels {}'.format(len(self.channels))
            self._logger.exception(msg)
            raise Exception(msg)
        if not isinstance(cmaxminrange, pd.Series):
            msg = 'cmaxminrange should be a pandas Series'
            self._logger.exception(msg)
            raise TypeError(msg)
        if cmaxminrange.empty:
            msg = 'cmaxminrange must not be empty'
            self._logger.exception(msg)
            raise Exception(msg)
        for chan_n in self.channels:
            if str(chan_n) + '_max' not in cmaxminrange.index:
                msg = 'cminmax range is missing index {}_max'
                msg = msg.format(chan_n)
                self._logger.exception(msg)
                raise ValueError(msg)
            if str(chan_n) + '_min' not in cmaxminrange.index:
                msg = 'cminmax range is missing index {}_min'
                msg = msg.format(chan_n)
                self._logger.exception(msg)
                raise ValueError(msg)
            if str(chan_n) + '_range' not in cmaxminrange.index:
                msg = 'cminmax range is missing index {}_range'
                msg = msg.format(chan_n)
                self._logger.exception(msg)
                raise ValueError(msg)
            if np.any(np.isnan(cmaxminrange.loc[str(chan_n) + '_max'])):
                msg = 'cmaxminrange contains nans'
                self._logger.exception(msg)
                raise ValueError(msg)
            if np.any(np.isnan(cmaxminrange.loc[str(chan_n) + '_min'])):
                msg = 'cmaxminrange contains nans'
                self._logger.exception(msg)
                raise ValueError(msg)
            if np.any(np.isnan(cmaxminrange.loc[str(chan_n) + '_range'])):
                msg = 'cmaxminrange contains nans'
                self._logger.exception(msg)
                raise ValueError(msg)
        denormed_im = np.zeros(image.shape, dtype=np.float)
        maxval_nim = np.iinfo(image.dtype).max
        #
        for chan_i, chan_n in enumerate(self.channels):
            cimage = image[:, :, chan_i].astype(float)
            cmax = cmaxminrange.loc[str(chan_n) + '_max']
            cmin = cmaxminrange.loc[str(chan_n) + '_min']
            crange = cmaxminrange.loc[str(chan_n) + '_range']
            cimage /= maxval_nim
            cimage *= crange
            cimage += cmin
            denormed_im[:, :, chan_i] = cimage
            if np.max(cimage) != cmax:
                msg = 'max cimage and max from cmaxminrange do not match'
                msg += '{}!={} in {}'.format(np.max(cimage),
                                             cmax, cmaxminrange.name)
                self._logger.warning(msg)
        return denormed_im

    def normalise_image(self, image, dtype=np.uint8):
        """normalises an image to a range between 0 and 1.
        :param image: image to be normalised
        :param dtype: type of the image (default: np.uint8)
        :type image: np.ndarray
        :returns: normalised image
        :rtype: np.ndarray
        """
        if not isinstance(image, np.ndarray):
            msg = 'image must be np.array'
            self._logger.exception(msg)
            raise TypeError(msg)
        if np.any(np.isnan(image)):
            msg = 'image must not contain nan values'
            self._logger.exception(msg)
            raise ValueError(msg)
        if image.shape[0] <= 0 or image.shape[1] <= 0:
            msg = 'image dimensions incorrect'
            self._logger.exception(msg)
            raise Exception(msg)
        if image.shape[2] != len(self.channels):
            msg = 'image channels number differs from\
                             given channel number'
            self._logger.exception(msg)
            raise Exception(msg)
        if not is_numeric_array(image):
            msg = 'scene is of non numeric type'
            self._logger.exception(msg)
            raise TypeError(msg)
        normed_im = np.zeros(image.shape, dtype=dtype)
        maxval_nim = np.iinfo(normed_im.dtype).max
        #
        columns = list()
        for chan_n in self.channels:
            columns.append(str(chan_n) + '_max')
            columns.append(str(chan_n) + '_min')
            columns.append(str(chan_n) + '_range')

        cmaxminrange = pd.Series(index=columns)
        for chan_i, chan_n in enumerate(self.channels):
            cimage = image[:, :, chan_i].astype(float)
            cmax = cimage.max()
            cmin = cimage.min()
            crange = cmax - cmin
            cimage -= cmin
            if np.isclose(crange, 0):
                # cimage should be equal to 0
                # so crange is irelevant we can assign it to 1
                crange = 1
            cimage /= crange
            cimage *= maxval_nim
            cimage = cimage.astype(normed_im.dtype)
            normed_im[:, :, chan_i] = cimage
            cmaxminrange.loc[str(chan_n) + '_max'] = cmax
            cmaxminrange.loc[str(chan_n) + '_min'] = cmin
            cmaxminrange.loc[str(chan_n) + '_range'] = crange
        check_scene(normed_im[..., np.newaxis])
        return normed_im, cmaxminrange
