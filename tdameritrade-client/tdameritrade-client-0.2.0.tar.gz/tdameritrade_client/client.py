from typing import Dict, Type, TypeVar

import requests

from tdameritrade_client.auth import TDAuthenticator
from tdameritrade_client.utils import urls
from tdameritrade_client.utils.tools import check_auth

# For typehint of the classmethod
T = TypeVar('T', bound='TrivialClass')


class TDClient(object):
    """
    Python client for the TDAmeritrade API.

    """
    def __init__(self, acct_number: int,
                 oauth_user_id: str,
                 redirect_uri: str,
                 token_path: str = urls.DEFAULT_TOKEN_PATH):
        """
        Constructor for the TDClient object.

        Args:
            acct_number: The account number to authenticate against.
            oauth_user_id: The oauth user ID of the TD developer app this client is authenticating against.
            redirect_uri: The redirect URI where TDAmeritrade will send an auth token.
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

        Returns:
            An instance of this class

        """
        return cls(**acct_info)

    def run_auth(self) -> None:
        """
        Runs the authentication flow. See the TDAuthenticator class for details.
        """
        self.token = self._authenticator.authenticate()

    @check_auth
    def get_instrument(self, symbol: str, projection: str = 'symbol-search'):
        """
        Return fundamental information for an instrument by ticker, CUSIP, or description.

        Args:
            symbol: The search string. Can be a ticker or a regex.
            projection: Type of search to perform.
                Supports:\n
                symbol-search: Search by exact ticker or CUSIP.\n
                symbol-regex: Return all instruments that match a regex.\n
                desc-regex: Return all instruments whose descriptions contain a regex.

        Returns:
            A dict of results where keys are tickers and values are objects containing
            fundamental information.

        """
        if projection not in ['symbol-search', 'symbol-regex', 'desc-regex']:
            raise NotImplementedError('Can only search by symbol, symbol regex, or desc regex.')

        reply = requests.get(self._get_url('get_instrument',
                                           {'symbol': symbol,
                                            'projection': projection}),
                             headers=self._build_header())
        return reply.json()

    @check_auth
    def get_quote(self, symbol: str):
        """
        Return quote for a given symbol.

        Args:
            symbol: The ticker symbol for a quote.

        Returns:
            A dict of results where keys are tickers and values are objects containing
            a quote.

        """
        reply = requests.get(self._get_url('get_quote',
                                           {'symbol': symbol}),
                             headers=self._build_header())
        return reply.json()

    @check_auth
    def get_positions(self) -> Dict:
        """
        Requests the positions information of self._acct_number

        Returns:
            A json object containing the account positions information.

        """
        reply = requests.get(self._get_url('positions'),
                             headers=self._build_header())
        return reply.json()

    def _get_url(self, type: str, params: Dict = {}) -> str:
        """
        Build the correct url to perform an API action.

        Args:
            type: What type of url to build. Supports:
                positions: Return account positions.
                get_instrument: Return fundamental data for a ticker or CUSIP
                    Must include params['symbol'] and params['projection']
                get_quote: Return quote for a symbol.
                    Must include params['symbol']
            params: Dict of keyword arguments

        Returns:
            The requested url.

        """
        url = urls.BASE_URL
        if type == 'positions':
            url += f'{urls.ACCOUNT_URL}{str(self._acct_number)}?fields={type}'
        elif type == 'get_instrument':
            url += f'{urls.INSTRUMENTS_URL}{urls.APIKEY_PARAM}{self._oauth_user_id}' \
                   f'&symbol={params["symbol"]}&projection={params["projection"]}'
        elif type == 'get_quote':
            url += f'{urls.QUOTES_URL}{urls.APIKEY_PARAM}{self._oauth_user_id}&symbol={params["symbol"]}'
        else:
            raise NotImplementedError('URL type {} not supported.'.format(type))
        return url

    @check_auth
    def _build_header(self) -> Dict:
        """
        Builds auth header to include with all requests.

        Returns:
            The header object to use with requests

        """
        return {'Authorization': 'Bearer ' + self.token}
