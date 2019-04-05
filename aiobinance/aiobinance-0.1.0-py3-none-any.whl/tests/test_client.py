import asyncio
from unittest.mock import patch

import pytest
from asynctest import CoroutineMock

from aiobinance import Client
from aiobinance.modules.account import Account
from aiobinance.modules.general import General
from aiobinance.modules.market import Market
from aiobinance.modules.stream import Stream
from aiobinance.network import Network


@pytest.fixture()
async def client():
    loop = asyncio.get_event_loop()
    c = Client('key', 'secret', loop=loop, timeout=55)
    yield c
    await c.close()


def test_api_key():
    with pytest.raises(TypeError):
        c = Client()


@pytest.mark.asyncio
async def test_client_init(client):
    assert isinstance(client._http, Network)
    assert client._http._API_KEY == 'key'
    assert client._http._API_SECRET == 'secret'
    assert client._http._session._timeout.total == 55


@pytest.mark.asyncio
async def test_loop():
    loop = asyncio.get_event_loop()
    c = Client('key', 'secret', loop=loop)
    assert c._http._loop == loop
    assert c._http._session._loop == loop


@pytest.mark.asyncio
async def test_modules_init(client):
    assert isinstance(client.account, Account)
    assert isinstance(client.general, General)
    assert isinstance(client.market, Market)
    assert isinstance(client.stream, Stream)


@pytest.mark.asyncio
async def test_close_session(client):
    with patch('aiobinance.network.Network.close', new_callable=CoroutineMock) as m:
        await client.close()
        m.assert_called_once_with()
