from typing import Dict, Type, TypeVar

import requests

from tdameritrade_client.auth import TDAuthenticator
from tdameritrade_client.utils import urls
from tdameritrade_client.utils.tools import check_auth

# For typehint of the classmethod
T = TypeVar('T', bound='TrivialClass')


class TDClient(object):
    def __init__(self, acct_number: int,
                 oauth_user_id: str,
                 redirect_uri: str = 'http://127.0.0.1:8080',
                 token_path: str = urls.DEFAULT_TOKEN_PATH):
        """
        An object which executes requests on the TDA API.
        Args:
            acct_number: The account number to authenticate against.
            oauth_user_id: The oauth user ID of the TD developer app this client is authenticating against.
            redirect_uri: The redirect URI of the TD developer app this client is authenticating against.
            token_path: Path where the auth-token.json should be written. Defaults to $HOME/.tda_certs/auth-token.json.
        """
        self._acct_number = acct_number
        self._redirect_uri = redirect_uri
        self._oauth_user_id = oauth_user_id.upper()
        self._token_path = token_path
        self.token = None

        ip = redirect_uri.split('/')[-1]
        host, port = ip.split(':')

        self._authenticator = TDAuthenticator(host, int(port),
                                              self._oauth_user_id,
                                              self._token_path)

    @classmethod
    def from_dict(cls: Type[T], acct_info: Dict) -> T:
        """
        Create an instance of this class from a dictionary.
        Args:
            acct_info: A dictionary of init parameters

        Returns: An instance of this class
        """
        return cls(**acct_info)

    def run_auth(self) -> None:
        """
        Runs the authentication flow. See the TDAuthenticator class for details.
        """
        self.token = self._authenticator.authenticate()

    @check_auth
    def get_positions(self) -> Dict:
        """
        Requests the positions information of self._acct_number
        Returns: A json object containing the account positions information.
        """
        reply = requests.get(self._get_url('positions'),
                             headers=self._build_header())
        # TODO handle exception on error
        return reply.json()

    def _get_url(self, type: str) -> str:
        """
        Build the correct url to perform an API action.
        Args:
            type: What type of url to build. Supports:
                positions: Return account positions.

        Returns: The requested url.
        """
        url = urls.BASE_URL
        if type == 'positions':
            url += urls.ACCOUNT_URL + str(self._acct_number) + urls.FIELDS + type
        else:
            raise NotImplementedError('URL type {} not supported.'.format(type))
        return url

    @check_auth
    def _build_header(self) -> Dict:
        """
        Builds auth header to include with all requests.
        Returns: The header object to use with requests
        """
        return {'Authorization': 'Bearer ' + self.token}
