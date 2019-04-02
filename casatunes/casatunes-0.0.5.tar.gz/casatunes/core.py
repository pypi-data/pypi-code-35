import asyncio
import aiohttp


async def async_request(session, url, params=None, json=True):
    try:
        async with session.get(url, params=params, timeout=10) as response:
            if response.status == 200:
                if json:
                    return await response.json()
                else:
                    return await response.text()
            else:
                return False
    except (asyncio.TimeoutError, aiohttp.ClientError) as error:
        return False
