
"""
Module holding DynaODBCConnector class.

Tools to load data from SQL to Dynizer via ODBC.

https://www.simba.com/resources/odbc/

"""

import datetime, decimal

import multiprocessing as mp

from dynapython.client import Client, Service

from dynagatewaytypes import action_pb2
from dynagatewaytypes import topology_pb2
from dynagatewaytypes import label_pb2
from dynagatewaytypes import instance_pb2
from dynagatewaytypes import enums_pb2
from dynagatewaytypes import general_types_pb2
from dynagatewaytypes import datatypes_pb2

from dynaodbc._dyna_odbc_const import _ErrFmts, _Keys
from dynaodbc.dyna_odbc_mapping import DataMapping, ActionMapping, QueryMapping
from dynaodbc.odbc_connection import ODBCConnection

class DynaODBCConnector:
    """
    DynaODBCConnector parameters and functions.

    Fields:
    - db_driver: ODBC driver to use
    - db_server: SQL server to connect to
    - db_database: SQL DB to use
    - db_username: SQL DB username
    - db_password: SQL DB password
    - dyn_server: Dynizer to connect to
    - dyn_username: Dynizer username
    - dyn_password: Dynizer password
    - query_mappings: Query mappings of connector

    Methods:
    - from_dict
    - from_json
    - connect
    - close
    - load_data

    """
    def __init__(self, db_driver, db_server, db_database, db_username, db_password,
        dyn_server, dyn_username, dyn_password, query_mappings):
        """
        Returns a new Connector

        Args:
        - db_driver: ODBC driver to use
        - db_server: SQL server to connect to
        - db_database: SQL DB to use
        - db_username: SQL DB username
        - db_password: SQL DB password
        - dyn_server: Dynizer to connect to
        - dyn_username: Dynizer username
        - dyn_password: Dynizer password
        - query_mappings: Query mappings of connector

        """
        if not isinstance(dyn_username, str):
            raise AttributeError(_ErrFmts.errmsg_invalid_dyn_username % dyn_username)

        if not isinstance(dyn_password, str):
            raise AttributeError(_ErrFmts.errmsg_invalid_dyn_password)

        self.db_driver = db_driver
        self.db_server = db_server
        self.db_database = db_database
        self.db_username = db_username
        self.db_password = db_password
        self.dyn_server = dyn_server
        self.dyn_username = dyn_username
        self.dyn_password = dyn_password
        self.query_mappings = query_mappings
        self._db_connection = None
        self._dyn_connection = None
        self._max_processes = 64

    @staticmethod
    def from_dict(dct, convert_functions={}):
        """
        Returns a new DynaODBCConnector from a dictionary

        Args:
        - dct: dictionary
        - convert_functions: optional custom convert functions

        Keys:
        - db_driver: ODBC driver to use
        - db_server: SQL server to connect to
        - db_database: SQL DB to use
        - db_username: SQL DB username
        - db_password: SQL DB password
        - dyn_server: Dynizer to connect to
        - dyn_username: Dynizer username
        - dyn_password: Dynizer password
        - query_mappings: Query mappings of connector

        """
        try:
            return DynaODBCConnector(
                dct[_Keys.db_driver],
                dct[_Keys.db_server],
                dct[_Keys.db_database],
                dct[_Keys.db_username],
                dct[_Keys.db_password],
                dct[_Keys.dyn_server],
                dct[_Keys.dyn_username],
                dct[_Keys.dyn_password],
                QueryMapping.from_dict(dct[_Keys.query_mappings], convert_functions=convert_functions)
            )
        except Exception as exc:
            raise AttributeError(_ErrFmts.errmsg_config % exc) from None

    @staticmethod
    def from_json(json_string, convert_functions={}):
        """
        Returns a new DynaODBCConnector from a json string.
        Calls DynaODBCConnector.from_dict
        """
        retval = None
        data = json.loads(json_string)
        retval = Connector.from_dict(data, convert_functions=convert_functions)
        return retval

    @staticmethod
    def create_convert_functions(*args):
        """
        Create convert function dictionary from functions.
        Functions will be mapped against their defined name.

        Args:
        - *args: functions to set in dictionary

        """
        convert_functions = {}
        for arg in args:
            convert_functions[arg.__name__] = arg
        return convert_functions

    @staticmethod
    def _detect_data_type(value):
        """
        Detects Dynizer data type
        """
        if isinstance(value, int):
            return enums_pb2.INTEGER
        if isinstance(value, str):
            return enums_pb2.STRING
        if isinstance(value, bool):
            return enums_pb2.BOOLEAN
        if isinstance(value, float):
            return enums_pb2.FLOAT
        if value is None:
            return enums_pb2.VOID

        raise AttributeError(_ErrFmts.errmsg_type_detect % value)

    def connect(self):
        """
        Connects to the SQL DB and Dynizer
        """
        try:
            # Connect to SQL DB
            self._db_connection = ODBCConnection(
                self.db_driver,
                self.db_server,
                self.db_database,
                self.db_username,
                self.db_password
            )

            self._db_connection.connect()

            # Connect to Dynizer
            connection_params = self.dyn_server.split(":", 1)

            if len(connection_params) == 1:
                connection_params.append(50022)
            else:
                connection_params[1] = int(connection_params[1])

            self._dyn_connection = Client(connection_params[0], connection_params[1])
            success = self._dyn_connection.user_login(self.dyn_username, self.dyn_password)
            if not success:
                raise AttributeError(_ErrFmts.errmsg_dyn_login % self.dyn_server)
        except Exception as exc:
            self.close()
            raise RuntimeError(_ErrFmts.errmsg_dyn_connect % exc) from None

    def close(self):
        """
        Closes the SQL DB and Dynizer connection
        """
        # TODO: Close dyn conn
        if self._db_connection is not None:
            self._db_connection.close()


    def load_data(self):
        """
        Load data from SQL DB to the Dynizer
        """
        for query_mapping in self.query_mappings:
            actions = []
            topologies = []
            labels = []
            action_topologies = {}

            for action_mapping in query_mapping.action_mappings:
                # Add action
                actions.append(action_pb2.CreateActionReq(
                        name = action_mapping.action_name
                    )
                )

                # Add topology
                components = []
                action_labels = []

                for i, data_mapping in enumerate(action_mapping.data_mappings):
                    components.append(data_mapping.component)

                    if data_mapping.label is not None:
                        action_labels.append(
                            general_types_pb2.LabelPosition(
                                label = data_mapping.label,
                                position = i + 1
                            )
                        )

                sequence = general_types_pb2.TopologySequence(
                    components = components
                )

                topology = topology_pb2.CreateTopologyReq(
                    sequence = sequence
                )

                topologies.append(topology)

                action_topologies[action_mapping.action_name] = sequence

                # Add labels
                if len(action_labels) != 0:
                    labels.append(
                        label_pb2.CreateLabelsReq(
                            name = action_mapping.action_name,
                            sequence = sequence,
                            labels = action_labels
                        )
                    )

            # Create actions
            it = self._dyn_connection.call(
                self._dyn_connection.service(Service.ACTION_SERVICE).Create,
                self._yield_objects(actions, "actions")
            )
            try:
                for r in it:
                    if r.HasField("error"):
                        raise RuntimeError(
                            _ErrFmts.errmsg_create_action % (
                            actions[r.stream_index], query_mapping.query_string, r.error)
                        )
            except Exception as exc:
                raise RuntimeError(
                    _ErrFmts.errmsg_create_action % (
                    actions, query_mapping.query_string, exc)
                ) from None

            # Create topologies
            it = self._dyn_connection.call(
                self._dyn_connection.service(Service.TOPOLOGY_SERVICE).Create,
                self._yield_objects(topologies, "topologies")
            )
            try:
                for r in it:
                    if r.HasField("error"):
                        raise RuntimeError(
                            _ErrFmts.errmsg_create_topology % (
                            topologies[r.stream_index], query_mapping.query_string, r.error)
                        )
            except Exception as exc:
                raise RuntimeError(
                    _ErrFmts.errmsg_create_topology % (
                    topologies, query_mapping.query_string, exc)
                ) from None

            # Create labels
            if len(labels) != 0:
                it = self._dyn_connection.call(
                    self._dyn_connection.service(Service.LABEL_SERVICE).Create,
                    self._yield_objects(labels, "labels")
                )
                try:
                    for r in it:
                        if r.HasField("error"):
                            raise RuntimeError(
                                _ErrFmts.errmsg_create_labels % (
                                labels[r.stream_index], query_mapping.query_string, r.error)
                            )
                except Exception as exc:
                    raise RuntimeError(
                        _ErrFmts.errmsg_create_labels % (
                        labels, query_mapping.query_string, exc)
                    ) from None

            # Execute query
            try:
                self._db_connection.cursor.execute(query_mapping.query_string)
            except Exception as exc:
                raise RuntimeError(
                    _ErrFmts.errmsg_db_execute % (
                    query_mapping.query_string, exc)
                ) from None

            row = self._db_connection.cursor.fetchone()

            # Create instances
            it = self._dyn_connection.call(
                self._dyn_connection.service(Service.INSTANCE_SERVICE).Create,
                self._yield_instances(
                    self._db_connection.cursor,
                    row,
                    action_topologies,
                    query_mapping
                )
            )
            try:
                for i, r in enumerate(it):
                    if r.HasField("error"):
                        raise RuntimeError(
                            _ErrFmts.errmsg_create_instance % (
                            r.stream_index, query_mapping.query_string, r.error)
                        )
            except Exception as exc:
                raise RuntimeError(
                    _ErrFmts.errmsg_create_instances % (
                    query_mapping.query_string, exc)
                ) from None

    @staticmethod
    def _load_data_p(db_conn):
        try:
            db_conn.connect()
            db_conn.load_data()
        except Exception as exc:
            db_conn.close()
            raise exc
        db_conn.close()

    def load_data_parallel(self):
        """
        Load data from SQL DB to the Dynizer in parallel.
        Starts a process for every query -> actions mapping.
        Opens and closes connections in each process.
        """
        p_len = len(self.query_mappings)
        if p_len > self._max_processes:
            p_len = self._max_processes

        db_conns = []

        for query_mapping in self.query_mappings:
            db_conns.append(DynaODBCConnector(
                self.db_driver,
                self.db_server,
                self.db_database,
                self.db_username,
                self.db_password,
                self.dyn_server,
                self.dyn_username,
                self.dyn_password,
                [query_mapping]
            ))

        with mp.Pool(processes = p_len) as p:
            results = p.map(self._load_data_p, [db_conn for db_conn in db_conns])

    @staticmethod
    def _yield_objects(objects, object_string):
        try:
            for object in objects:
                yield object
        except Exception as exc:
            msg = _ErrFmts.errmsg_yield_object % (
                object_string, query_mapping.query_string, exc)
            print(msg)
            ServicerContext.abort(StatusCode.ABORTED, msg)

    @staticmethod
    def _yield_instances(cursor, row, action_topologies, query_mapping):
        try:
            while row:
                for action_mapping in query_mapping.action_mappings:
                    # Create values
                    values = []

                    for data_mapping in action_mapping.data_mappings:
                        try:
                            converted_value = data_mapping.convert_function(
                                row[data_mapping.position - 1]
                            )
                        except Exception as exc:
                            raise RuntimeError(
                                _ErrFmts.errmsg_convert_fun % (
                                data_mapping.convert_function.__name__,
                                query_mapping.query_string,
                                action_mapping.action_name,
                                exc)
                            )

                        data_type = data_mapping.data_type
                        if data_type == enums_pb2.DT_NONE:
                            data_type = detect_data_type(converted_value)

                        # Handle NULL values
                        if converted_value is None:
                            data_type = enums_pb2.VOID

                        value = general_types_pb2.Value(
                            data_type = data_type,
                        )

                        if data_type == enums_pb2.INTEGER:
                            if isinstance(converted_value, decimal.Decimal):
                                converted_value = int(converted_value)
                            elif not isinstance(converted_value, int):
                                raise AttributeError(
                                    _ErrFmts.errmsg_python_type_not_supported % (
                                    type(converted_value), enums_pb2.INTEGER)
                                )
                            value.integer_value = converted_value
                        elif data_type == enums_pb2.STRING:
                            if not isinstance(converted_value, str):
                                raise AttributeError(
                                    _ErrFmts.errmsg_python_type_not_supported % (
                                    type(converted_value), enums_pb2.STRING)
                                )
                            value.string_value = converted_value
                        elif data_type == enums_pb2.BOOLEAN:
                            if not isinstance(converted_value, bool):
                                raise AttributeError(
                                    _ErrFmts.errmsg_python_type_not_supported % (
                                    type(converted_value), enums_pb2.BOOLEAN)
                                )
                            value.boolean_value = converted_value
                        elif data_type == enums_pb2.DECIMAL:
                            # TODO: Implement decimal
                            raise NotImplementedError(_ErrFmts.errmsg_not_implemented % enums_pb2.DECIMAL)
                        elif data_type == enums_pb2.TIMESTAMP:
                            if not isinstance(converted_value, datetime.datetime):
                                raise AttributeError(
                                    _ErrFmts.errmsg_python_type_not_supported % (
                                    type(converted_value), enums_pb2.TIMESTAMP)
                                )

                            offset = 0
                            utc_offset = converted_value.utcoffset()
                            if utc_offset is not None:
                                offset = int(utc_offset.total_seconds())

                            # Cannot assign timestamp_value
                            value = general_types_pb2.Value(
                                data_type = data_type,
                                timestamp_value = datatypes_pb2.Timestamp(
                                    unix_seconds = int(converted_value.timestamp()),
                                    timezone = converted_value.tzname(),
                                    offset = offset
                                )
                            )

                        elif data_type == enums_pb2.URI:
                            # TODO: Implement uri
                            raise NotImplementedError(_ErrFmts.errmsg_not_implemented % enums_pb2.URI)
                        elif data_type == enums_pb2.VOID:
                            pass
                        elif data_type == enums_pb2.FLOAT:
                            if not isinstance(converted_value, float):
                                raise AttributeError(
                                    _ErrFmts.errmsg_python_type_not_supported % (
                                    type(converted_value), enums_pb2.FLOAT)
                                )
                            value.float_value = converted_value
                        elif data_type == enums_pb2.UNSIGNED_INTEGER:
                            if not isinstance(converted_value, int):
                                raise AttributeError(
                                    _ErrFmts.errmsg_python_type_not_supported % (
                                    type(converted_value), enums_pb2.UNSIGNED_INTEGER)
                                )
                            value.unsigned_integer_value = converted_value
                        elif data_type == enums_pb2.BINARY:
                            if not isinstance(converted_value, bytearray):
                                raise AttributeError(
                                    _ErrFmts.errmsg_python_type_not_supported % (
                                    type(converted_value), enums_pb2.BINARY)
                                )
                            value.binary_value = converted_value
                        elif data_type == enums_pb2.UUID:
                            if not isinstance(converted_value, str):
                                raise AttributeError(
                                    _ErrFmts.errmsg_python_type_not_supported % (
                                    type(converted_value), enums_pb2.UUID)
                                )
                            value.uuid_value = converted_value
                        elif data_type == enums_pb2.TEXT:
                            if not isinstance(converted_value, str):
                                raise AttributeError(
                                    _ErrFmts.errmsg_python_type_not_supported % (
                                    type(converted_value), enums_pb2.TEXT)
                                )
                            value.text_value = converted_value
                        else:
                            raise AttributeError(_ErrFmts.errmsg_invalid_type)

                        values.append(value)

                    value_list = general_types_pb2.ValueList(
                        values = values
                    )

                    yield instance_pb2.CreateInstanceReq(
                        name = action_mapping.action_name,
                        sequence = action_topologies[action_mapping.action_name],
                        values = value_list
                    )

                row = cursor.fetchone()
        except Exception as exc:
            msg = _ErrFmts.errmsg_yield_instance % (query_mapping.query_string, exc)
            print(msg)
            ServicerContext.abort(StatusCode.ABORTED, msg)