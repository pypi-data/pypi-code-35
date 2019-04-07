from trecord.database import Database
from trecord.error import TRecordError
import pyodbc
import re
from datetime import datetime, date


class PyODBCMSSQL(Database):
    """This class implements the database using PyMySQL"""

    def __init__(self) -> None:
        super().__init__()

    def connect(self, database_url: str):
        super().connect(database_url)
        self.connection = pyodbc.connect(
                f'DSN={self.database_url.host};UID={self.database_url.username};PWD={self.database_url.password}'
            )
        if self.database_url.database:
            self.write("USE {}".format(self.database_url.database))

    def query(self, query: str, limit: int = None):
        try:
            result = super().query(query, limit)
            return result
        except pyodbc.Error as err:
            raise TRecordError(err)

    def add_row_limit_in_query(self, query, limit):
        if limit and not re.search(r'\s+top\s+', query, re.IGNORECASE):
            query = re.sub(r'^select\s+', 'select top {} '.format(limit), query)
        return query

    def get_data_type(self, type_code: int) -> str:
        """
        Check the type code and return a string description
        :param type_code:
        :return:
        """
        if type_code is int:
            return 'INTEGER'
        elif type_code is bool:
            return 'BOOLEAN'
        elif type_code is datetime:
            return 'DATETIME'
        elif type_code is date:
            return 'DATE'

        mapping = {
            pyodbc.STRING: 'STRING',
            pyodbc.BINARY: 'BINARY',
            pyodbc.NUMBER: 'NUMBER',
            pyodbc.Date: 'DATE',
            pyodbc.Time: 'TIME',
            pyodbc.Timestamp: 'TIMESTAMP'
        }
        for key in mapping.keys():
            if type_code is key:
                return mapping[key]
            else:
                return str(type_code)

    def get_version(self) -> str:
        return self.query('SELECT @@VERSION')[0][0]

    def get_current_db(self) -> str:
        return self.query('SELECT DB_NAME()')[0][0]

    def get_tables(self, database=None) -> list:
        if not database:
            database = self.get_current_db()
        return list(
            self.query("select table_name "
                       "from {}.information_schema.tables;".format(database)).get_col(0)
        )

    def get_ddl(self, table, database=None):
        if not database:
            database = self.get_current_db()
        ddl = ''
        ddl += self.query(
            "select table_catalog, table_schema, table_name, column_name, data_type, character_maximum_length, "
            "numeric_precision, numeric_scale from {}.INFORMATION_SCHEMA.COLUMNS "
            "where table_name = '{}' order by ordinal_position;".format(database, table)).__str__()

        ddl += '\n\n'

        constraints_query = """SELECT
            constraint_name, ordinal_position, table_name, column_name, is_unique, is_primary_key
            FROM {}.INFORMATION_SCHEMA.KEY_COLUMN_USAGE k
            JOIN SYS.INDEXES i
            ON   k.constraint_name = i.name
            WHERE table_name = '{}'
            ORDER BY constraint_name, ordinal_position
            """.format(database, table)
        ddl += self.query(constraints_query).__str__()

        return ddl


if __name__ == '__main__':
    import sys

    sql = PyODBCMSSQL()
    sql.connect(sys.argv[1])
    print(sql.get_version())
    print(sql.get_current_db())
    print(sql.get_ddl('vw_eBay_NiceLinksForSurvey'))
    print(sql.get_ddl('tblREScorecardRule'))
