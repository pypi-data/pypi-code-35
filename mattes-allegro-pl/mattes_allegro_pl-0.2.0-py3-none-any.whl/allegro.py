import allegro_api.configuration
import allegro_api.rest
import tenacity
import zeep

from .oauth import AllegroAuth


class Allegro:
    def __init__(self, auth_handler: AllegroAuth):
        self.oauth = auth_handler
        if not self.oauth.access_token:
            if self.oauth._refresh_token:
                self.oauth.refresh_token()
            else:
                self.oauth.fetch_token()

    def rest_api_client(self):
        config = allegro_api.configuration.Configuration()
        config.host = 'https://api.allegro.pl'

        self.oauth.configure(config)
        return allegro_api.ApiClient(config)

    def retry(self, fn):
        return tenacity.retry(
            retry=AllegroAuth.token_needs_refresh,
            before=self.oauth.retry_refresh_token,
            stop=tenacity.stop_after_attempt(2)
        )(fn)

    def web_api_client(self):
        return zeep.client.Client('https://webapi.allegro.pl/service.php?wsdl')
