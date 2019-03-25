import pytest
from webtest import TestApp

from test.conftest import app


@pytest.fixture(scope='function')
def api_client():
    client = TestApp(app)
    yield client


def test_json_response(api_client):
    result = api_client.get('/index')
    assert result.status_int == 200


def test_cors_response(api_client):
    result = api_client.get('/documents')
    print(result._headers)
    assert 'Access-Control-Allow-Origin' in result._headers
