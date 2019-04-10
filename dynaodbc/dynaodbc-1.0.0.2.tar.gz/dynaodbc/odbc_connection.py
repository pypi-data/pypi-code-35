"""
Module holding ODBCConnection class.

Tools to connect to SQL databases via ODBC.

"""

import pyodbc

from dynaodbc._dyna_odbc_const import _ErrFmts

class ODBCConnection:
    """
    Wrapper class containing ODBC connection

    Fields:
    - driver: ODBC driver to use
    - server: SQL server to connect to
    - database: SQL DB to use
    - username: DB username
    - password: DB password
    - cursor: pyodbc cursor object

    Methods:
    - connect
    - close

    """
    def __init__(self, driver, server, database, username, password):
        """
        Connects to a SQL database and returns new ODBCConnection

        Args:
        - driver: ODBC driver to use
        - server: SQL server to connect to
        - database: SQL DB to use
        - username: DB username
        - password: DB password

        """
        if not isinstance(driver, str):
            raise AttributeError(_ErrFmts.errmsg_invalid_db_driver % db_driver)

        if not isinstance(server, str):
            raise AttributeError(_ErrFmts.errmsg_invalid_db_server % db_server)

        if not isinstance(database, str):
            raise AttributeError(_ErrFmts.errmsg_invalid_db_database % db_database)

        if not isinstance(username, str):
            raise AttributeError(_ErrFmts.errmsg_invalid_db_username % db_username)

        if not isinstance(password, str):
            raise AttributeError(_ErrFmts.errmsg_invalid_db_password)

        self.driver = driver
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self._connection = None
        self.cursor = None

    def connect(self):
        """
        Connect to the configured SQL database
        """
        try:
            self._connection = pyodbc.connect(
                'DRIVER={' + self.driver +
                '};SERVER=' + self.server +
                ';DATABASE=' + self.database +
                ';UID=' + self.username +
                ';PWD=' + self.password
            )
            self.cursor = self._connection.cursor()
        except Exception as exc:
            raise RuntimeError(_ErrFmts.errmsg_db_connect % exc)

    def close(self):
        """
        Close the ODBC connection
        """
        try:
            if self.cursor is not None:
                self.cursor.close()
            if self._connection is not None:
                self._connection.close()
        except Exception as exc:
            raise RuntimeError(_ErrFmts.errmsg_db_close % exc)