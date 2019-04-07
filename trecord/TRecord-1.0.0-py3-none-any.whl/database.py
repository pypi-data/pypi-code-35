from abc import ABC, abstractmethod
import re
from tablib import Dataset


class Database(ABC):
    """A base database client class with default DB API 2 implementations
    """
    def __init__(self) -> None:
        super().__init__()
        self.connection = None
        self.database_url: DatabaseURL = None
        self.read_keywords = ['select']
        self.write_keywords = ['insert', 'update', 'delete', 'merge']

    @abstractmethod
    def connect(self, database_url: str):
        """Create a connection to the database.

        The database url has this form as SQLAlchemy does:
        dialect+driver://username:password@host:port/database

        Check the following link for examples:
        https://docs.sqlalchemy.org/en/latest/core/engines.html

        :param database_url: the database url
        :return: None, should set up the instance variable self.connection though
        """
        self.database_url = DatabaseURL(database_url)
        self.connection = None

    def read(self, query: str, limit: int = None) -> Dataset:
        """Run a read(select) query to the database.

        It should return a list of tuples,
        the first tuple is metadata, each element is a tuple of column name and data type,
        the rest are the records.

        :param query: the sql query
        :param limit: the maximum number of records to return
        :return: a list of tuples
        """
        data = Dataset()
        cursor = self.connection.cursor()
        query = self.add_row_limit_in_query(query, limit)
        cursor.execute(query)
        result = cursor.fetchall()

        if cursor.description:
            data.headers = ['{0}({1})'.format(d[0], self.get_data_type(d[1])) for d in cursor.description]
        data.extend(result)
        cursor.close()

        return data

    @abstractmethod
    def add_row_limit_in_query(self, query, limit):
        """This adds a filter into the query to limit the number of rows.
        It depends on the specific database SQL.
        This is for performance consideration that fetchmany does not work well with large data set.

        Such as to add a limit 10 or top 10 into the query if it does not have it.
        """
        pass

    def write(self, query: str) -> int:
        """Run a write(insert, update, delete) query to the database.

        :param query: the sql query
        :return: number of rows affected
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.rowcount

    def query(self, query: str, limit: int = None):
        """
        Dispatch to read or write accordingly.
        Sub classes should wrapper it around to transfer errors to TRecordError.

        :param query: the sql query
        :param limit: the maximum number of records to return
        :return: what read or write should return
        """
        first_key_word = re.split(r'\s+', query.strip().lower(), 1)[0]
        if first_key_word in self.read_keywords:
            return self.read(query, limit)
        elif first_key_word in self.write_keywords:
            return self.write(query)
        else:
            return self.read(query)

    @abstractmethod
    def get_version(self) -> str:
        pass

    @abstractmethod
    def get_current_db(self) -> str:
        pass

    @abstractmethod
    def get_tables(self, database=None) -> list:
        pass

    @abstractmethod
    def get_ddl(self, table, database=None):
        pass

    @abstractmethod
    def get_data_type(self, type_code: int) -> str:
        """
        Check the type code and return a string description
        :param type_code:
        :return:
        """
        pass

    def close(self):
        self.connection.close()


class DatabaseURL:
    """This class is mainly to extract database url into individual elements"""
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.dialect = None
        self.driver = None
        self.username = None
        self.password = None
        self.host = None
        self.port = None
        self.database = None
        self.extract_info()

    def extract_info(self):
        """
        Extract elements from database url: dialect+driver://username:password@host:port/database
        :return:
        """
        pattern = re.compile(r'([a-z]+)\+?([a-z]+)?://([a-zA-Z0-9_]+):(.+?)@([a-zA-Z0-9._]+):?([0-9]+)?/?([a-zA-Z0-9_]+)?')
        m = pattern.match(self.database_url)
        if m:
            self.dialect, self.driver, self.username, self.password, self.host, self.port, self.database = m.groups()
        else:
            raise RuntimeError('The database url is invalid.')

    def __str__(self) -> str:
        return self.database_url


if __name__ == '__main__':
    u = DatabaseURL('mysql://scott:tiger~*&%@$_+@localhost/foo')
    print(u.dialect, u.driver, u.username, u.password, u.host, u.port, u.database)
