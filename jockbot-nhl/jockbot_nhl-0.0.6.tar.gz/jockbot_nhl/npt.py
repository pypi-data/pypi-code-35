import asyncio

import newspaper


async def foo():
    print('fuck you')
    urls = [
        'http://www.espn.com/',
        'https://www.npr.org/',
        'http://cnn.com',
        'https://arstechnica.com/'
    ]
    async for value in build_newspaper(urls):
        print('fuck you')
        print(value)
        await print(value)

async def build_newspaper(urls):
    print('fuck you')
    for url in urls:
        _newspaper = await newspaper.build(url)
        yield _newspaper


print('fuck you')
loop = asyncio.get_event_loop().run_until_complete(foo())
