from .core import async_request


class CasaTunesZone:
    def __init__(self, zone, url, sources, session):
        self._session = session
        self._sources = sources
        self._zone = zone
        self._zone_id = self._zone.get('ZoneID')
        self._url = '{}zones/{}'.format(url, self._zone_id)

    async def update(self):
        response = await async_request(self._session, self._url)
        if response is False:
            return False
        self._zone.update(response)
        return True

    async def _set_property(self, prop, value):
        props = {prop: value, 'format': 'json'}
        response = await async_request(self._session, self._url, props)
        if response is False:
            return False
        self._zone.update(response)
        return True

    @property
    def name(self):
        return self._zone.get('Name')

    @property
    def power(self):
        return self._zone.get('Power', False)

    @property
    def volume(self):
        return int(self._zone.get('Volume', 0))

    @property
    def muted(self):
        return self._zone.get('Mute', False) is True

    @property
    def source_name(self):
        for source in self._sources:
            if source.get('SourceID') == self._zone.get('SourceID'):
                return source.get('Name')
        return None

    @property
    def source_list(self):
        return [source.get('Name') for source in self._sources
                if not source.get('Hidden', False)]

    async def set_volume(self, volume):
        await self._set_property('Volume', volume)

    async def mute(self, mute):
        await self._set_property('Mute', 'true' if mute else 'false')

    async def turn_off(self):
        await self._set_property('Power', 'off')

    async def turn_on(self):
        await self._set_property('Power', 'on')

    async def set_source(self, source):
        for source_item in self._sources:
            if source_item.get('Name') == source:
                source_id = source_item.get('SourceID')
                await self._set_property('SourceID', source_id)
