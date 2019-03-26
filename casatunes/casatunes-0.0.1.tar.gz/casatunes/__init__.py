from .core import async_request
from .zone import CasaTunesZone
from .player import CasaTunesPlayer


class CasaTunes:
    def __init__(self, host, port):
        self.url = 'http://{}:{}/api/v1/'.format(host, port)
        self.logo_prefix_url = 'http://{}/CasaTunes/GetImage.ashx?ID='\
            .format(host)

    async def get_zones(self):
        zones_url = self.url + 'zones'
        sources_url = self.url + 'sources'
        zones = await async_request(zones_url, {'format': 'json'})
        sources = await async_request(sources_url, {'format': 'json'})
        if zones is False or sources is False:
            return False
        devices = []
        for zone in zones:
            devices.append(CasaTunesZone(zone, self.url, sources))
        return devices

    async def get_sources(self):
        url = self.url + 'sources'
        sources = await async_request(url, {'format': 'json'})
        if sources is False:
            return False
        devices = []
        for source in sources:
            if not source.get('Hidden'):
                devices.append(CasaTunesPlayer(source, self.url,
                                               self.logo_prefix_url))
        return devices
