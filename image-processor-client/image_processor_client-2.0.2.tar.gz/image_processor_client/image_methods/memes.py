from .._http import HttpImageClient


class MemesMethods(object):
    """Base class for available memes processing methods."""

    def __init__(self, http: HttpImageClient):
        self.http = http

    async def rip(self, text: str, avatar_url: str) -> bytes:
        """Requests server to process RIP meme using provided parameters and returns image\
        bytes.

        Parameters
        ----------
        text : str
            The text to write below avatar of RIP person.
        avatar_url: str
            Direct link to avatar to be shown in RIP Meme.

        Returns
        -------
        bytes
            Binary image bytes.

        """
        data = await self.http.rip_meme(text, avatar_url)
        return data.read_data
