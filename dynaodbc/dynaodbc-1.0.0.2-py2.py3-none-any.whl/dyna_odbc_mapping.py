"""
Module holding DynaODBCConnector mapping classes.

- DataMapping: SQL value to Dynizer value
- ActionMapping: SQL query result to Dynizer Action Instance
- QueryMapping: SQL query to actions

All classes contain a static 'from_dict' method to construct from a dictionary.

"""

from dynaodbc._dyna_odbc_const import _ErrFmts, _Keys

from dynagatewaytypes import enums_pb2

class DataMapping:
    """
    Class containing the parameters for parsing of one SQL value to a Dynizer value

    Fields:
    - component: WHO, WHAT, WHERE, WHEN enum proto value
    - position: Position integer in SQL source data
    - data_type: Dynizer data type enum proto value
    - label: Value label (optional)
    - convert_function: converter function for source data

    Methods:
    - from_dict
    - get_convert_function

    """

    @staticmethod
    def _default_convert(value):
        """
        Default convert function for SQL value.
        Returns value
        """
        return value

    @staticmethod
    def _any_to_int(value):
        """
        Any to integer converter for SQL value.
        Returns None for NULL values.
        """
        if value is None:
            return value
        try:
            return int(value)
        except Exception as exc:
            raise RuntimeError(_ErrFmts.errmsg_convert_fail % (value, exc)) from None


    @staticmethod
    def _any_to_string(value):
        """
        Any to string converter for SQL value.
        Returns None for NULL values.
        """
        if value is None:
            return value
        try:
            return str(value)
        except Exception as exc:
            raise RuntimeError(_ErrFmts.errmsg_convert_fail % (value, exc)) from None

    @staticmethod
    def _any_to_float(value):
        """
        Any to float converter for SQL value.
        Returns None for NULL values.
        """
        if value is None:
            return value
        try:
            return float(value)
        except Exception as exc:
            raise RuntimeError(_ErrFmts.errmsg_convert_fail % (value, exc)) from None

    _CONVERT_FUNCTIONS = {
        "default": _default_convert.__func__,
        "any_to_int": _any_to_int.__func__,
        "any_to_string": _any_to_string.__func__,
        "any_to_float": _any_to_float.__func__
    }

    @staticmethod
    def get_convert_function(key, convert_functions={}):
        """
        Gets the convert function for SQL value from string

        Args:
        - key: function name
        - convert_functions: custom convert functions dictionary

        """
        if key in convert_functions:
            return convert_functions[key]

        return DataMapping._CONVERT_FUNCTIONS[key]

    def __init__(self, component, position, data_type, label, convert_function = None, convert_functions={}):
        """
        Returns a new DataMapping

        Args:
        - component: WHO, WHAT, WHERE, WHEN string value
        - position: Position integer in SQL source data
        - data_type: Dynizer data type string value
        - label: Value label (optional)
        - convert_function: converter function for source data
        - convert_functions: custom convert functions dictionary

        """
        if not isinstance(position, int) or position <= 0:
            raise AttributeError(_ErrFmts.errmsg_invalid_position % position)
        self.position = position
        self.data_type = enums_pb2.DT_NONE
        self.convert_function = self._default_convert
        self.label = label

        try:
            self.component = enums_pb2.ComponentType.Value(component)
            if data_type is not None:
                self.data_type = enums_pb2.DataType.Value(data_type)
            if convert_function is not None:
                self.convert_function = self.get_convert_function(convert_function, convert_functions=convert_functions)
        except Exception as exc:
            raise AttributeError(_ErrFmts.errmsg_create_dm % exc) from None

    @staticmethod
    def from_dict(dct, convert_functions={}):
        """
        Returns a new DataMapping from a dictionary.

        Keys:
        - component: WHO, WHAT, WHERE, WHEN string value
        - position: Position integer in SQL source data
        - data_type: Dynizer data type string value
        - label: Value label (optional)
        - convert_function: converter function string for source data
        - convert_functions: custom convert functions dictionary

        """
        retval = None
        if isinstance(dct, list):
            retval = []
            for i, d in enumerate(dct):
                try:
                    retval.append(DataMapping.from_dict(d, convert_functions=convert_functions))
                except Exception as exc:
                    raise AttributeError(_ErrFmts.errmsg_read_index % (i, exc)) from None
        else:
            try:
                retval = DataMapping(
                    dct[_Keys.component],
                    dct[_Keys.position],
                    dct.get(_Keys.data_type, None),
                    dct.get(_Keys.label, None),
                    convert_function=dct.get(_Keys.convert_function, None),
                    convert_functions=convert_functions
                )
            except Exception as exc:
                raise AttributeError(_ErrFmts.errmsg_read_dm % exc) from None
        return retval

