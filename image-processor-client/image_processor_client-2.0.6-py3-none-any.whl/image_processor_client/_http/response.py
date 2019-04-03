import aiohttp


class HttpResponseData(object):

    def __init__(self, response: aiohttp.ClientResponse):
        self.response = response
        self.read_data = None

    async def read(self):
        self.read_data = await self.response.read()
