from trecord.mssql import PyODBCMSSQL
from trecord.mysql import PyMySQL
from trecord.oracle import CxOracle
from trecord.database import DatabaseURL, Database
from trecord.error import TRecordError
from trecord.command import Command


def get_database_by_url(url: str):
    db_url = DatabaseURL(url)
    if db_url.dialect == 'mssql':
        db = PyODBCMSSQL()
    elif db_url.dialect == 'mysql':
        db = PyMySQL()
    elif db_url.dialect == 'oracle':
        db = CxOracle()
    else:
        raise NotImplementedError('The database is not implemented yet.')

    db.connect(url)
    return db
