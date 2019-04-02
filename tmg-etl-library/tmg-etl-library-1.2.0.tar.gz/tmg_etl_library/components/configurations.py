# TODO: Find a way to substitute default config values when they are needed from within functions
# e.g.: for func_config not in current_config: current_config.func_config = DefaultValue
from google.cloud.bigquery import WriteDisposition


class BQTOBQConfig:
    def __init__(self):
        # TODO: Find default values for these attributes
        self._full_table = True
        self._query = False
        self._query_file_name = None
        self._write_disposition = 'WRITE_APPEND'
        self._force_dataset_creation = True
        self._force_table_creation = True
        self._use_legacy_sql = False
        self._async_query = False
        self._query_params = {}

    @property
    def query_file_name(self):
        return self._query_file_name

    @query_file_name.setter
    def query_file_name(self, value):
        if not isinstance(value, str):
            raise TypeError('query_file_name must be set to a String Value')
        self._query_file_name = value

    @property
    def query_params(self):
        return self._query_params

    @query_params.setter
    def query_params(self, value):
        if not isinstance(value, dict):
            raise TypeError('query_params must be set to a Dictionary')
        self._query_params = value

    @property
    def async_query(self):
        return self._async_query

    @async_query.setter
    def async_query(self, value):
        if not isinstance(value, bool):
            raise TypeError('async_query must be set to a Boolean Value')
        self._async_query = value

    @property
    def full_table(self):
        return self._full_table

    @full_table.setter
    def full_table(self, value):
        if not isinstance(value, bool):
            raise TypeError('Full Table must be set to a Boolean Value (True/False')
        self._full_table = value

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        if not isinstance(value, str):
            raise TypeError('Query must be set to a String Value')
        self._query = value

    @property
    def write_disposition(self):
        return self._write_disposition

    @write_disposition.setter
    def write_disposition(self, value):
        """
        write_disposition setter raise value error if wrong type used

        :param str value:
        """
        allowed_dispositions = [
            WriteDisposition.WRITE_APPEND,
            WriteDisposition.WRITE_TRUNCATE,
            WriteDisposition.WRITE_EMPTY
        ]
        if value not in allowed_dispositions:
            raise ValueError(f"{value} not int {allowed_dispositions}")

        self._write_disposition = value

    @property
    def force_table_creation(self):
        return self._force_table_creation

    @force_table_creation.setter
    def force_table_creation(self, value):
        if not isinstance(value, bool):
            raise TypeError('force_table_creation must be set to a Boolean Value')
        self._force_table_creation = value

    @property
    def force_dataset_creation(self):
        return self._force_dataset_creation

    @force_dataset_creation.setter
    def force_dataset_creation(self, value):
        if not isinstance(value, bool):
            raise TypeError('force_dataset_creation must be set to a Boolean Value')
        self._force_dataset_creation = value

    @property
    def use_legacy_sql(self):
        return self._use_legacy_sql

    @use_legacy_sql.setter
    def use_legacy_sql(self, value):
        if not isinstance(value, bool):
            raise TypeError('use_legacy_sql must be set to a Boolean Value')
        self._use_legacy_sql = value


class BQTOMySQLConfig:
    # TODO: Discuss, can we just ignore all the CSV intermediate steps and then just set up the most robust default way to go from SOURCE > CSV > TARGET
    def __init__(self):
        # TODO: Find default values for these attributes
        self._write_disposition = 'WRITE_EMPTY'
        self._force_creation = True
        self._query = None
        self._query_params = None

    @property
    def write_disposition(self):
        return self._write_disposition

    @write_disposition.setter
    def write_disposition(self, value):
        if not isinstance(value, str):
            raise TypeError('write_disposition must be set to a String Value')
        self._write_disposition = value

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        if not isinstance(value, str):
            raise TypeError('query must be set to a String Value')
        self._query = value

    @property
    def query_params(self):
        return self._query_params

    @query_params.setter
    def query_params(self, value):
        if not isinstance(value, dict):
            raise TypeError('query_params must be set to a Dictionary Value')
        self._query_params = value

    @property
    def force_creation(self):
        return self._force_creation

    @force_creation.setter
    def force_creation(self, value):
        if not isinstance(value, bool):
            raise TypeError('force_creation must be set to a Boolean Value')
        self._force_creation = value


class BQTOCSVConfig:
    def __init__(self):
        # TODO: Find default values for these attributes
        self._field_delimiter = '§'
        # TODO: discuss whether we need a quote character for String fields
        self._quote_character = ''
        self._use_legacy_sql = False
        self._print_header = False
        self._full_table = True
        self._query = False
        self._query_file_path = None
        self._storage_retention = False
        self._gs_bucket = None
        self._gs_filename = None
        self._query_params = None

    @property
    def use_legacy_sql(self):
        return self._use_legacy_sql

    @use_legacy_sql.setter
    def use_legacy_sql(self, value):
        if not isinstance(value, bool):
            raise TypeError('use_legacy_sql must be set to a Boolean Value')
        self._use_legacy_sql = value

    @property
    def print_header(self):
        return self._print_header

    @print_header.setter
    def print_header(self, value):
        if not isinstance(value, bool):
            raise TypeError('Print Header must be set to a Boolean Value (True/False')
        self._print_header = value

    @property
    def full_table(self):
        return self._full_table

    @full_table.setter
    def full_table(self, value):
        if not isinstance(value, bool):
            raise TypeError('full_table must be set to a Boolean Value (True/False')
        self._full_table = value

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        if not isinstance(value, str):
            raise TypeError('Query must be set to a String Value')
        self._query = value

    @property
    def query_file_path(self):
        return self._query_file_path

    @query_file_path.setter
    def query_file_path(self, value):
        if not isinstance(value, str):
            raise TypeError('query_file_path must be set to a String Value')
        self._query_file_path = value

    @property
    def field_delimiter(self):
        return self._field_delimiter

    @field_delimiter.setter
    def field_delimiter(self, value):
        if not isinstance(value, str):
            raise TypeError('Query must be set to a String Value')
        self._field_delimiter = value

    @property
    def storage_retention(self):
        return self._storage_retention

    @storage_retention.setter
    def storage_retention(self, value):
        if not isinstance(value, bool):
            raise TypeError('source_format must be set to a Boolean Value')
        self._storage_retention = value

    @property
    def gs_bucket(self):
        return self._gs_bucket

    @gs_bucket.setter
    def gs_bucket(self, value):
        if not isinstance(value, str):
            raise TypeError('source_format must be set to a String Value')
        self._gs_bucket = value

    @property
    def gs_filename(self):
        return self._gs_filename

    @gs_filename.setter
    def gs_filename(self, value):
        if not isinstance(value, str):
            raise TypeError('gs_filename must be set to a String Value')
        self._gs_filename = value

    @property
    def query_params(self):
        return self._query_params

    @query_params.setter
    def query_params(self, value):
        if not isinstance(value, dict):
            raise TypeError('query_params must be set to a Dictionary Value')
        self._query_params = value


