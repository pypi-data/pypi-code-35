"""Helpful fixtures for testing with pytest and PostgreSQL.

Use these fixtures to test code that requires access to a PostgreSQL database.

The `pg` fixture
"""
import pathlib
import re
from typing import Callable, Generator, List, Set, Union

import psycopg2
import psycopg2.extensions
import psycopg2.sql
import pytest
import testing.postgresql


@pytest.fixture(scope='session')
def pg() -> Generator[testing.postgresql.Postgresql, None, None]:
    """A session-scoped temporary PostgreSQL instance.

    Add this fixture to your test function to get access to a temporary PostgreSQL database.
    Because setting up a temporary database is a costly operation that slow your tests down, this
    fixture is scoped at the session level, so the database is set up only once per testing
    session.

    You can create a connection to the temporary database as follows:
    >> conn = psycopg2.connect(**pg.dsn())

    Yields:
        A temporary database.
    """
    Postgresql = testing.postgresql.PostgresqlFactory(cache_initialized_db=True)
    pg = Postgresql()
    yield pg
    pg.stop()
    Postgresql.clear_cache()


def load_schema_definitions(pg: testing.postgresql.Postgresql, def_path: pathlib.Path) -> List[pathlib.Path]:
    """Loads the data definitions for a new database instance.

    Data definitions include tables and other named objects such as data types and functions.

    The definitions are loaded from files written in SQL data definition language.

    Args:
        pg: An initialized temporary database.
        def_path: A Path to a file or directory that contains the schema definitions to load.
    """
    path = def_path.resolve()
    if path.is_file():
        files = [path]
    elif path.is_dir():
        files = [child for child in sorted(path.iterdir()) if child.is_file()]
    else:
        raise ValueError('def_path must be a valid path to a file or directory.')

    with psycopg2.connect(**pg.dsn()) as conn:
        with conn.cursor() as cursor:
            for file in files:
                cursor.execute(file.read_text())
    return files


Connector = Callable[[Union[pathlib.Path, None], Union[psycopg2.extensions.cursor, None]],
                     psycopg2.extensions.connection]
"""A type alias for the function returned by the pg_conn fixture."""


@pytest.fixture(scope='function')
def pg_connect(request, pg) -> Connector:
    """Returns a function that opens a connection to a temporary PostgreSQL instance.

    To get a connection in your test function, use it like so:
    >> conn = pg_connect(data_path=pathlib.Path('my_path'), cursor_factory=psycopg2.extras.NamedTupleCursor)
    You may also omit any or both arguments:
    >> conn = pg_connect()

    Use the data_path argument to copy test data into the database prior to running your test
    function.
    The data is automatically deleted after the test function is done, so test functions do not leak
    side effects.
    The data_path argument may point to a single data file, or a directory of files.

    Note that a schema definition must be loaded before the data can be copied.
    Use `load_schema_definitions` for that, perhaps together with another session-scoped fixture.
    See `tests/conftest.py::init_schema` for an example.

    Use the cursor_factory argument to specify a cursor factory for the new connection.

    The arguments to the fixture itself are auto-loaded by pytest.
    """
    def connector(data_path=None, cursor_factory=None):
        dsn = psycopg2.extensions.make_dsn(**pg.dsn())
        conn = psycopg2.connect(dsn, cursor_factory=cursor_factory)
        tables = []
        if data_path:
            tables = _copy_data(conn, data_path)

        def finalize():
            _delete_data(conn, tables)
            conn.close()

        request.addfinalizer(finalize)

        return conn

    return connector


def _copy_data(conn: psycopg2.extensions.connection, data_path: pathlib.Path) -> Set[str]:
    """Copies data from the specified path into the database.

    You can provide a single file, or a directory.
    In the latter case, the function copies data from every file directly under that directory.
    The files are loaded in alphabetical order.

    File names *must* contain the name of the target table, optionally with a leading number and
    optionally with the trailing word "data", separted from the table name by underscores ("_").

    The file format *must* be supported by the PostgreSQL COPY FROM command.

    The file name extension determines the file format. It *must* be one of:
    1. .txt, .text - text format
    2. .csv - CSV format
    3. .bin, .binary - binary format

    For example, if the target table is called "table1", all the following are valid file names:
    * table1.csv
    * 1_table1.bin
    * 017_table1.text

    Args:
        conn: An open connection to the database.
        data_path: A Path to a file or directory that contains the data to load.

    Returns:
        The tables that data were loaded into.
    """
    def parse_name(path):
        """Returns a triplet: (file name, table name, file format)."""
        # The regular expression does not match exactly the SQL rules for valid table names.
        # I decided to leave it like that for now, for the sake of simplicity.
        match = re.fullmatch(r'(?:\d+_)?(\w+)\.(te?xt|csv|bin(?:ary)?)', path.name, re.IGNORECASE)
        if match:
            format = match.group(2).lower()
            format = {'txt': 'text', 'bin': 'binary'}.get(format, format)
            return path, match.group(1), format
        raise ValueError(f'{path.name} has an unexpected format.')

    path = data_path.resolve()
    if path.is_file():
        files = [parse_name(path)]
    elif path.is_dir():
        files = [parse_name(child) for child in sorted(path.iterdir()) if child.is_file()]
    else:
        raise ValueError('data_path must be a valid path to a file or directory.')

    with conn:
        with conn.cursor() as cursor:
            for file, table, format in files:
                sql = psycopg2.sql.SQL('COPY {table} FROM STDIN WITH (FORMAT {format});').format(
                    table=psycopg2.sql.Identifier(table),
                    format=psycopg2.sql.Literal(format))
                with file.open() as f:
                    cursor.copy_expert(sql, f)
    # Return the tables. Use a set because multiple files may apply to the same table.
    return set(file[1] for file in files)


def _delete_data(conn: psycopg2.extensions.connection, tables: Set[str]) -> None:
    """Deletes all the data from the specified tables."""
    if tables:
        with conn:
            with conn.cursor() as cursor:
                sql = psycopg2.sql.SQL('TRUNCATE {tables} CASCADE;').format(
                    tables=psycopg2.sql.SQL(', ').join(psycopg2.sql.Identifier(table) for table in tables))
                cursor.execute(sql)
