# https://chromedevtools.github.io/devtools-protocol/
# Первоначально я наткнулся на такое решение
# `https://github.com/marty90/PyChromeDevTools/`, но мне оно не
# подходило из-за блокирующих операций. Про puppeteer я знал, но свой
# велосипед удобнее.
import asyncio
import json
from typing import Any, Callable, List, Mapping, Optional, Union
from urllib.parse import quote_plus, urljoin

import aiohttp

from .datatypes import AttrDict
from .log import logger
from .utils import camelize

__all__ = ('ChromeDevTools', 'Tab', 'Domain')


class ChromeDevTools:

  def __init__(
    self,
    session: aiohttp.ClientSession = None,
    *,
    host: Optional[str] = 'localhost',
    port: Optional[int] = 9222,
    loop: Optional[asyncio.AbstractEventLoop] = None
  ):
    self.loop = loop or asyncio.get_event_loop()
    logger.debug(self.loop)
    self.session = session or aiohttp.ClientSession(loop=self.loop)
    self.host = host
    self.port = port

  async def version(self) -> Mapping[str, Any]:
    r = await self.fetch('version')
    return await r.json()

  async def protocol(self) -> Mapping[str, Any]:
    r = await self.fetch('protocol/')
    return await r.json()

  def _create_tab(self, data: Mapping[str, Any]) -> 'Tab':
    logger.debug(data)
    return Tab(self, data)

  async def new_tab(self, url: str) -> 'Tab':
    r = await self.fetch('new?' + quote_plus(url))
    return self._create_tab(await r.json())

  async def tabs(self) -> List['Tab']:
    r = await self.fetch('list')
    return [self._create_tab(x) for x in (await r.json())]

  async def fetch(self, url: str) -> aiohttp.ClientResponse:
    endpoint = urljoin(self.base_url, url)
    response = await self.session.get(endpoint)
    return response

  async def connect_ws(self, url: str) -> '_WSRequestContextManager':
    logger.debug('connect ws: %s', url)
    ws = await self.session.ws_connect(url)
    # logger.debug(ws)
    return ws

  async def close_session(self):
    await self.session.close()

  @property
  def base_url(self) -> str:
    return f'http://{self.host}:{self.port}/json/'


class Tab:
  TIMEOUT = 15
  SKIPPED_LIMIT = 1000

  def __init__(self, devtools: ChromeDevTools, data: Mapping[str, Any]):
    self.devtools = devtools
    self.id = data['id']
    self.url = data['url']
    self.title = data['title']
    self.ws_url = data['webSocketDebuggerUrl']
    self.raw = data
    self.ws = None
    self._id = 0
    self._skipped = []

  async def activate(self) -> str:
    r = await self.devtools.fetch(f'activate/{self.id}')
    return await r.text()

  async def close(self) -> str:
    r = await self.devtools.fetch(f'close/{self.id}')
    # disconnect?
    return await r.text()

  async def connect(self):
    self.ws = await self.devtools.connect_ws(self.ws_url)

  @property
  def connected(self) -> bool:
    return False if self.ws is None else not self.ws.closed

  async def disconnect(self):
    await self.ws.close()

  @property
  def loop(self) -> Any:
    return self.devtools.loop

  async def wait(self, seconds: float):
    await asyncio.sleep(seconds, loop=self.loop)

  async def send_rpc(
    self,
    method: str,
    params: Optional[Mapping[str, Any]] = None,
    nowait: Optional[bool] = False,
    timeout: Optional[int] = None,
    **kw
  ) -> Any:
    """ Возвращает результат либо id запроса (не все запросы предполагают ответ) """
    params = dict(params or {})
    params.update(kw)
    request = dict(
      id=self._get_next_id(),
      method=method,
      params=params,
      jsonrpc='2.0'
    )
    if not self.connected:
      await self.connect()
    await self.ws.send_json(request)
    if nowait:
      return request['id']
    return await self.wait_response(request['id'])

  async def wait_response(self, request_id: int, timeout: Optional[int] = None) -> AttrDict:
    return await self._wait_for('id', request_id, timeout)

  async def wait_event(self, name: str, timeout: Optional[int] = None) -> AttrDict:
    return await self._wait_for('method', name, timeout)

  async def __aiter__(self):
    while self._skipped:
      yield self._skipped.pop(0)
    async for msg in self.ws:
      if msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
        break
      if msg.type == aiohttp.WSMsgType.TEXT:
        data = json.loads(msg.data, object_hook=AttrDict)
        if 'error' in data:
          logger.warn(data)
        yield data

  def __getattr__(self, name: str) -> 'Domain':
    logger.debug(f'getter: {self.__class__.__name__}.{name}')
    return Domain(name, self)

  def _get_next_id(self):
    # По достижению 2 миллиардов счетчик сбрасывается
    if self._id > 2e9:
      self._id = 0
    self._id += 1
    return self._id

  async def _wait_for(self, key: str, value: Any, timeout: Optional[int] = None) -> AttrDict:
    async def coro():
      async for message in self:
        if message.get(key) == value:
          return message
        # Складываем сообщения в стэк
        if len(self._skipped) > self.SKIPPED_LIMIT - 1:
          self._skipped.pop(0)
        self._skipped.append(message)
    return await asyncio.wait_for(coro(), timeout or self.TIMEOUT, loop=self.loop)


class Domain:

  def __init__(self, name, tab):
    self._name = name
    self._tab = tab

  def __getattr__(self, name: str) -> Callable:
    """
    Без разницы Tab.browser.grant_permissions или
    Tab.Browser.grantPermissions, но первый - pythonic-style.
    """
    async def compound_method(*args, **kw) -> str:
      # Некоторые методы, например, RpcClient.network.enable() не предполагают
      # ответа, их вызов должен выглядеть так:
      #   async rpc.network.enable_nowait()
      # UnboundLocalError: local variable 'name' referenced before assignment
      meth = name
      if meth.endswith('_nowait'):
        meth = meth[:-7]
        kw['nowait'] = True
      meth = f'{self._name.title()}.{camelize(meth)}'
      return await self._tab.send_rpc(meth, *args, **kw)
    return compound_method
