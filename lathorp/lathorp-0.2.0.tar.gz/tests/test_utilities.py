import pathlib

import psycopg2.extras
import pytest

import lathorp


@pytest.fixture
def clear_schema(pg):
    """Removes tables prior to tests."""
    with psycopg2.connect(**pg.dsn()) as conn:
        with conn.cursor() as cursor:
            cursor.execute('DROP TABLE IF EXISTS test_table;')
            cursor.execute('DROP TABLE IF EXISTS another_table;')


def test_load_schema_definitions_file(pg, clear_schema):
    """Tests that the helper function loads data definitions from a file."""
    path = pathlib.Path(__file__) / '..' / 'pg_ddl' / 'test_table.sql'
    lathorp.load_schema_definitions(pg.dsn(), path)
    query = '''SELECT * FROM pg_catalog.pg_tables
               WHERE schemaname = 'public'
               AND tablename = %s;'''
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


def test_load_schema_definitions_dir(pg, clear_schema):
    """Tests that the helper function loads data definitions from a directory.

    Data definitions are expected to load from all the files directly under the directory.
    """
    query = '''SELECT tablename FROM pg_catalog.pg_tables
               WHERE schemaname = 'public'
               ORDER BY tablename;'''
    path = pathlib.Path(__file__) / '..' / 'pg_ddl'
    lathorp.load_schema_definitions(pg.dsn(), path)
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
        lathorp.load_schema_definitions(pg.dsn(), path)


def test_copy_data_file(pg, init_schema):
    """Tests that copy_data can load data from a file into the database."""
    path = pathlib.Path(__file__) / '..' / 'pg_data' / '001_test_table.csv'
    assert path.resolve().is_file()
    with psycopg2.connect(**pg.dsn()) as conn:
        lathorp.copy_data(conn, path)
        with conn.cursor() as cursor:
            cursor.execute('SELECT num FROM test_table;')
            assert cursor.fetchall() == [(1001, ), (1002, ), (1003, ), (None, ), (1005, )]
            # Clean up for the next tests
            cursor.execute('TRUNCATE test_table CASCADE;')


def test_copy_data_dir(pg, init_schema):
    """Tests that copy_data can load data from all files in a directory."""
    path = pathlib.Path(__file__) / '..' / 'pg_data'
    assert path.resolve().is_dir()
    assert len(list(path.resolve().iterdir())) > 1
    with psycopg2.connect(**pg.dsn()) as conn:
        lathorp.copy_data(conn, path)
        with conn.cursor() as cursor:
            cursor.execute('SELECT num FROM test_table;')
            assert cursor.fetchall() == [(1001, ), (1002, ), (1003, ), (None, ), (1005, ),
                                         (2001, ), (2002, ), (2003, ), (None, ), (2005, )]
            # Clean up for the next tests
            cursor.execute('TRUNCATE test_table CASCADE;')


def test_copy_data_raises_on_invalid_path(pg):
    """Tests copy_data fixture with exceptional conditions.

    The function is expected to raise a ValueError when given invalid paths, or paths that
    contain files whose names are in an unexpected format.
    """
    with psycopg2.connect(**pg.dsn()) as conn:
        # The file name is in the wrong format:
        with pytest.raises(ValueError):
            lathorp.copy_data(conn, pathlib.Path(__file__))
        # Missing path:
        path = pathlib.Path(__file__) / 'nosuchpath'
        assert not path.exists()
        with pytest.raises(ValueError):
            lathorp.copy_data(conn, path)


def test_delete_data(pg, init_schema):
    """Tests that delete_data removes all data from specified tables."""
    path = pathlib.Path(__file__) / '..' / 'pg_data' / '001_test_table.csv'
    with psycopg2.connect(**pg.dsn()) as conn:
        lathorp.copy_data(conn, path)
        with conn.cursor() as cursor:
            cursor.execute('SELECT count(*) FROM test_table;')
            assert cursor.fetchone()[0] == 5
        lathorp.delete_data(conn, {'test_table'})
        with conn.cursor() as cursor:
            cursor.execute('SELECT count(*) FROM test_table;')
            assert cursor.fetchone()[0] == 0
