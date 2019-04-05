from abc import ABC
from enum import Enum
from typing import Dict, Optional

from aiobinance.network import Network
from aiobinance.types import ApiVersion


class BaseModule(ABC):
    def __init__(self, network):
        self._http: Network = network

    async def _get(
            self,
            path: str, sign: bool = False, params: Optional[Dict] = None, version: ApiVersion = ApiVersion.V1
    ):
        return await self._http.get(path, sign=sign, params=self._filter_params(params), version=ApiVersion(version))

    async def _post(
            self,
            path: str, sign: bool = True, params: Optional[Dict] = None, version: ApiVersion = ApiVersion.V1
    ):
        return await self._http.post(path, version, sign=sign, params=self._filter_params(params))

    async def _put(
            self,
            path: str, sign: bool = True, params: Optional[Dict] = None, version: ApiVersion = ApiVersion.V1
    ):
        return await self._http.put(path, version, sign=sign, params=self._filter_params(params))


    async def _delete(
            self,
            path: str, sign: bool = True, params: Optional[Dict] = None, version: ApiVersion = ApiVersion.V1
    ):
        return await self._http.delete(path, version, sign=sign, params=self._filter_params(params))


    @staticmethod
    def _filter_params(params: Dict) -> Dict:
        return {
            k: v.value if isinstance(v, Enum) else v
            for k, v in params.items()
            if v is not None
        }
