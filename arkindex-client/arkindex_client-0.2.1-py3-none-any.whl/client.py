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

    def upload(self, corpus_id, f, mode='rb'):
        """
        Upload a file-like object or a file path to a corpus.
        This helper is required as APIStar does not currently handle
        anything else than JSON as request parameters.

        :param str corpus_id: ID of a writable corpus to upload files to.
        :param f: File-like object, or path to a readable file, to upload.
        :type f: str or file-like object
        :param str mode: When specifying a path, sets the mode to use when
           opening the file.
        :return: The JSON response from the endpoint
        :rtype: dict
        """
        if isinstance(f, str):
            assert os.path.exists(f), 'File {} does not exist'.format(f)
            f = open(f, mode)

        params = {'id': corpus_id}
        content = {'file': f}
        encoding = apistar.client.encoders.MultiPartEncoder.media_type

        link = self.lookup_operation('UploadDataFile')
        url = self.get_url(link, params)
        query_params = self.get_query_params(link, params)

        return self.transport.send(
            link.method,
            url,
            query_params=query_params,
            content=content,
            encoding=encoding,
        )
