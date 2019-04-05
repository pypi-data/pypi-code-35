"""Core module of the project."""

from asyncio import gather
from typing import Coroutine, Iterable

from aiohttp import ClientResponse, ClientSession

URL = str


async def check(session: ClientSession, url: URL,
                redirect: bool = False) -> ClientResponse:
    """Check the status of a website."""
    async with session.head(url, allow_redirects=redirect) as response:
        return response


async def checkall(websites: Iterable[URL], **kwargs) -> Iterable[Coroutine]:
    """Check the status of some websites."""
    async with ClientSession() as session:
        tasks = [check(session, url, **kwargs) for url in websites]

        return await gather(*tasks)
