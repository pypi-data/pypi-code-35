import requests

from .const import TIMEOUT, __version__, API_URL
from .exceptions import RequestException


class RequestExecutor:
    def __init__(
            self,
            timeout=TIMEOUT,
            api_url=API_URL,
            session=None,
    ):
        self.timeout = timeout

        self._http = session or requests.Session()
        self._http.headers["User-Agent"] = "python-capitalist/{}".format(__version__)
        self._http.headers["X-Response-Format"] = "json"

        self.api_url = api_url

    def close(self):
        """Call close on the underlying session."""
        return self._http.close()

    def request(self, **kwargs):
        """Issue the HTTP request capturing any errors that may occur."""
        try:
            return self._http.post(self.api_url, timeout=self.timeout, **kwargs).json()
        except Exception as exc:
            raise RequestException(exc, kwargs)
