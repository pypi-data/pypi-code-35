# -*- coding: utf-8 -*-

from aiohttp import ClientSession

from .base import BaseService


class HttpClientService(BaseService):
    """Service class providing functions for interacting with HTTP servers

    :ivar http_client: aiohttp.ClientSession instance
    """

    http_client: ClientSession

    async def http_request(self, *args, **kwargs):
        """Creates a custom HTTP request

        :param args: args to pass along to `aiohttp.ClientSession.request`
        :param kwargs: kwargs to pass along to `aiohttp.ClientSession.request`
        :return: aiohttp.ClientResponse
        """

        async with self.http_client.request(*args, **kwargs) as resp:
            result = await resp.json()
            return result, resp.status

    async def http_post(self, url: str, payload: dict):
        """Creates a new HTTP POST request

        :param url: URL to send the request to
        :param payload: Payload to send
        :return: aiohttp.ClientResponse
        """

        return await self.http_request('POST', url, data=payload)

    async def http_get(self, url: str):
        """Creates a new HTTP GET request

        :param url: URL to send the request to
        :return: aiohttp.ClientResponse
        """

        return await self.http_request('GET', url)

    @classmethod
    def register(cls, pkg, mgr):
        super(HttpClientService, cls).register(pkg, mgr)
        cls.http_client = mgr.http_client
