import abc
import json
import concurrent.futures

import allegro_api.rest
import oauthlib.oauth2
import requests_oauthlib

URL_TOKEN = 'https://allegro.pl/auth/oauth/token'


class AllegroAuth:
    def __init__(self, client_id: str, client_secret: str, access_token=None, refresh_token=None):
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self._access_token: str = access_token
        self._refresh_token: str = refresh_token
        self._config: allegro_api.configuration.Configuration = None

    @property
    def access_token(self) -> str:
        return self._access_token

    @access_token.setter
    def access_token(self, access_token: str) -> None:
        self._access_token = access_token
        self.update_configuration()

    @abc.abstractmethod
    def fetch_token(self):
        pass

    def configure(self, config: allegro_api.configuration.Configuration):
        self._config = config
        self.update_configuration()

    def update_configuration(self):
        if self._config:
            self._config.access_token = self._access_token

    def retry_refresh_token(self, _, attempt) -> None:
        if attempt <= 1:
            return

        self.refresh_token()

    @abc.abstractmethod
    def refresh_token(self):
        pass

    @staticmethod
    def token_needs_refresh(f: concurrent.futures.Future) -> bool:
        x = f.exception(0)
        if isinstance(x, allegro_api.rest.ApiException) and x.status == 401:
            body = json.loads(x.body)
            return body['error'] == 'invalid_token' and body['error_description'].startswith('Access token expired: ')
        else:
            return False


class ClientCredentialsAuth(AllegroAuth):
    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret)

        client = oauthlib.oauth2.BackendApplicationClient(self.client_id, access_token=self.access_token)

        self.oauth = requests_oauthlib.OAuth2Session(client=client, token_updater=self.access_token)

    def fetch_token(self):
        token = self.oauth.fetch_token(URL_TOKEN, client_id=self.client_id,
                                       client_secret=self.client_secret)

        self.access_token = token['access_token']

    def refresh_token(self):
        return self.fetch_token()
