import aiohttp

from .core import async_request
from .zone import CasaTunesZone
from .player import CasaTunesPlayer


class CasaTunes:
    def __init__(self, host, port, session=None):
        self._session = session
        self._url = 'http://{}:{}/api/v1/'.format(host, port)
        self._logo_prefix_url = 'http://{}/CasaTunes/GetImage.ashx?ID='\
            .format(host)

    async def create_session(self):
        async with aiohttp.ClientSession() as session:
            self._session = session

    async def get_zones(self):
        zones_url = self._url + 'zones'
        sources_url = self._url + 'sources'
        zones = await async_request(self._session, zones_url,
                                    {'format': 'json'})
        sources = await async_request(self._session, sources_url,
                                      {'format': 'json'})
        if zones is False or sources is False:
            return False
        devices = []
        for zone in zones:
            devices.append(CasaTunesZone(zone, self._url, sources,
                                         self._session))
        return devices

    async def get_sources(self):
        url = self._url + 'sources'
        sources = await async_request(self._session, url, {'format': 'json'})
        if sources is False:
            return False
        devices = []
        for source in sources:
            if not source.get('Hidden'):
                devices.append(CasaTunesPlayer(source, self._url,
                                               self._logo_prefix_url,
                                               self._session))
        return devices
