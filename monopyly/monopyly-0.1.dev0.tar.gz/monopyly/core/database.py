import datetime
import getpass
import pandas as pd
import seaborn as sns
import MySQLdb

def connect_to_database(default_file='~/.my.cnf', database='credit_cards'):
    """Attempt to connect to the local MySQL database.

    Try connecting to the local MySQL database using the default file. If
    unsuccessful, prompt the user to enter their information.

    Parameters
    ––––––––––
    default_file : str, optional
        The name (and path) of the default file to read for MySQL configuration
        information. (The default is '~/.my.cnf'.)
    db : str, optional
        The name of the MySQL database to access.

    Returns
    –––––––
    cursor : Cursor object
        A MySQLdb cursor object linking to the MySQL database for performing
        queries.
    """
    try:
        # Attempt connecting with the default file
        conn = MySQLdb.connect(read_default_file=default_file,
                               db=database)
    except MySQLdb.OperationalError:
        # Credentials weren't accepted, so prompt the user for info
        conn = MySQLdb.connect(user=input('Username: '),
                               passwd=getpass.getpass('Password: '),
                               db=database)
    cursor = conn.cursor()
    return cursor

def load_dataframe(cursor, col_order=None, col_types={}, order_by=None):
    """
    Create a dataframe from the returned values of a cursor object.

    Loads the result of a MySQL database query, accessed using the cursor, into
    a pandas dataframe. The loading process ensures that dates are loaded as
    Python datetime objects, currency values are loaded as floating point
    numbers, all entries are sorted by transaction date, and then the columns
    of the dataframe are stored in order (specifically: card, transaction date,
    vendor, price, notes, and statement date).

    Parameters
    ––––––––––
    cursor : Cursor object
        A MySQLdb Cursor that has executed a query on a database.
    col_order : list of str, optional
        The order of the columns (left to right) to use when organizing the
        dataframe.
    col_types : dict, optional
        A dictionary giving the type to use for each column read in from the
        database. Keys are column names, values are data types. (The default
        type is `str`, unless the column name includes 'date' in which it is
        converted to a Python datetime object.)
    order_by : list of str, optional
        Column(s) that are used to sort the loaded dataframe. Dataframe ordered
        by columns successively as given.

    Returns
    –––––––
    df : DataFrame
        A dataframe with the transaction history stored in the database.
    """
    # Load database data into dataframe
    result = []
    columns = tuple([item[0] for item in cursor.description])
    for row in cursor:
        result.append(dict(zip(columns, row)))
    df = pd.DataFrame(result)
    if col_order is not None:
        df = df[col_order]
    # Set dates to datetime objects unless otherwise specified
    for col in columns:
        if 'date' in col and col not in col_types:
            col_types[col] = datetime.datetime
    # Format data to proper types
    for col in col_types:
        if col_types[col] is datetime.datetime:
            df[col] = pd.to_datetime(df[col])
        else:
            df[col] = df[col].astype(col_types[col])
    if order_by is not None:
        df.sort_values(by=order_by, inplace=True)
    return df
