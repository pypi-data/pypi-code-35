import traceback
from typing import Optional

import pandas
import sqlalchemy

from ips_common.logging import log
from ips_common.config.configuration import Configuration

eng = None

config = Configuration().cfg['database']

username = config['user']
password = config['password']
database = config['database']
server = config['server']

connection_string = f"mysql+pymysql://{username}:{password}@{server}/{database}"


def get_sql_connection():
    """
    Author       : Thomas Mahoney / Nassir Mohammad (edits)
    Date         : 11 / 07 / 2018
    Purpose      : Establishes a connection to the SQL Server database and returns the connection object.
    Parameters   : in_table_name - the IPS survey records for the period.
                   credentials_file  - file containing the server and login credentials used for connection.
    Returns      : a pyodbc connection object.
    Requirements : NA
    Dependencies : NA
    """

    global eng

    if eng is not None:
        return eng

    # Get credentials and decrypt

    try:
        engi = sqlalchemy.create_engine(connection_string)
        eng = engi
        return engi
    except Exception as err:
        log.error(f"get_sql_connection failed: {err}")
        raise err


def clear_memory_table(table_name: str) -> None:
    """
    Author        : Elinor Thorne
    Date          : 7 Dec 2017
    Purpose       : Generic SQL query to drop table
    Parameters    : table_name - name of table to drop
    Returns       : True/False (bool)
    Requirements  : None
    Dependencies  : check_table()
                  : get_sql_connection()
                  : database_logger()
    """

    try:
        conn = get_sql_connection()
        conn.execute(f"ALTER TABLE {table_name} ENGINE=MEMORY")
    except Exception as err:
        log.error(f"Clear memory_table failed: {err}")
        raise err


def drop_table(table_name: str) -> None:
    """
    Author        : Elinor Thorne
    Date          : 7 Dec 2017
    Purpose       : Generic SQL query to drop table
    Parameters    : table_name - name of table to drop
    Returns       : True/False (bool)
    Requirements  : None
    Dependencies  : check_table()
                  : get_sql_connection()
                  : database_logger()
    """

    try:
        conn = get_sql_connection()
        conn.execute("DROP TABLE IF EXISTS " + table_name)
    except Exception as err:
        log.error(f"drop_table failed: {err}")
        raise err


def delete_from_table(table_name: str, condition1: str = None, operator: str = None,
                      condition2: str = None, condition3: str = None) -> None:
    """
    Author         : Elinor Thorne
    Date           : 7 Dec 2017
    Purpose        : Generic SQL query to delete contents of table
    Parameters     : table_name - name of table
                     condition1 - first condition / value
                     operator - comparison operator i.e
                     '=' Equal
                     '!=' Not Equal
                     '>' Greater than
                     '>=' Greater than or equal, etc
                     https://www.techonthenet.com/oracle/comparison_operators.php
                     condition2 - second condition / value
                     condition3 - third condition / value used for BETWEEN
                     ranges, i.e: "DELETE FROM table_name WHERE condition1
                     BETWEEN condition2 AND condition3"
    Returns         : True/False (bool)
    Requirements    : None
    Dependencies    : check_table(),
                      get_sql_connection,
    """

    if condition1 is None:
        query = ("DELETE FROM " + table_name)
    elif condition3 is None:
        query = ("DELETE FROM " + table_name
                 + " WHERE " + condition1
                 + " " + operator
                 + " '" + condition2 + "'")
    else:
        query = ("DELETE FROM " + table_name
                 + " WHERE " + condition1
                 + " " + operator
                 + " '" + condition2 + "'"
                 + " AND " + condition3)

    try:
        conn = get_sql_connection()
        conn.execute(query)
    except Exception as err:
        traceback.print_exc()
        log.error(f"delete_from_table failed: {err}")
        raise err


def select_data(column_name: str, table_name: str, condition1: str, condition2: str) -> Optional[pandas.DataFrame]:
    """
    Author        : Elinor Thorne
    Date          : 21 Dec 2017
    Purpose       : Uses SQL query to retrieve values from database
    Parameters    : column_name, table_name, condition1, condition2, i.e:
                  : "SELECT column_name FROM table_name WHERE condition1 = condition2" (no 'AND'/'OR' clause)
    Returns       : Data Frame for multiple values, scalar/string for single values
    Requirements  : None
    """

    query = f"""
        SELECT {column_name} 
        FROM {table_name}
        WHERE {condition1} = '{condition2}'
        """

    try:
        return pandas.read_sql_query(query, con=connection_string)
    except Exception as err:
        log.error(f"select_data failed: {err}")
        raise err


def get_table_values(table_name: str) -> pandas.DataFrame:
    """
    Author       : Thomas Mahoney
    Date         : 02 Jan 2018
    Purpose      : Extracts a full table into a pandas dataframe
    Params       : table_name - the name of the target table in the sql database.
    Returns      : Dataframe containing the extracted table data.
    Requirements : NA
    Dependencies : NA
    """

    try:
        return pandas.read_sql_table(table_name=table_name, con=connection_string)
    except Exception as err:
        log.error(f"get_table_values failed: {err}")
        raise err


def insert_dataframe_into_table(table_name: str,
                                dataframe: pandas.DataFrame,
                                if_exists='append') -> None:
    """
    Author       : Thomas Mahoney
    Date         : 02 Jan 2018
    Purpose      : Inserts a full dataframe into a SQL table
    Params       : table_name - the name of the target table in the sql database.
                   dataframe - the dataframe to be added to the selected table.
    Returns      : The number of rows added to the database.
    Requirements : NA
    Dependencies : NA
    """

    dataframe = dataframe.where((pandas.notnull(dataframe)), None)
    dataframe.columns = dataframe.columns.astype(str)

    try:
        dataframe.to_sql(table_name, con=connection_string, if_exists=if_exists,
                         chunksize=5000, index=False)
    except Exception as err:
        log.error(f"insert_dataframe_into_table failed: {err}")
        raise err


def execute_sql_statement(sq):
    try:
        conn = get_sql_connection()
        return conn.execute(sq)
    except Exception as err:
        log.error(f"execute_sql_statement failed: {err}")
        raise err
