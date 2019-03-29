import asyncio
import aiohttp


async def async_request(url, params=None, json=True):
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, params=params, timeout=10)
            if response.status == 200:
                if json:
                    return await response.json()
                else:
                    return await response.text()
            else:
                return False
    except (asyncio.TimeoutError, aiohttp.ClientError) as error:
        return False

