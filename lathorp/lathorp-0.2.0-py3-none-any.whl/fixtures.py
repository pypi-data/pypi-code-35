"""Helpful fixtures for testing with pytest and PostgreSQL.

Use these fixtures to test code that requires access to a PostgreSQL database.
"""
import pathlib
from typing import Callable, Generator, Union

import psycopg2
import psycopg2.extensions
import psycopg2.sql
import pytest
import testing.postgresql

import lathorp


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
            tables = lathorp.copy_data(conn, data_path)

        def finalize():
            lathorp.delete_data(conn, tables)
            conn.close()

        request.addfinalizer(finalize)

        return conn

    return connector