class ActionMapping:
    """
    Class containing the parameters of parsing SQL query data to an action

    Fields:
    - action_name: Action name to save data to
    - data_mappings: Data mappings of SQL values to use

    Methods:
    - from_dict

    """
    def __init__(self, action_name, data_mappings):
        """
        Returns a new ActionMapping

        Args:
        - action_name: Action name to save data to
        - data_mappings: Data mappings of SQL values to use

        """
        if not isinstance(action_name, str) or len(action_name) == 0:
            raise AttributeError(_ErrFmts.errmsg_invalid_action % action_name)

        self.action_name = action_name
        self.data_mappings = data_mappings

    @staticmethod
    def from_dict(dct, convert_functions={}):
        """
        Returns a new ActionMapping from a dictionary.

        Keys:
        - action_name: Action name to save data to
        - data_mappings: Data mappings of SQL values
        - convert_functions: custom convert functions dictionary

        """
        retval = None
        if isinstance(dct, list):
            retval = []
            for i, d in enumerate(dct):
                try:
                    retval.append(ActionMapping.from_dict(d, convert_functions=convert_functions))
                except Exception as exc:
                    raise AttributeError(_ErrFmts.errmsg_read_index % (i, exc)) from None
        else:
            try:
                retval = ActionMapping(
                    dct[_Keys.action_name],
                    DataMapping.from_dict(dct[_Keys.data_mappings], convert_functions=convert_functions)
                )
            except Exception as exc:
                raise AttributeError(_ErrFmts.errmsg_read_am % exc) from None
        return retval

class QueryMapping:
    """
    Class containing the parameters of a SQL query to convert to Dynizer actions

    Fields:
    - query_string: SQL query string to execute
    - action_mappings: Action mappings of SQL query

    Methods:
    - from_dict

    """
    def __init__(self, query_string, action_mappings):
        """
        Returns a new QueryMapping

        Args:
        - query_string: SQL query string to execute
        - action_mappings: Action mappings of SQL query

        """
        if not isinstance(query_string, str) or len(query_string) == 0:
            raise AttributeError(_ErrFmts.errmsg_invalid_query % query_string)

        self.query_string = query_string
        self.action_mappings = action_mappings

    @staticmethod
    def from_dict(dct, convert_functions={}):
        """
        Returns a new QueryMapping from a dictionary.

        Keys:
        - query_string: SQL query string to execute
        - action_mappings: Action mappings of SQL query
        - convert_functions: custom convert functions dictionary

        """
        retval = None
        if isinstance(dct, list):
            retval = []
            for i, d in enumerate(dct):
                try:
                    item = QueryMapping.from_dict(d, convert_functions=convert_functions)
                    if item is not None:
                        retval.append(item)
                except Exception as exc:
                    raise AttributeError(_ErrFmts.errmsg_read_index % (i, exc)) from None
        else:
            try:
                if dct.get(_Keys.ignore, False):
                    return retval

                retval = QueryMapping(
                    dct[_Keys.query_string],
                    ActionMapping.from_dict(dct[_Keys.action_mappings], convert_functions=convert_functions)
                )
            except Exception as exc:
                raise AttributeError(_ErrFmts.errmsg_read_qm % exc) from None
        return retval