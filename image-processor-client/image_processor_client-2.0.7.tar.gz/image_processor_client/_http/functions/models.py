from abc import ABC, abstractmethod

from ..._http.response import HttpResponseData
from ..._http.route import Route


class ImageFunction(ABC):

    @abstractmethod
    def route(self, path, method: str = "POST", **params):
        raise NotImplementedError

    @abstractmethod
    async def request(self, route: Route, **kwargs) -> HttpResponseData:
        raise NotImplementedError
