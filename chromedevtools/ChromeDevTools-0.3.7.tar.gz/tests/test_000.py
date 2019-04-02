import asyncio
import logging

import aiohttp
import pytest

from ChromeDevTools import ChromeDevTools, logger


logging.basicConfig(level=logging.DEBUG)
# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


async def test_new_tab(event_loop):
  async with aiohttp.ClientSession(loop=event_loop) as session:
    devtools = ChromeDevTools(session, loop=event_loop)
    tab = await devtools.new_tab('http://example.org/')
    # Ждем пока загрузится страница
    await tab.wait(5)
    r = await tab.runtime.evaluate(expression='document.domain')
    logger.debug(r)
    assert r.result.result.type == 'string'
    assert r.result.result.value == 'example.org'
