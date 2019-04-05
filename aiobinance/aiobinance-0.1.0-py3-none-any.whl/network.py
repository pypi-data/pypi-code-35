import asyncio
import hashlib
import hmac
from asyncio import AbstractEventLoop
from time import time
from typing import Optional, Dict
from urllib.parse import urlencode

from aiohttp import ClientSession, ClientTimeout, ClientResponse, ContentTypeError

from aiobinance.exceptions import BinanceAPIException, BinanceResponseException
from aiobinance.types import HttpMethod, ApiVersion


class Network:
    _API_URL = 'https://api.binance.com/api'

    _PUBLIC_API_VERSION = 'v1'
    _PRIVATE_API_VERSION = 'v3'

    def __init__(self, api_key: str, api_secret: str, loop: AbstractEventLoop = None, timeout: int = 10):
        self._API_KEY = api_key
        self._API_SECRET = api_secret

        self._loop = loop or asyncio.get_event_loop()
        self._session = self._init_session(timeout)

    def _generate_signature(self, params):
        return hmac.new(
            self._API_SECRET.encode('u8'),
            urlencode(params).encode('u8'),
            hashlib.sha256
        ).hexdigest()

    def _init_session(self, timeout: int) -> ClientSession:
        return ClientSession(
            headers={
                'Accept': 'application/json',
                'User-Agent': 'aiobinance/python',
                'X-MBX-APIKEY': self._API_KEY
            },
            timeout=ClientTimeout(total=timeout),
            loop=self._loop
        )

    async def close(self, delay: float = 0.250):
        '''Graceful shutdown.
        https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
        '''
        await asyncio.sleep(delay)
        await self._session.close()

    def _create_api_uri(self, path: str, version: ApiVersion) -> str:
        return f'{self._API_URL}/{version.value}/{path}'

    async def _request_api(
            self,
            method: HttpMethod,
            path: str,
            version: ApiVersion,
            private: bool = False,
            params: Optional[dict] = None,
    ):
        return await self._request(
            method,
            self._create_api_uri(path, version),
            private,
            params
        )

    async def _request(self, method: HttpMethod, url: str, sign: bool = False, params: Optional[dict] = None):
        params = params or {}

        if sign:
            params['timestamp'] = self._get_nonce()
            params['signature'] = self._generate_signature(params)

        async with self._session as session:
            http_method = getattr(session, method.value)
            async with http_method(url, params=params) as response:
                return await self._handle_response(response)

    @staticmethod
    async def _handle_response(response: ClientResponse):
        try:
            response_json = await response.json()
        except ContentTypeError:
            raise BinanceResponseException(f'Invalid response: {await response.text()!r}')
        else:
            if 200 <= response.status < 300:
                return response_json

            raise BinanceAPIException(response, response_json)

    async def get(self, path: str, version: ApiVersion, sign: bool = False, params: Optional[Dict] = None):
        return await self._request_api(HttpMethod.GET, path, version, sign, params)

    async def post(self, path: str, version: ApiVersion, sign: bool = False, params: Optional[Dict] = None):
        return await self._request_api(HttpMethod.POST, path, version, sign, params)

    async def put(self, path: str, version: ApiVersion, sign: bool = False, params: Optional[Dict] = None):
        return await self._request_api(HttpMethod.PUT, path, version, sign, params)

    async def delete(self, path: str, version: ApiVersion, sign: bool = False, params: Optional[Dict] = None):
        return await self._request_api(HttpMethod.DELETE, path, version, sign, params)

    @staticmethod
    def _get_nonce() -> int:
        return int(time() * 1000)
