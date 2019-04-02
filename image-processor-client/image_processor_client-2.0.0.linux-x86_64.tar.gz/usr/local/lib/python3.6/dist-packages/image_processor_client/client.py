from ._http import HttpImageClient
from .image_methods import ImageMethods


class Client(ImageMethods):
    """Main client class for end users\
    establishing connection to `Image Processor <https://github.com/thec0sm0s/image-processor/>`_ API Server providing\
    all of the categorised Image Methods.

    Parameters
    ----------
    connection_url : str, optional
        Base URL to running Image Processor API server. If not specified, attempts to connect to local Image Processor\
        API or developer's server if available.
    loop : :obj: `event_loop`, optional
        The event loop to use for asynchronous operations. Uses ``asyncio.get_event_loop()`` if not specified.

    Attributes
    ----------
    memes : image_processor_client.image_methods.MemesMethods
        An instance of ``MemesMethods`` class providing all of the available methods for memes category.
    discord : image_processor_client.image_methods.DiscordMethods
        An instance of ``DiscordMethods`` class providing all of the available methods for discord category.

    """

    def __init__(self, connection_uri: str = None, loop=None):
        self._http = HttpImageClient(uri=connection_uri, loop=loop)
        super().__init__()

    @property
    def http(self):
        return self._http

    async def close(self):
        """Closes running aiohttp session and performs basic cleanup."""
        return await self.http.session.close()
