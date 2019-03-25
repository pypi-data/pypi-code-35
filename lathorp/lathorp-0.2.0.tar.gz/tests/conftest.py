import pathlib

import pytest

from lathorp import load_schema_definitions
# Import the fixtures to make them available to the tests
from lathorp.fixtures import pg  # noqa: F401
from lathorp.fixtures import pg_connect  # noqa: F401


@pytest.fixture(scope='module')
def init_schema(pg):  # noqa: F811
    """Loads the schema definition from a known location.

    This session-scoped fixture can be used together with the function-scoped `pg_connect`
    in order to load the schema definition just once per test session yet allow `pg_connect`
    to copy test data into that schema and then remove it for each test function.
    """
    path = (pathlib.Path(__file__) / '..' / 'pg_ddl').resolve()
    assert path.is_dir()
    load_schema_definitions(pg.dsn(), path)
