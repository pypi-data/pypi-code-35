from megaphone.client import APIObject, HTTPClient


class Episode(APIObject):
    path = 'episodes'


class Podcast(APIObject):
    path = 'podcasts'

    @property
    def episodes(self, draft=None):
        kwargs = {}
        if draft is not None:
            kwargs['draft'] = "true" if draft else "false"
        for episode in self.http.get('episodes', **kwargs):
            yield Episode(self.http, episode)


class NetworkClient(APIObject):
    path = "networks"

    def __init__(self, token, objid):
        super().__init__(HTTPClient(token), {'id': objid})

    @property
    def podcasts(self):
        for podcast in self.http.get('podcasts'):
            yield Podcast(self.http, podcast)

    def get_podcast(self, objid):
        return Podcast.build(self.http, objid)
