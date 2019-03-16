import pathlib

import psycopg2.extras
import pytest

from lathorp.fixtures import load_schema_definitions


def test_pg_is_connectable(pg):
    """Tests that the pg fixtures yields a connectable database."""
    # A failure to connect would raise an exception and the test would fail
    psycopg2.connect(**pg.dsn())


def test_load_schema_definitions_file(pg):
    """Tests that the helper function loads data definitions from a file."""
    query = '''SELECT * FROM pg_catalog.pg_tables
               WHERE schemaname = 'public'
               AND tablename = %s;'''
    path = pathlib.Path(__file__) / '..' / 'pg_ddl' / 'test_table.sql'
    load_schema_definitions(pg, path)
    with psycopg2.connect(**pg.dsn()) as conn:
        with conn.cursor() as cursor:
            # Check that the `test_table` table exists
            cursor.execute(query, ('test_table', ))
            assert cursor.fetchone() is not None
            # Check that a non-existing tables yield nothing
            cursor.execute(query, ('another_table', ))
            assert cursor.fetchone() is None
            # Clean-up
            cursor.execute('DROP TABLE IF EXISTS test_table;')


def test_load_schema_definitions_dir(pg):
    """Tests that the helper function loads data definitions from a directory.

    Data definitions are expected to load from all the files directly under the directory.
    """
    query = '''SELECT tablename FROM pg_catalog.pg_tables
               WHERE schemaname = 'public'
               ORDER BY tablename;'''
    path = pathlib.Path(__file__) / '..' / 'pg_ddl'
    load_schema_definitions(pg, path)
    with psycopg2.connect(**pg.dsn()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            assert cursor.fetchall() == [('another_table', ), ('test_table', )]
            # Clean-up
            cursor.execute('DROP TABLE IF EXISTS another_table;')
            cursor.execute('DROP TABLE IF EXISTS test_table;')


def test_load_schema_definitions_raises_on_invalid_def_path(pg):
    """Tests the helper function with exceptional conditions.

    The function is expected to raise a ValueError when given an invalid definitions path.
    """
    path = pathlib.Path(__file__) / 'nosuchpath'
    assert not path.exists()
    with pytest.raises(ValueError):
        load_schema_definitions(pg, path)


def test_pg_connect_is_usable(pg_connect):
    """Tests that the pg_connect fixture yields a usable connection function to the database."""
    conn = pg_connect()
    with conn.cursor() as cursor:
        cursor.execute("SELECT 'Hello, world!';")
        assert cursor.fetchone()[0] == 'Hello, world!'


def test_pg_connect_sets_cursor_factory(pg_connect):
    """Tests that the option to set the cursor factory for the connection via the fixture."""
    conn = pg_connect(cursor_factory=psycopg2.extras.NamedTupleCursor)
    with conn.cursor() as cursor:
        cursor.execute("SELECT 'Hello, world!' AS hello;")
        result = cursor.fetchone()
        assert result[0] == 'Hello, world!'
        assert result.hello == 'Hello, world!'

#
# The following tests use the init_schema fixture defined in conftest.py
# This fixture loads the schema definition so that pg_connect can copy data into those tables.
#


def test_pg_connect_loads_data_file(init_schema, pg_connect):
    """Tests that the pg_connect fixture loads data from a file into the database."""
    # The tested function should call `resolve()` on the path to remove the '..'
    path = pathlib.Path(__file__) / '..' / 'pg_data' / '001_test_table.csv'
    assert path.resolve().is_file()
    conn = pg_connect(data_path=path)
    with conn.cursor() as cursor:
        cursor.execute('SELECT num FROM test_table;')
        assert cursor.fetchall() == [(1001, ), (1002, ), (1003, ), (None, ), (1005, )]


def test_pg_connect_loads_data_dir(init_schema, pg_connect):
    """Tests that the pg_connect fixture loads data from all files in a directory."""
    path = pathlib.Path(__file__) / '..' / 'pg_data'
    assert path.resolve().is_dir()
    assert len(list(path.resolve().iterdir())) > 1
    conn = pg_connect(data_path=path)
    with conn.cursor() as cursor:
        cursor.execute('SELECT num FROM test_table;')
        assert cursor.fetchall() == [(1001, ), (1002, ), (1003, ), (None, ), (1005, ),
                                     (2001, ), (2002, ), (2003, ), (None, ), (2005, )]


def test_pg_connect_raises_on_invalid_path(pg_connect):
    """Tests the pg_connect fixture with exceptional conditions.

    The fixture is expected to raise a ValueError when given invalid paths, or paths that
    contain files whose names are in an unexpected format.
    """
    # The file name is in the wrong format:
    with pytest.raises(ValueError):
        pg_connect(data_path=pathlib.Path(__file__))
    # Missing path:
    path = pathlib.Path(__file__) / 'nosuchpath'
    assert not path.exists()
    with pytest.raises(ValueError):
        pg_connect(data_path=path)


@pytest.mark.parametrize('data_file', ['001_test_table.csv', '002_test_table.txt'])
def test_pg_connect_deletes_data(init_schema, pg_connect, data_file):
    """Tests that the pg_connect fixtures deletes data between test invocations.

    This test is parametrized so that it runs twice, loading a different data file each time.
    It ensures that following each invocation, only data from the current data_file exists in
    the database.
    """
    path = pathlib.Path(__file__) / '..' / 'pg_data' / data_file
    with pg_connect(data_path=path).cursor() as cursor:
        cursor.execute('SELECT num FROM test_table;')
        numbers = [row[0] for row in cursor.fetchall()]
        if data_file == '001_test_table.csv':
            assert numbers == [1001, 1002, 1003, None, 1005]
        elif data_file == '002_test_table.txt':
            assert numbers == [2001, 2002, 2003, None, 2005]