class BQTOGSConfig:
    def __init__(self):
        self._print_header = True
        self._field_delimiter = '§'
        self._tmp_bucket = None
        self._tmp_filename = None

    @property
    def print_header(self):
        return self._print_header

    @print_header.setter
    def print_header(self, value):
        if not isinstance(value, bool):
            raise TypeError('Print Header must be set to a Boolean Value (True/False')
        self._print_header = value

    @property
    def field_delimiter(self):
        return self._field_delimiter

    @field_delimiter.setter
    def field_delimiter(self, value):
        """
        :param value: Time in Minutes for when the table should expire (delete itself)
        :return: Nothing
        """
        if not isinstance(value, str):
            raise TypeError('Field Delimiter must be a String')
        elif len(value) != 1:
            raise TypeError('Field Delimiter must be of length 1')

        self._field_delimiter = value

    @property
    def tmp_bucket(self):
        return self._tmp_bucket

    @tmp_bucket.setter
    def tmp_bucket(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_bucket must be set to a String Value')
        self._tmp_bucket = value

    @property
    def tmp_filename(self):
        return self._tmp_filename

    @tmp_filename.setter
    def tmp_filename(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_filename must be set to a String Value')
        self._tmp_filename = value


class BQTOS3Config:
    def __init__(self):
        self._delimiter = '§'
        self._tmp_local_path = '/tmp/'
        self._tmp_filename = None
        self._include_headers = True
        self._quote_char = '"'
        self._query = None
        self._query_file_path = None
        self._query_params = None
        self._use_legacy_sql = False
        self._retain_local = False

    @property
    def delimiter(self):
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value):
        if not isinstance(value, str):
            raise TypeError('delimiter must be set to a String Value')
        self._delimiter = value

    @property
    def tmp_local_path(self):
        return self._tmp_local_path

    @tmp_local_path.setter
    def tmp_local_path(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_local_path must be set to a String Value')
        self._tmp_local_path = value

    @property
    def tmp_filename(self):
        return self._tmp_filename

    @tmp_filename.setter
    def tmp_filename(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_filename must be set to a String Value')
        self._tmp_filename = value

    @property
    def include_headers(self):
        return self._include_headers

    @include_headers.setter
    def include_headers(self, value):
        if not isinstance(value, bool):
            raise TypeError('include_headers must be set to a Boolean Value')
        self._include_headers = value

    @property
    def quote_char(self):
        return self._quote_char

    @quote_char.setter
    def quote_char(self, value):
        if not isinstance(value, str):
            raise TypeError('quote_char must be set to a String Value')
        self._quote_char = value

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        if not isinstance(value, str):
            raise TypeError('query must be set to a String Value')
        self._query = value

    @property
    def query_file_path(self):
        return self._query_file_path

    @query_file_path.setter
    def query_file_path(self, value):
        if not isinstance(value, str):
            raise TypeError('query_file_path must be set to a String Value')
        self._query_file_path = value

    @property
    def query_params(self):
        return self._query_params

    @query_params.setter
    def query_params(self, value):
        if not isinstance(value, dict):
            raise TypeError('query_params must be set to a Dictionary Value')
        self._query_params = value

    @property
    def use_legacy_sql(self):
        return self._use_legacy_sql

    @use_legacy_sql.setter
    def use_legacy_sql(self, value):
        if not isinstance(value, bool):
            raise TypeError('use_legacy_sql must be set to a Boolean Value')
        self._use_legacy_sql = value

    @property
    def retain_local(self):
        return self._retain_local

    @retain_local.setter
    def retain_local(self, value):
        if not isinstance(value, bool):
            raise TypeError('retain_local must be set to a Boolean Value')
        self._retain_local = value


class BQTOFTPConfig:
    def __init__(self):
        self._delimiter = '§'
        self._tmp_local_path = '/tmp/'
        self._tmp_filename = None
        self._include_headers = True
        self._quote_char = '"'
        self._query = None
        self._query_file_path = None
        self._query_params = None
        self._use_legacy_sql = False
        self._retain_local = False

    @property
    def delimiter(self):
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value):
        if not isinstance(value, str):
            raise TypeError('delimiter must be set to a String Value')
        self._delimiter = value

    @property
    def tmp_local_path(self):
        return self._tmp_local_path

    @tmp_local_path.setter
    def tmp_local_path(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_local_path must be set to a String Value')
        self._tmp_local_path = value

    @property
    def tmp_filename(self):
        return self._tmp_filename

    @tmp_filename.setter
    def tmp_filename(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_filename must be set to a String Value')
        self._tmp_filename = value

    @property
    def include_headers(self):
        return self._include_headers

    @include_headers.setter
    def include_headers(self, value):
        if not isinstance(value, bool):
            raise TypeError('include_headers must be set to a Boolean Value')
        self._include_headers = value

    @property
    def quote_char(self):
        return self._quote_char

    @quote_char.setter
    def quote_char(self, value):
        if not isinstance(value, str):
            raise TypeError('quote_char must be set to a String Value')
        self._quote_char = value

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        if not isinstance(value, str):
            raise TypeError('query must be set to a String Value')
        self._query = value

    @property
    def query_file_path(self):
        return self._query_file_path

    @query_file_path.setter
    def query_file_path(self, value):
        if not isinstance(value, str):
            raise TypeError('query_file_path must be set to a String Value')
        self._query_file_path = value

    @property
    def query_params(self):
        return self._query_params

    @query_params.setter
    def query_params(self, value):
        if not isinstance(value, dict):
            raise TypeError('query_params must be set to a Dictionary Value')
        self._query_params = value

    @property
    def use_legacy_sql(self):
        return self._use_legacy_sql

    @use_legacy_sql.setter
    def use_legacy_sql(self, value):
        if not isinstance(value, bool):
            raise TypeError('use_legacy_sql must be set to a Boolean Value')
        self._use_legacy_sql = value

    @property
    def retain_local(self):
        return self._retain_local

    @retain_local.setter
    def retain_local(self, value):
        if not isinstance(value, bool):
            raise TypeError('retain_local must be set to a Boolean Value')
        self._retain_local = value


class MySQLTOMySQLConfig:
    def __init__(self):
        self._query = None
        self._query_file_path = None
        self._insert_query = False
        self._query_params = None
        self._force_creation = True

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        if not isinstance(value, str):
            raise TypeError('query must be set to a String Value')
        self._query = value

    @property
    def query_file_path(self):
        return self._query_file_path

    @query_file_path.setter
    def query_file_path(self, value):
        if not isinstance(value, str):
            raise TypeError('query_file_path must be set to a String Value')
        self._query_file_path = value

    @property
    def query_params(self):
        return self._query_params

    @query_params.setter
    def query_params(self, value):
        if not isinstance(value, dict):
            raise TypeError('query_params must be set to a Dictionary Value')
        self._query_params = value

    @property
    def insert_query(self):
        return self._insert_query

    @insert_query.setter
    def insert_query(self, value):
        if not isinstance(value, bool):
            raise TypeError('insert_query must be set to a Boolean Value')
        self._insert_query = value

    @property
    def force_creation(self):
        return self._force_creation

    @force_creation.setter
    def force_creation(self, value):
        if not isinstance(value, bool):
            raise TypeError('force_creation must be set to a Boolean Value')
        self._force_creation = value


class MySQLTOBQConfig:
    # TODO: Discuss, can we just ignore all the CSV intermediate steps and then just set up the most robust default way to go from SOURCE > CSV > TARGET
    def __init__(self):
        # TODO: Find default values for these attributes
        self._write_disposition = 'WRITE_EMPTY'
        self._stream = False
        self._delimiter = '§'
        self._tmp_local_path = '/tmp/'
        self._tmp_filename = None
        self._include_headers = True
        self._quote_char = '"'
        self._query = None
        self._query_file_path = None
        self._query_params = None
        self._use_legacy_sql = False
        self._retain_local = False

    @property
    def write_disposition(self):
        return self._write_disposition

    @write_disposition.setter
    def write_disposition(self, value):
        if not isinstance(value, str):
            raise TypeError('source_format must be set to a String Value')
        self._write_disposition = value

    @property
    def stream(self):
        return self._stream

    @stream.setter
    def stream(self, value):
        if not isinstance(value, bool):
            raise TypeError('source_format must be set to a Boolean Value')
        self._stream = value

    @property
    def delimiter(self):
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value):
        if not isinstance(value, str):
            raise TypeError('delimiter must be set to a String Value')
        self._delimiter = value

    @property
    def tmp_local_path(self):
        return self._tmp_local_path

    @tmp_local_path.setter
    def tmp_local_path(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_local_path must be set to a String Value')
        self._tmp_local_path = value

    @property
    def tmp_filename(self):
        return self._tmp_filename

    @tmp_filename.setter
    def tmp_filename(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_filename must be set to a String Value')
        self._tmp_filename = value

    @property
    def include_headers(self):
        return self._include_headers

    @include_headers.setter
    def include_headers(self, value):
        if not isinstance(value, bool):
            raise TypeError('include_headers must be set to a Boolean Value')
        self._include_headers = value

    @property
    def quote_char(self):
        return self._quote_char

    @quote_char.setter
    def quote_char(self, value):
        if not isinstance(value, str):
            raise TypeError('quote_char must be set to a String Value')
        self._quote_char = value

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        if not isinstance(value, str):
            raise TypeError('query must be set to a String Value')
        self._query = value

    @property
    def query_file_path(self):
        return self._query_file_path

    @query_file_path.setter
    def query_file_path(self, value):
        if not isinstance(value, str):
            raise TypeError('query_file_path must be set to a String Value')
        self._query_file_path = value

    @property
    def query_params(self):
        return self._query_params

    @query_params.setter
    def query_params(self, value):
        if not isinstance(value, dict):
            raise TypeError('query_params must be set to a Dictionary Value')
        self._query_params = value

    @property
    def use_legacy_sql(self):
        return self._use_legacy_sql

    @use_legacy_sql.setter
    def use_legacy_sql(self, value):
        if not isinstance(value, bool):
            raise TypeError('use_legacy_sql must be set to a Boolean Value')
        self._use_legacy_sql = value

    @property
    def retain_local(self):
        return self._retain_local

    @retain_local.setter
    def retain_local(self, value):
        if not isinstance(value, bool):
            raise TypeError('retain_local must be set to a Boolean Value')
        self._retain_local = value


class MySQLTOCSVConfig:
    def __init__(self):
        self._delimiter = '§'
        self._include_headers = True
        self._quote_char = '"'
        self._query = None
        self._query_file_path = None
        self._query_params = None
        self._full_table = True

    @property
    def delimiter(self):
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value):
        if not isinstance(value, str):
            raise TypeError('delimiter must be set to a String Value')
        self._delimiter = value

    @property
    def include_headers(self):
        return self._include_headers

    @include_headers.setter
    def include_headers(self, value):
        if not isinstance(value, bool):
            raise TypeError('include_headers must be set to a Boolean Value')
        self._include_headers = value

    @property
    def quote_char(self):
        return self._quote_char

    @quote_char.setter
    def quote_char(self, value):
        if not isinstance(value, str):
            raise TypeError('quote_char must be set to a String Value')
        self._quote_char = value

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        if not isinstance(value, str):
            raise TypeError('query must be set to a String Value')
        self._query = value

    @property
    def query_file_path(self):
        return self._query_file_path

    @query_file_path.setter
    def query_file_path(self, value):
        if not isinstance(value, str):
            raise TypeError('query_file_path must be set to a String Value')
        self._query_file_path = value

    @property
    def query_params(self):
        return self._query_params

    @query_params.setter
    def query_params(self, value):
        if not isinstance(value, dict):
            raise TypeError('query_params must be set to a Dictionary Value')
        self._query_params = value

    @property
    def full_table(self):
        return self._full_table

    @full_table.setter
    def full_table(self, value):
        if not isinstance(value, bool):
            raise TypeError('full_table must be set to a Boolean Value')
        self._full_table = value


class MySQLTOGSConfig:
    def __init__(self):
        self._delimiter = '§'
        self._include_headers = True
        self._quote_char = '"'
        self._query = None
        self._query_file_path = None
        self._query_params = None
        self._full_table = True
        self._retain_local = False
        self._tmp_local_path = '/tmp/'
        self._tmp_filename = None

    @property
    def delimiter(self):
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value):
        if not isinstance(value, str):
            raise TypeError('delimiter must be set to a String Value')
        self._delimiter = value

    @property
    def include_headers(self):
        return self._include_headers

    @include_headers.setter
    def include_headers(self, value):
        if not isinstance(value, bool):
            raise TypeError('include_headers must be set to a Boolean Value')
        self._include_headers = value

    @property
    def quote_char(self):
        return self._quote_char

    @quote_char.setter
    def quote_char(self, value):
        if not isinstance(value, str):
            raise TypeError('quote_char must be set to a String Value')
        self._quote_char = value

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        if not isinstance(value, str):
            raise TypeError('query must be set to a String Value')
        self._query = value

    @property
    def query_file_path(self):
        return self._query_file_path

    @query_file_path.setter
    def query_file_path(self, value):
        if not isinstance(value, str):
            raise TypeError('query_file_path must be set to a String Value')
        self._query_file_path = value

    @property
    def query_params(self):
        return self._query_params

    @query_params.setter
    def query_params(self, value):
        if not isinstance(value, dict):
            raise TypeError('query_params must be set to a Dictionary Value')
        self._query_params = value

    @property
    def full_table(self):
        return self._full_table

    @full_table.setter
    def full_table(self, value):
        if not isinstance(value, bool):
            raise TypeError('full_table must be set to a Boolean Value')
        self._full_table = value

    @property
    def retain_local(self):
        return self._retain_local

    @retain_local.setter
    def retain_local(self, value):
        if not isinstance(value, bool):
            raise TypeError('retain_local must be set to a Boolean Value')
        self._retain_local = value

    @property
    def tmp_filename(self):
        return self._tmp_filename

    @tmp_filename.setter
    def tmp_filename(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_filename must be set to a String Value')
        self._tmp_filename = value

    @property
    def tmp_local_path(self):
        return self._tmp_local_path

    @tmp_local_path.setter
    def tmp_local_path(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_local_path must be set to a String Value')
        self._tmp_local_path = value


class MySQLTOS3Config:
    def __init__(self):
        self._delimiter = '§'
        self._include_headers = True
        self._quote_char = '"'
        self._query = None
        self._query_file_path = None
        self._query_params = None
        self._full_table = True
        self._retain_local = False
        self._tmp_local_path = '/tmp/'
        self._tmp_filename = None

    @property
    def delimiter(self):
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value):
        if not isinstance(value, str):
            raise TypeError('delimiter must be set to a String Value')
        self._delimiter = value

    @property
    def include_headers(self):
        return self._include_headers

    @include_headers.setter
    def include_headers(self, value):
        if not isinstance(value, bool):
            raise TypeError('include_headers must be set to a Boolean Value')
        self._include_headers = value

    @property
    def quote_char(self):
        return self._quote_char

    @quote_char.setter
    def quote_char(self, value):
        if not isinstance(value, str):
            raise TypeError('quote_char must be set to a String Value')
        self._quote_char = value

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        if not isinstance(value, str):
            raise TypeError('query must be set to a String Value')
        self._query = value

    @property
    def query_file_path(self):
        return self._query_file_path

    @query_file_path.setter
    def query_file_path(self, value):
        if not isinstance(value, str):
            raise TypeError('query_file_path must be set to a String Value')
        self._query_file_path = value

    @property
    def query_params(self):
        return self._query_params

    @query_params.setter
    def query_params(self, value):
        if not isinstance(value, dict):
            raise TypeError('query_params must be set to a Dictionary Value')
        self._query_params = value

    @property
    def full_table(self):
        return self._full_table

    @full_table.setter
    def full_table(self, value):
        if not isinstance(value, bool):
            raise TypeError('full_table must be set to a Boolean Value')
        self._full_table = value

    @property
    def retain_local(self):
        return self._retain_local

    @retain_local.setter
    def retain_local(self, value):
        if not isinstance(value, bool):
            raise TypeError('retain_local must be set to a Boolean Value')
        self._retain_local = value

    @property
    def tmp_filename(self):
        return self._tmp_filename

    @tmp_filename.setter
    def tmp_filename(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_filename must be set to a String Value')
        self._tmp_filename = value

    @property
    def tmp_local_path(self):
        return self._tmp_local_path

    @tmp_local_path.setter
    def tmp_local_path(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_local_path must be set to a String Value')
        self._tmp_local_path = value


class MySQLTOFTPConfig:
    def __init__(self):
        self._delimiter = '§'
        self._include_headers = True
        self._quote_char = '"'
        self._query = None
        self._query_file_path = None
        self._query_params = None
        self._full_table = True
        self._retain_local = False
        self._tmp_local_path = '/tmp/'
        self._tmp_filename = None

    @property
    def delimiter(self):
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value):
        if not isinstance(value, str):
            raise TypeError('delimiter must be set to a String Value')
        self._delimiter = value

    @property
    def include_headers(self):
        return self._include_headers

    @include_headers.setter
    def include_headers(self, value):
        if not isinstance(value, bool):
            raise TypeError('include_headers must be set to a Boolean Value')
        self._include_headers = value

    @property
    def quote_char(self):
        return self._quote_char

    @quote_char.setter
    def quote_char(self, value):
        if not isinstance(value, str):
            raise TypeError('quote_char must be set to a String Value')
        self._quote_char = value

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        if not isinstance(value, str):
            raise TypeError('query must be set to a String Value')
        self._query = value

    @property
    def query_file_path(self):
        return self._query_file_path

    @query_file_path.setter
    def query_file_path(self, value):
        if not isinstance(value, str):
            raise TypeError('query_file_path must be set to a String Value')
        self._query_file_path = value

    @property
    def query_params(self):
        return self._query_params

    @query_params.setter
    def query_params(self, value):
        if not isinstance(value, dict):
            raise TypeError('query_params must be set to a Dictionary Value')
        self._query_params = value

    @property
    def full_table(self):
        return self._full_table

    @full_table.setter
    def full_table(self, value):
        if not isinstance(value, bool):
            raise TypeError('full_table must be set to a Boolean Value')
        self._full_table = value

    @property
    def retain_local(self):
        return self._retain_local

    @retain_local.setter
    def retain_local(self, value):
        if not isinstance(value, bool):
            raise TypeError('retain_local must be set to a Boolean Value')
        self._retain_local = value

    @property
    def tmp_filename(self):
        return self._tmp_filename

    @tmp_filename.setter
    def tmp_filename(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_filename must be set to a String Value')
        self._tmp_filename = value

    @property
    def tmp_local_path(self):
        return self._tmp_local_path

    @tmp_local_path.setter
    def tmp_local_path(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_local_path must be set to a String Value')
        self._tmp_local_path = value


class CSVTOBQConfig:
    def __init__(self):
        # TODO: Find default values for these attributes
        self._create_disposition = 'CREATE_IF_NEEDED'
        self._write_disposition = 'WRITE_EMPTY'
        self._field_delimiter = '§'
        self._source_format = 'CSV'
        self._allow_quoted_newlines = False
        self._quote_character = None
        self._skip_leading_rows = None
        self._ignore_unknown_values = None
        self._max_bad_records = 0
        self._allow_jagged_rows = None
        self._partitioned_field = None
        self._expiry = None
        self._auto_generate_schema = False

    @property
    def create_disposition(self):
        return self._create_disposition

    @create_disposition.setter
    def create_disposition(self, value):
        if not isinstance(value, str):
            raise TypeError('create_disposition must be set to a String Value')
        self._create_disposition = value

    @property
    def write_disposition(self):
        return self._write_disposition

    @write_disposition.setter
    def write_disposition(self, value):
        if not isinstance(value, str):
            raise TypeError('write_disposition must be set to a String Value')
        self._write_disposition = value

    @property
    def source_format(self):
        return self._source_format

    @source_format.setter
    def source_format(self, value):
        if not isinstance(value, str):
            raise TypeError('source_format must be set to a String Value')
        self._source_format = value

    @property
    def field_delimiter(self):
        return self._field_delimiter

    @field_delimiter.setter
    def field_delimiter(self, value):
        """
        :param str value: char which delimit the column on the file
        :return: Nothing
        """
        if not isinstance(value, str):
            raise TypeError('Field Delimiter must be a String')
        elif len(value) != 1:
            raise TypeError('Field Delimiter must be of length 1')

        self._field_delimiter = value

    @property
    def allow_quoted_newlines(self):
        return self._allow_quoted_newlines

    @allow_quoted_newlines.setter
    def allow_quoted_newlines(self, value):
        if not isinstance(value, bool):
            raise TypeError('allow_quoted_newlines must be set to a Boolean Value')
        self._allow_quoted_newlines = value

    @property
    def skip_leading_rows(self):
        return self._skip_leading_rows

    @skip_leading_rows.setter
    def skip_leading_rows(self, value):
        if not isinstance(value, bool):
            raise TypeError('skip_leading_rows must be set to a Boolean Value')
        self._skip_leading_rows = value

    @property
    def max_bad_records(self):
        return self._max_bad_records

    @max_bad_records.setter
    def max_bad_records(self, value):
        if not isinstance(value, int):
            raise TypeError('max_bad_records must be set to a Integer Value')
        self._max_bad_records = value

    @property
    def allow_jagged_rows(self):
        return self._allow_jagged_rows

    @allow_jagged_rows.setter
    def allow_jagged_rows(self, value):
        if not isinstance(value, bool):
            raise TypeError('allow_jagged_rows must be set to a Boolean Value')
        self._allow_jagged_rows = value

    @property
    def quote_character(self):
        return self._quote_character

    @quote_character.setter
    def quote_character(self, value):
        if not isinstance(value, str):
            raise TypeError('quote_character must be set to a String Value')
        self._quote_character = value

    @property
    def ignore_unknown_values(self):
        return self._ignore_unknown_values

    @ignore_unknown_values.setter
    def ignore_unknown_values(self, value):
        if not isinstance(value, bool):
            raise TypeError('ignore_unknown_values must be set to a Boolean Value')
        self._ignore_unknown_values = value

    @property
    def expiry(self):
        return self._expiry

    @expiry.setter
    def expiry(self, value):
        """
        :param value: Time in Minutes for when the table should expire (delete itself)
        :return: Nothing
        """
        if not isinstance(value, int):
            raise TypeError('Partitioned Field must be an Integer')
        self._expiry = value

    @property
    def partitioned_field(self):
        return self._partitioned_field

    @partitioned_field.setter
    def partitioned_field(self, value):
        """
        :param value: Field (String) to set as the field to partition the table on
        :return: Nothing
        """
        if not isinstance(value, str):
            raise TypeError('Partitioned Field must be a String')

        self._partitioned_field = value

    @property
    def auto_generate_schema(self):
        return self._auto_generate_schema

    @auto_generate_schema.setter
    def auto_generate_schema(self, value):
        if not isinstance(value, bool):
            raise TypeError('source_format must be set to a Boolean Value')
        self._auto_generate_schema = value


class CSVTOMySQLConfig:
    def __init__(self):
        # TODO: Find default values for these attributes
        self._create_disposition = 'CREATE_IF_NEEDED'
        self._write_disposition = 'WRITE_EMPTY'
        self._field_delimiter = '§'
        self._source_format = 'CSV'
        self._quote_character = None
        self._skip_leading_rows = None
        self._auto_generate_schema = False

    @property
    def create_disposition(self):
        return self._create_disposition

    @create_disposition.setter
    def create_disposition(self, value):
        if not isinstance(value, str):
            raise TypeError('create_disposition must be set to a String Value')
        self._create_disposition = value

    @property
    def write_disposition(self):
        return self._write_disposition

    @write_disposition.setter
    def write_disposition(self, value):
        if not isinstance(value, str):
            raise TypeError('write_disposition must be set to a String Value')
        self._write_disposition = value

    @property
    def source_format(self):
        return self._source_format

    @source_format.setter
    def source_format(self, value):
        if not isinstance(value, str):
            raise TypeError('source_format must be set to a String Value')
        self._source_format = value

    @property
    def field_delimiter(self):
        return self._field_delimiter

    @field_delimiter.setter
    def field_delimiter(self, value):
        """
        :param value: Time in Minutes for when the table should expire (delete itself)
        :return: Nothing
        """
        if not isinstance(value, str):
            raise TypeError('Field Delimiter must be a String')
        elif len(value) != 1:
            raise TypeError('Field Delimiter must be of length 1')

        self._field_delimiter = value

    @property
    def allow_quoted_newlines(self):
        return self._allow_quoted_newlines

    @allow_quoted_newlines.setter
    def allow_quoted_newlines(self, value):
        if not isinstance(value, bool):
            raise TypeError('allow_quoted_newlines must be set to a Boolean Value')
        self._allow_quoted_newlines = value

    @property
    def skip_leading_rows(self):
        return self._skip_leading_rows

    @skip_leading_rows.setter
    def skip_leading_rows(self, value):
        if not isinstance(value, bool):
            raise TypeError('skip_leading_rows must be set to a Boolean Value')
        self._skip_leading_rows = value

    @property
    def max_bad_records(self):
        return self._max_bad_records

    @max_bad_records.setter
    def max_bad_records(self, value):
        if not isinstance(value, int):
            raise TypeError('max_bad_records must be set to a Integer Value')
        self._max_bad_records = value

    @property
    def allow_jagged_rows(self):
        return self._allow_jagged_rows

    @allow_jagged_rows.setter
    def allow_jagged_rows(self, value):
        if not isinstance(value, bool):
            raise TypeError('allow_jagged_rows must be set to a Boolean Value')
        self._allow_jagged_rows = value

    @property
    def quote_character(self):
        return self._quote_character

    @quote_character.setter
    def quote_character(self, value):
        if not isinstance(value, str):
            raise TypeError('quote_character must be set to a String Value')
        self._quote_character = value

    @property
    def ignore_unknown_values(self):
        return self._ignore_unknown_values

    @ignore_unknown_values.setter
    def ignore_unknown_values(self, value):
        if not isinstance(value, bool):
            raise TypeError('ignore_unknown_values must be set to a Boolean Value')
        self._ignore_unknown_values = value


class CSVTOGSConfig:
    def __init__(self):
        self._write_disposition = 'REPLACE'

    @property
    def write_disposition(self):
        return self._write_disposition

    @write_disposition.setter
    def write_disposition(self, value):
        if not isinstance(value, str):
            raise TypeError('write_disposition must be set to a String Value')
        self._write_disposition = value


class CSVTOS3Config:
    def __init__(self):
        self._write_disposition = 'REPLACE'

    @property
    def write_disposition(self):
        return self._write_disposition

    @write_disposition.setter
    def write_disposition(self, value):
        if not isinstance(value, str):
            raise TypeError('write_disposition must be set to a String Value')
        self._write_disposition = value


class CSVTOFTPConfig:
    def __init__(self):
        self._write_disposition = 'REPLACE'

    @property
    def write_disposition(self):
        return self._write_disposition

    @write_disposition.setter
    def write_disposition(self, value):
        if not isinstance(value, str):
            raise TypeError('write_disposition must be set to a String Value')
        self._write_disposition = value


class GSTOBQConfig:
    def __init__(self):
        # TODO: Find default values for these attributes
        self._create_disposition = 'CREATE_IF_NEEDED'
        self._write_disposition = 'WRITE_EMPTY'
        self._field_delimiter = '§'
        self._source_format = 'CSV'
        self._allow_quoted_newlines = False
        self._quote_character = None
        self._skip_leading_rows = None
        self._ignore_unknown_values = None
        self._max_bad_records = 0
        self._allow_jagged_rows = None
        self._partitioned_field = None
        self._expiry = None
        self._auto_generate_schema = False

    @property
    def create_disposition(self):
        return self._create_disposition

    @create_disposition.setter
    def create_disposition(self, value):
        if not isinstance(value, str):
            raise TypeError('create_disposition must be set to a String Value')
        self._create_disposition = value

    @property
    def write_disposition(self):
        return self._write_disposition

    @write_disposition.setter
    def write_disposition(self, value):
        if not isinstance(value, str):
            raise TypeError('source_format must be set to a String Value')
        self._write_disposition = value

    @property
    def source_format(self):
        return self._source_format

    @source_format.setter
    def source_format(self, value):
        if not isinstance(value, str):
            raise TypeError('source_format must be set to a String Value')
        self._source_format = value

    @property
    def field_delimiter(self):
        return self._field_delimiter

    @field_delimiter.setter
    def field_delimiter(self, value):
        """
        :param value: Time in Minutes for when the table should expire (delete itself)
        :return: Nothing
        """
        if not isinstance(value, str):
            raise TypeError('Field Delimiter must be a String')
        elif len(value) != 1:
            raise TypeError('Field Delimiter must be of length 1')

        self._field_delimiter = value

    @property
    def allow_quoted_newlines(self):
        return self._allow_quoted_newlines

    @allow_quoted_newlines.setter
    def allow_quoted_newlines(self, value):
        if not isinstance(value, bool):
            raise TypeError('allow_quoted_newlines must be set to a Boolean Value')
        self._allow_quoted_newlines = value

    @property
    def skip_leading_rows(self):
        return self._skip_leading_rows

    @skip_leading_rows.setter
    def skip_leading_rows(self, value):
        if not isinstance(value, bool):
            raise TypeError('skip_leading_rows must be set to a Boolean Value')
        self._skip_leading_rows = value

    @property
    def max_bad_records(self):
        return self._max_bad_records

    @max_bad_records.setter
    def max_bad_records(self, value):
        if not isinstance(value, int):
            raise TypeError('max_bad_records must be set to a Integer Value')
        self._max_bad_records = value

    @property
    def allow_jagged_rows(self):
        return self._allow_jagged_rows

    @allow_jagged_rows.setter
    def allow_jagged_rows(self, value):
        if not isinstance(value, bool):
            raise TypeError('allow_jagged_rows must be set to a Boolean Value')
        self._allow_jagged_rows = value

    @property
    def quote_character(self):
        return self._quote_character

    @quote_character.setter
    def quote_character(self, value):
        if not isinstance(value, str):
            raise TypeError('quote_character must be set to a String Value')
        self._quote_character = value

    @property
    def ignore_unknown_values(self):
        return self._ignore_unknown_values

    @ignore_unknown_values.setter
    def ignore_unknown_values(self, value):
        if not isinstance(value, bool):
            raise TypeError('ignore_unknown_values must be set to a Boolean Value')
        self._ignore_unknown_values = value

    @property
    def expiry(self):
        return self._expiry

    @expiry.setter
    def expiry(self, value):
        """
        :param value: Time in Minutes for when the table should expire (delete itself)
        :return: Nothing
        """
        if not isinstance(value, int):
            raise TypeError('Partitioned Field must be an Integer')

        self._expiry = value

    @property
    def partitioned_field(self):
        return self._partitioned_field

    @partitioned_field.setter
    def partitioned_field(self, value):
        """
        :param value: Field (String) to set as the field to partition the table on
        :return: Nothing
        """
        if not isinstance(value, str):
            raise TypeError('Partitioned Field must be a String')

        self._partitioned_field = value

    @property
    def auto_generate_schema(self):
        return self._auto_generate_schema

    @auto_generate_schema.setter
    def auto_generate_schema(self, value):
        if not isinstance(value, bool):
            raise TypeError('source_format must be set to a Boolean Value')
        self._auto_generate_schema = value


class GSTOMySQLConfig():
    def __init__(self):
        self._tmp_local_path = '/tmp/'
        self._tmp_filename = None
        self._delimiter = '§'
        self._include_headers = True
        self._quote_char = '"'
        self._retain_local = False

    @property
    def tmp_filename(self):
        return self._tmp_filename

    @tmp_filename.setter
    def tmp_filename(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_filename must be set to a String Value')
        self._tmp_filename = value

    @property
    def tmp_local_path(self):
        return self._tmp_local_path

    @tmp_local_path.setter
    def tmp_local_path(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_local_path must be set to a String Value')
        self._tmp_local_path = value

    @property
    def delimiter(self):
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value):
        if not isinstance(value, str):
            raise TypeError('delimiter must be set to a String Value')
        self._delimiter = value

    @property
    def include_headers(self):
        return self._include_headers

    @include_headers.setter
    def include_headers(self, value):
        if not isinstance(value, bool):
            raise TypeError('include_headers must be set to a Boolean Value')
        self._include_headers = value

    @property
    def quote_char(self):
        return self._quote_char

    @quote_char.setter
    def quote_char(self, value):
        if not isinstance(value, str):
            raise TypeError('quote_char must be set to a String Value')
        self._quote_char = value

    @property
    def retain_local(self):
        return self._retain_local

    @retain_local.setter
    def retain_local(self, value):
        if not isinstance(value, bool):
            raise TypeError('retain_local must be set to a Boolean Value')
        self._retain_local = value


class GSTOCSVConfig():
    def __init__(self):
        pass


class S3TOBQConfig():
    def __init__(self):
        # TODO: Find default values for these attributes
        self._create_disposition = 'CREATE_IF_NEEDED'
        self._write_disposition = 'WRITE_EMPTY'
        self._field_delimiter = '§'
        self._source_format = 'CSV'
        self._allow_quoted_newlines = False
        self._quote_character = None
        self._skip_leading_rows = None
        self._ignore_unknown_values = None
        self._max_bad_records = 0
        self._allow_jagged_rows = None
        self._partitioned_field = None
        self._expiry = None
        self._auto_generate_schema = False
        self._tmp_local_path = '/tmp/'
        self._tmp_filename = None
        self._delimiter = '§'
        self._include_headers = True
        self._quote_char = '"'
        self._retain_local = False

    @property
    def create_disposition(self):
        return self._create_disposition

    @create_disposition.setter
    def create_disposition(self, value):
        if not isinstance(value, str):
            raise TypeError('create_disposition must be set to a String Value')
        self._create_disposition = value

    @property
    def write_disposition(self):
        return self._write_disposition

    @write_disposition.setter
    def write_disposition(self, value):
        if not isinstance(value, str):
            raise TypeError('write_disposition must be set to a String Value')
        self._write_disposition = value

    @property
    def source_format(self):
        return self._source_format

    @source_format.setter
    def source_format(self, value):
        if not isinstance(value, str):
            raise TypeError('source_format must be set to a String Value')
        self._source_format = value

    @property
    def field_delimiter(self):
        return self._field_delimiter

    @field_delimiter.setter
    def field_delimiter(self, value):
        """
        :param value: Time in Minutes for when the table should expire (delete itself)
        :return: Nothing
        """
        if not isinstance(value, str):
            raise TypeError('Field Delimiter must be a String')
        elif len(value) != 1:
            raise TypeError('Field Delimiter must be of length 1')

        self._field_delimiter = value

    @property
    def allow_quoted_newlines(self):
        return self._allow_quoted_newlines

    @allow_quoted_newlines.setter
    def allow_quoted_newlines(self, value):
        if not isinstance(value, bool):
            raise TypeError('allow_quoted_newlines must be set to a Boolean Value')
        self._allow_quoted_newlines = value

    @property
    def skip_leading_rows(self):
        return self._skip_leading_rows

    @skip_leading_rows.setter
    def skip_leading_rows(self, value):
        if not isinstance(value, bool):
            raise TypeError('skip_leading_rows must be set to a Boolean Value')
        self._skip_leading_rows = value

    @property
    def max_bad_records(self):
        return self._max_bad_records

    @max_bad_records.setter
    def max_bad_records(self, value):
        if not isinstance(value, int):
            raise TypeError('max_bad_records must be set to a Integer Value')
        self._max_bad_records = value

    @property
    def allow_jagged_rows(self):
        return self._allow_jagged_rows

    @allow_jagged_rows.setter
    def allow_jagged_rows(self, value):
        if not isinstance(value, bool):
            raise TypeError('allow_jagged_rows must be set to a Boolean Value')
        self._allow_jagged_rows = value

    @property
    def quote_character(self):
        return self._quote_character

    @quote_character.setter
    def quote_character(self, value):
        if not isinstance(value, str):
            raise TypeError('quote_character must be set to a String Value')
        self._quote_character = value

    @property
    def ignore_unknown_values(self):
        return self._ignore_unknown_values

    @ignore_unknown_values.setter
    def ignore_unknown_values(self, value):
        if not isinstance(value, bool):
            raise TypeError('ignore_unknown_values must be set to a Boolean Value')
        self._ignore_unknown_values = value

    @property
    def expiry(self):
        return self._expiry

    @expiry.setter
    def expiry(self, value):
        """
        :param value: Time in Minutes for when the table should expire (delete itself)
        :return: Nothing
        """
        if not isinstance(value, int):
            raise TypeError('Partitioned Field must be an Integer')

        self._expiry = value

    @property
    def partitioned_field(self):
        return self._partitioned_field

    @partitioned_field.setter
    def partitioned_field(self, value):
        """
        :param value: Field (String) to set as the field to partition the table on
        :return: Nothing
        """
        if not isinstance(value, str):
            raise TypeError('Partitioned Field must be a String')

        self._partitioned_field = value

    @property
    def auto_generate_schema(self):
        return self._auto_generate_schema

    @auto_generate_schema.setter
    def auto_generate_schema(self, value):
        if not isinstance(value, bool):
            raise TypeError('source_format must be set to a Boolean Value')
        self._auto_generate_schema = value

    @property
    def tmp_filename(self):
        return self._tmp_filename

    @tmp_filename.setter
    def tmp_filename(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_filename must be set to a String Value')
        self._tmp_filename = value

    @property
    def tmp_local_path(self):
        return self._tmp_local_path

    @tmp_local_path.setter
    def tmp_local_path(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_local_path must be set to a String Value')
        self._tmp_local_path = value

    @property
    def delimiter(self):
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value):
        if not isinstance(value, str):
            raise TypeError('delimiter must be set to a String Value')
        self._delimiter = value

    @property
    def include_headers(self):
        return self._include_headers

    @include_headers.setter
    def include_headers(self, value):
        if not isinstance(value, bool):
            raise TypeError('include_headers must be set to a Boolean Value')
        self._include_headers = value

    @property
    def quote_char(self):
        return self._quote_char

    @quote_char.setter
    def quote_char(self, value):
        if not isinstance(value, str):
            raise TypeError('quote_char must be set to a String Value')
        self._quote_char = value

    @property
    def retain_local(self):
        return self._retain_local

    @retain_local.setter
    def retain_local(self, value):
        if not isinstance(value, bool):
            raise TypeError('retain_local must be set to a Boolean Value')
        self._retain_local = value


class S3TOMySQLConfig():
    def __init__(self):
        self._tmp_local_path = '/tmp/'
        self._tmp_filename = None
        self._delimiter = '§'
        self._include_headers = True
        self._quote_char = '"'
        self._retain_local = False

    @property
    def tmp_filename(self):
        return self._tmp_filename

    @tmp_filename.setter
    def tmp_filename(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_filename must be set to a String Value')
        self._tmp_filename = value

    @property
    def tmp_local_path(self):
        return self._tmp_local_path

    @tmp_local_path.setter
    def tmp_local_path(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_local_path must be set to a String Value')
        self._tmp_local_path = value

    @property
    def delimiter(self):
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value):
        if not isinstance(value, str):
            raise TypeError('delimiter must be set to a String Value')
        self._delimiter = value

    @property
    def include_headers(self):
        return self._include_headers

    @include_headers.setter
    def include_headers(self, value):
        if not isinstance(value, bool):
            raise TypeError('include_headers must be set to a Boolean Value')
        self._include_headers = value

    @property
    def quote_char(self):
        return self._quote_char

    @quote_char.setter
    def quote_char(self, value):
        if not isinstance(value, str):
            raise TypeError('quote_char must be set to a String Value')
        self._quote_char = value

    @property
    def retain_local(self):
        return self._retain_local

    @retain_local.setter
    def retain_local(self, value):
        if not isinstance(value, bool):
            raise TypeError('retain_local must be set to a Boolean Value')
        self._retain_local = value


class S3TOCSVConfig():
    def __init__(self):
        pass


class S3TOGSConfig():
    def __init__(self):
        self._tmp_local_path = '/tmp/'
        self._tmp_filename = None
        self._delimiter = '§'
        self._include_headers = True
        self._quote_char = '"'
        self._retain_local = False

    @property
    def tmp_filename(self):
        return self._tmp_filename

    @tmp_filename.setter
    def tmp_filename(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_filename must be set to a String Value')
        self._tmp_filename = value

    @property
    def tmp_local_path(self):
        return self._tmp_local_path

    @tmp_local_path.setter
    def tmp_local_path(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_local_path must be set to a String Value')
        self._tmp_local_path = value

    @property
    def delimiter(self):
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value):
        if not isinstance(value, str):
            raise TypeError('delimiter must be set to a String Value')
        self._delimiter = value

    @property
    def include_headers(self):
        return self._include_headers

    @include_headers.setter
    def include_headers(self, value):
        if not isinstance(value, bool):
            raise TypeError('include_headers must be set to a Boolean Value')
        self._include_headers = value

    @property
    def quote_char(self):
        return self._quote_char

    @quote_char.setter
    def quote_char(self, value):
        if not isinstance(value, str):
            raise TypeError('quote_char must be set to a String Value')
        self._quote_char = value

    @property
    def retain_local(self):
        return self._retain_local

    @retain_local.setter
    def retain_local(self, value):
        if not isinstance(value, bool):
            raise TypeError('retain_local must be set to a Boolean Value')
        self._retain_local = value


class FTPTOBQConfig():
    def __init__(self):
        # TODO: Find default values for these attributes
        self._create_disposition = 'CREATE_IF_NEEDED'
        self._write_disposition = 'WRITE_EMPTY'
        self._field_delimiter = '§'
        self._source_format = 'CSV'
        self._allow_quoted_newlines = False
        self._quote_character = None
        self._skip_leading_rows = None
        self._ignore_unknown_values = None
        self._max_bad_records = 0
        self._allow_jagged_rows = None
        self._partitioned_field = None
        self._expiry = None
        self._auto_generate_schema = False
        self._tmp_local_path = '/tmp/'
        self._tmp_filename = None
        self._delimiter = '§'
        self._include_headers = True
        self._quote_char = '"'
        self._retain_local = False

    @property
    def create_disposition(self):
        return self._create_disposition

    @create_disposition.setter
    def create_disposition(self, value):
        if not isinstance(value, str):
            raise TypeError('create_disposition must be set to a String Value')
        self._create_disposition = value

    @property
    def write_disposition(self):
        return self._write_disposition

    @write_disposition.setter
    def write_disposition(self, value):
        if not isinstance(value, str):
            raise TypeError('write_disposition must be set to a String Value')
        self._write_disposition = value

    @property
    def source_format(self):
        return self._source_format

    @source_format.setter
    def source_format(self, value):
        if not isinstance(value, str):
            raise TypeError('source_format must be set to a String Value')
        self._source_format = value

    @property
    def field_delimiter(self):
        return self._field_delimiter

    @field_delimiter.setter
    def field_delimiter(self, value):
        """
        :param value: Time in Minutes for when the table should expire (delete itself)
        :return: Nothing
        """
        if not isinstance(value, str):
            raise TypeError('Field Delimiter must be a String')
        elif len(value) != 1:
            raise TypeError('Field Delimiter must be of length 1')

        self._field_delimiter = value

    @property
    def allow_quoted_newlines(self):
        return self._allow_quoted_newlines

    @allow_quoted_newlines.setter
    def allow_quoted_newlines(self, value):
        if not isinstance(value, bool):
            raise TypeError('allow_quoted_newlines must be set to a Boolean Value')
        self._allow_quoted_newlines = value

    @property
    def skip_leading_rows(self):
        return self._skip_leading_rows

    @skip_leading_rows.setter
    def skip_leading_rows(self, value):
        if not isinstance(value, bool):
            raise TypeError('skip_leading_rows must be set to a Boolean Value')
        self._skip_leading_rows = value

    @property
    def max_bad_records(self):
        return self._max_bad_records

    @max_bad_records.setter
    def max_bad_records(self, value):
        if not isinstance(value, int):
            raise TypeError('max_bad_records must be set to a Integer Value')
        self._max_bad_records = value

    @property
    def allow_jagged_rows(self):
        return self._allow_jagged_rows

    @allow_jagged_rows.setter
    def allow_jagged_rows(self, value):
        if not isinstance(value, bool):
            raise TypeError('allow_jagged_rows must be set to a Boolean Value')
        self._allow_jagged_rows = value

    @property
    def quote_character(self):
        return self._quote_character

    @quote_character.setter
    def quote_character(self, value):
        if not isinstance(value, str):
            raise TypeError('quote_character must be set to a String Value')
        self._quote_character = value

    @property
    def ignore_unknown_values(self):
        return self._ignore_unknown_values

    @ignore_unknown_values.setter
    def ignore_unknown_values(self, value):
        if not isinstance(value, bool):
            raise TypeError('ignore_unknown_values must be set to a Boolean Value')
        self._ignore_unknown_values = value

    @property
    def expiry(self):
        return self._expiry

    @expiry.setter
    def expiry(self, value):
        """
        :param value: Time in Minutes for when the table should expire (delete itself)
        :return: Nothing
        """
        if not isinstance(value, int):
            raise TypeError('Partitioned Field must be an Integer')

        self._expiry = value

    @property
    def partitioned_field(self):
        return self._partitioned_field

    @partitioned_field.setter
    def partitioned_field(self, value):
        """
        :param value: Field (String) to set as the field to partition the table on
        :return: Nothing
        """
        if not isinstance(value, str):
            raise TypeError('Partitioned Field must be a String')

        self._partitioned_field = value

    @property
    def auto_generate_schema(self):
        return self._auto_generate_schema

    @auto_generate_schema.setter
    def auto_generate_schema(self, value):
        if not isinstance(value, bool):
            raise TypeError('source_format must be set to a Boolean Value')
        self._auto_generate_schema = value

    @property
    def tmp_filename(self):
        return self._tmp_filename

    @tmp_filename.setter
    def tmp_filename(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_filename must be set to a String Value')
        self._tmp_filename = value

    @property
    def tmp_local_path(self):
        return self._tmp_local_path

    @tmp_local_path.setter
    def tmp_local_path(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_local_path must be set to a String Value')
        self._tmp_local_path = value

    @property
    def delimiter(self):
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value):
        if not isinstance(value, str):
            raise TypeError('delimiter must be set to a String Value')
        self._delimiter = value

    @property
    def include_headers(self):
        return self._include_headers

    @include_headers.setter
    def include_headers(self, value):
        if not isinstance(value, bool):
            raise TypeError('include_headers must be set to a Boolean Value')
        self._include_headers = value

    @property
    def quote_char(self):
        return self._quote_char

    @quote_char.setter
    def quote_char(self, value):
        if not isinstance(value, str):
            raise TypeError('quote_char must be set to a String Value')
        self._quote_char = value

    @property
    def retain_local(self):
        return self._retain_local

    @retain_local.setter
    def retain_local(self, value):
        if not isinstance(value, bool):
            raise TypeError('retain_local must be set to a Boolean Value')
        self._retain_local = value


class FTPTOMySQLConfig():
    def __init__(self):
        self._tmp_local_path = '/tmp/'
        self._tmp_filename = None
        self._delimiter = '§'
        self._include_headers = True
        self._quote_char = '"'
        self._retain_local = False

    @property
    def tmp_filename(self):
        return self._tmp_filename

    @tmp_filename.setter
    def tmp_filename(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_filename must be set to a String Value')
        self._tmp_filename = value

    @property
    def tmp_local_path(self):
        return self._tmp_local_path

    @tmp_local_path.setter
    def tmp_local_path(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_local_path must be set to a String Value')
        self._tmp_local_path = value

    @property
    def delimiter(self):
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value):
        if not isinstance(value, str):
            raise TypeError('delimiter must be set to a String Value')
        self._delimiter = value

    @property
    def include_headers(self):
        return self._include_headers

    @include_headers.setter
    def include_headers(self, value):
        if not isinstance(value, bool):
            raise TypeError('include_headers must be set to a Boolean Value')
        self._include_headers = value

    @property
    def quote_char(self):
        return self._quote_char

    @quote_char.setter
    def quote_char(self, value):
        if not isinstance(value, str):
            raise TypeError('quote_char must be set to a String Value')
        self._quote_char = value

    @property
    def retain_local(self):
        return self._retain_local

    @retain_local.setter
    def retain_local(self, value):
        if not isinstance(value, bool):
            raise TypeError('retain_local must be set to a Boolean Value')
        self._retain_local = value


class FTPTOCSVConfig():
    def __init__(self):
        pass


class FTPTOGSConfig():
    def __init__(self):
        self._tmp_local_path = '/tmp/'
        self._tmp_filename = None
        self._delimiter = '§'
        self._include_headers = True
        self._quote_char = '"'
        self._retain_local = False

    @property
    def tmp_filename(self):
        return self._tmp_filename

    @tmp_filename.setter
    def tmp_filename(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_filename must be set to a String Value')
        self._tmp_filename = value

    @property
    def tmp_local_path(self):
        return self._tmp_local_path

    @tmp_local_path.setter
    def tmp_local_path(self, value):
        if not isinstance(value, str):
            raise TypeError('tmp_local_path must be set to a String Value')
        self._tmp_local_path = value

    @property
    def delimiter(self):
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value):
        if not isinstance(value, str):
            raise TypeError('delimiter must be set to a String Value')
        self._delimiter = value

    @property
    def include_headers(self):
        return self._include_headers

    @include_headers.setter
    def include_headers(self, value):
        if not isinstance(value, bool):
            raise TypeError('include_headers must be set to a Boolean Value')
        self._include_headers = value

    @property
    def quote_char(self):
        return self._quote_char

    @quote_char.setter
    def quote_char(self, value):
        if not isinstance(value, str):
            raise TypeError('quote_char must be set to a String Value')
        self._quote_char = value

    @property
    def retain_local(self):
        return self._retain_local

    @retain_local.setter
    def retain_local(self, value):
        if not isinstance(value, bool):
            raise TypeError('retain_local must be set to a Boolean Value')
        self._retain_local = value
