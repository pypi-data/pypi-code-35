"""
Arkindex API Client
"""
import os.path
import apistar
import yaml
from arkindex.auth import TokenSessionAuthentication
from arkindex.pagination import ResponsePaginator

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ArkindexClient(apistar.Client):
    """
    An Arkindex API client.
    """

    def __init__(self, token=None, base_url=None, **kwargs):
        r"""
        :param token: An API token to use. If omitted, access is restricted to public endpoints.
        :type token: str or None
        :param host: A custom base URL for the client. If omitted, defaults to the Arkindex main server.
        :type host: str or None
        :param \**kwargs: Keyword arguments to send to ``apistar.Client``.
        """
        kwargs.setdefault('auth', TokenSessionAuthentication(token))

        with open(os.path.join(BASE_DIR, 'schema.yml')) as f:
            schema = yaml.safe_load(f.read())

        if base_url:
            # APIStar currently does not handle setting a custom base URL; we will override the schema servers
            schema['servers'] = [{'url': base_url}, ]

        super().__init__(schema, **kwargs)

        # Add the Referer header to allow Django CSRF to function
        self.transport.headers.setdefault('Referer', self.document.url)

    def __repr__(self):
        return '<{} on {}>'.format(self.__class__.__name__, self.document.url)

    def paginate(self, *args, **kwargs):
        """
        Perform a usual request as done by APIStar, but handle paginated endpoints.

        :return: An iterator for a paginated endpoint.
        :rtype: arkindex.pagination.ResponsePaginator
        """
        return ResponsePaginator(self, *args, **kwargs)

    def login(self, email, password):
        """
        Login to Arkindex using an email/password combination.
        This helper method automatically sets the client's authentication settings with the token.
        """
        resp = self.request('Login', body={'email': email, 'password': password})
        if 'auth_token' in resp:
            self.transport.session.auth.token = resp['auth_token']
        return resp
