class ImageUtils(object):
    """A common utility class containing methods to fetch details or something of image."""

    def __init__(self, client):
        self.__session = client.http.session

    async def fetch_size(self, url: str):
        """Returns total size of content from provided URL querying ``Content-Length`` from HTTP headers.

        Parameters
        ----------
        url : str
            Direct URL to the content to get size of.

        Returns
        -------
        int
            An integer representing total size of content in bytes.

        """
        response = await self.__session.request("GET", url)
        return int(response.headers.get("Content-Length"), 0)
