# https://chromedevtools.github.io/devtools-protocol/
# Первоначально я наткнулся на такое решение
# `https://github.com/marty90/PyChromeDevTools/`, но мне оно не
# подходило из-за блокирующих операций. Про puppeteer я знал, но свой
# велосипед удобнее.
import asyncio
import json
from dataclasses import dataclass
from typing import Any, Callable, List, Mapping, Optional, Union
from urllib.parse import quote_plus, urljoin

import aiohttp

from .datatypes import AttrDict
from .log import logger
from .utils import camelize

__all__ = ('ChromeDevTools', 'Domain', 'RpcClient')


class ChromeDevTools:
  host = 'localhost'
  port = 9222

  def __init__(
    self,
    session: Optional[aiohttp.ClientSession] = None,
    *,
    host: str = None,
    port: int = None,
    loop = None  # какой тип?
  ):
    self.host = host or self.host
    self.port = port or self.port
    self.loop = loop or asyncio.get_event_loop()
    self.session = session or aiohttp.ClientSession(loop=self.loop)

  async def version(self) -> Mapping[str, Any]:
    r = await self.fetch('/json/version')
    return await r.json()

  async def tabs(self) -> List[Mapping[str, Any]]:
    r = await self.fetch('/json/list')
    return await r.json()

  async def protocol(self) -> Mapping[str, Any]:
    r = await self.fetch('/json/protocol/')
    return await r.json()

  async def new_tab(self, url: str) -> Mapping[str, Any]:
    r = await self.fetch('/json/new?' + quote_plus(url))
    return await r.json()

  async def activate_tab(self, tab_id: str) -> str:
    r = await self.fetch(f'/json/activate/{tab_id}')
    return await r.text()

  async def close_tab(self, tab_id: str) -> str:
    r = await self.fetch(f'/json/close/{tab_id}')
    return await r.text()

  async def connect_tab(self, url: str) -> 'RpcClient':
    ws = await self.session.ws_connect(url)
    return RpcClient(ws, loop=self.loop)

  async def fetch(self, url: str) -> aiohttp.ClientResponse:
    endpoint = urljoin(f'http://{self.hostname}', url)
    response = await self.session.get(endpoint)
    return response

  @property
  def hostname(self) -> str:
    return f'{self.host}:{self.port}'


class RpcClient:
  TIMEOUT = 15
  SKIPPED_LIMIT = 100

  def __init__(self, ws: aiohttp.ClientWebSocketResponse, *, loop = None):
    self.ws = ws
    self.loop = loop
    self.skipped = []
    self._id = 0

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
      id=self.next_id(),
      method=method,
      params=params,
      jsonrpc='2.0'
    )
    await self.ws.send_json(request)
    if nowait:
      return request['id']
    return await self.wait_for(request['id'])

  def next_id(self):
    # По достижению 2 миллиардов счетчик сбрасывается
    if self._id > 2e9:
      self._id = 0
    self._id += 1
    return self._id

  async def wait_for(self, request_id: int, timeout: Optional[int] = None) -> AttrDict:
    async def coro():
      async for message in self:
        if message.get('id') == request_id:
          return message
        # Складываем сообщения в стэк
        if len(self.skipped) > self.SKIPPED_LIMIT - 1:
          self.skipped.pop(0)
        self.skipped.append(message)
    return await asyncio.wait_for(coro(), timeout or self.TIMEOUT, loop=self.loop)

  async def __aiter__(self):
    while self.skipped:
      yield self.skipped.pop(0)
    async for msg in self.ws:
      if msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
        break
      if msg.type == aiohttp.WSMsgType.TEXT:
        data = json.loads(msg.data, object_hook=AttrDict)
        if 'error' in data:
          logger.warn(data)
        yield data

  def __getattr__(self, name: str) -> 'Domain':
    return Domain(name, self)


class Domain:

  def __init__(self, domain: str, client: RpcClient):
    self._domain = domain
    self._client = client

  def __getattr__(self, name: str) -> Callable:
    """
    Без разницы RpcClient.browser.grant_permissions или
    RpcClient.Browser.grantPermissions, но первый - pythonic-style.
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
      meth = camelize(meth)
      meth = f'{self._domain.title()}.{meth}'
      return await self._client.send_rpc(meth, *args, **kw)
    return compound_method
