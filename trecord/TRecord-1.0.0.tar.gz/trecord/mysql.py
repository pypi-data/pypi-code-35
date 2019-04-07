from trecord.database import Database
from trecord.error import TRecordError
import pymysql
import re


class PyMySQL(Database):
    """This class implements the database using PyMySQL"""
    def __init__(self) -> None:
        super().__init__()

    def connect(self, database_url: str):
        super().connect(database_url)
        self.connection = pymysql.connect(host=self.database_url.host,
                                          user=self.database_url.username,
                                          password=self.database_url.password,
                                          db=self.database_url.database,
                                          charset='utf8mb4')

    def query(self, query: str, limit: int = None):
        try:
            result = super().query(query, limit)
            return result
        except pymysql.Error as err:
            raise TRecordError(err)

    def add_row_limit_in_query(self, query, limit):
        if limit and not re.search(r'\s+limit\s+', query, re.IGNORECASE):
            query = query.strip(' ;') + ' limit {};'.format(limit)
        return query

    def get_data_type(self, type_code: int) -> str:
        """
        Check the type code and return a string description
        :param type_code:
        :return:
        """
        mapping = {
            pymysql.STRING: 'STRING',
            pymysql.BINARY: 'BINARY',
            pymysql.NUMBER: 'NUMBER',
            pymysql.DATE: 'DATE',
            pymysql.TIME: 'TIME',
            pymysql.TIMESTAMP: 'TIMESTAMP',
            pymysql.ROWID: 'ROWID'
        }
        for key in mapping.keys():
            if type_code == key:
                return mapping[key]

    def get_version(self) -> str:
        return self.query('select version()')[0][0]

    def get_current_db(self) -> str:
        db = self.query('select database()')[0][0]
        if not db:
            db = ''
        return db

    def get_tables(self, database=None) -> list:
        if database:
            return list(
                self.query("select table_name "
                           "from information_schema.tables "
                           "where TABLE_SCHEMA='{}';".format(database)).get_col(0)
            )
        else:
            return list(self.query('show tables;').get_col(0))

    def get_ddl(self, table, database=None):
        if not database:
            database = self.get_current_db()
        return self.query('show create table {}.{};'.format(database, table))[0][1]


if __name__ == '__main__':
    sql = PyMySQL()
    sql.connect('mysql+pymysql://lusaisai:lusaisai@198.58.115.91/employees')
    print(sql.get_version())
    print(sql.get_current_db())
    print(sql.get_tables())
    print(sql.get_ddl('employees'))
    print(sql.query('select * from departments;', 5))
    print(sql.query('select * from employees;', 20))
