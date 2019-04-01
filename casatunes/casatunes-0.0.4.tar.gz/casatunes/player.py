import datetime as dt
import pytz
import validators

from .core import async_request


class CasaTunesPlayer:
    def __init__(self, source, url, logo_prefix_url, session):
        self._session = session
        self._source = source
        self._source_id = self._source.get('SourceID')
        self._url = '{}sources/{}'.format(url, self._source_id)
        self._url_now_playing = '{}/nowplaying'.format(self._url)
        self._now_playing = dict()
        self._logo_prefix_url = logo_prefix_url
        self._last_updated = None

        self.update_now_playing()

    async def update(self):
        await self.update_now_playing()
        return True

    async def update_now_playing(self):
        response = await async_request(self._session, self._url_now_playing)
        if response is False:
            return False
        self._set_now_playing_dict(response)
        return True

    async def _set_property(self, prop, value):
        props = {prop: value, 'format': 'json'}
        response = await async_request(self._session, self._url_now_playing,
                                       props)
        if response is False:
            return False
        self._set_now_playing_dict(response)
        return True

    async def _send_action(self, action):
        url = '{}/player/{}'.format(self._url, action)
        response = await async_request(self._session, url, json=False)
        if response is False:
            return False
        elif response == '"OK"':
            return True
        else:
            return True

    def _set_now_playing_dict(self, now_playing):
        self._last_updated = dt.datetime.now(pytz.utc)
        self._now_playing.update(now_playing)

    @property
    def _curr_song(self):
        return self._now_playing.get('CurrSong', {})

    @property
    def _next_song(self):
        return self._now_playing.get('NextSong', {})

    @property
    def content_id(self):
        return self._curr_song.get('ID')

    @property
    def title(self):
        return self._curr_song.get('Title')

    @property
    def artist(self):
        return self._curr_song.get('Artists')

    @property
    def album(self):
        return self._curr_song.get('Album')

    @property
    def image_url(self):
        url = self._curr_song.get('ArtworkURI')
        logo_url = self._now_playing.get('ServiceLogoURI')
        prefix = self._logo_prefix_url
        if url and validators.url(url):
            return url
        elif url:
            return '{}{}'.format(prefix, url)
        if logo_url and validators.url(logo_url):
            return logo_url
        elif logo_url:
            return '{}{}'.format(prefix, logo_url)
        return None

    @property
    def name(self):
        return self._source.get('Name')

    @property
    def duration(self):
        return self._curr_song.get('Duration', 0)

    @property
    def track(self):
        return self._now_playing.get('QueueSongIndex', 0)

    @property
    def shuffle(self):
        return self._now_playing.get('ShuffleMode', False)

    @property
    def status(self):
        return self._now_playing.get('Status', 0)

    @property
    def position(self):
        return self._now_playing.get('CurrProgress')

    @property
    def position_updated_at(self):
        return self._last_updated

    async def seek(self, position):
        await self._set_property('CurrProgress', position)

    async def previous_track(self):
        await self._send_action('previous')

    async def next_track(self):
        await self._send_action('next')

    async def play(self):
        await self._send_action('play')

    async def pause(self):
        await self._send_action('pause')

    async def stop(self):
        await self._send_action('stop')

    async def set_shuffle(self, shuffle):
        str_flag = 'true' if shuffle else 'false'
        await self._set_property('ShuffleMode', str_flag)

