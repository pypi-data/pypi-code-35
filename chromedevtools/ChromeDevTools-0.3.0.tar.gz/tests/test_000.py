import asyncio

import aiohttp
import pytest

from ChromeDevTools import ChromeDevTools

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


async def test_new_tab(event_loop):
  async with aiohttp.ClientSession(loop=event_loop) as session:
    chrome = ChromeDevTools(session, loop=event_loop)
    tab = await chrome.new_tab('http://example.org/')
    rpc = await chrome.connect_tab(tab['webSocketDebuggerUrl'])
    # Ждем пока загрузится страница
    await asyncio.sleep(5)
    r = await rpc.runtime.evaluate(expression='document.domain')
    print(r)
    assert r.result.result.type == 'string'
    assert r.result.result.value == 'example.org'
