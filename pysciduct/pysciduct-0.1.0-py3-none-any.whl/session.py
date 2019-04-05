import requests
import json
from urllib.parse import urljoin
import jwt
from datetime import datetime

class Session():
    """
    User session used to get a token and verify it.  A session can be created
    with an application id and secret along with the url of the user service.
    In this case the session will get the token from the user service using is
    id/secret pair.  Alternatively, a token can be supplied, in which case the
    provided token will be used.
    
    :param url: URL of User Service.
    :type url: str
    :param app_id: App id.
    :type app_id: str
    :param app_secret: App secret.
    :type app_secret: str
    :param token: Token to use for the session.
    :type token: str
    """
    def __init__(self, url='http://localhost/', app_id=None,
            app_secret=None, token=None, pub_key=None):
        self.token = token
        self.url = url
        
        if app_id is not None and app_secret is not None:
            full_url = urljoin(url, 'authenticate/' + app_id)
            data = { 'secret': app_secret }
            response = requests.post(url=full_url, data=data)
            self.token = response.text

        if pub_key:
            self.pub_key = pub_key
        else:
            self.pub_key = self._get_pub_key()

        account = self.verify()

        self.user = account['sub']
        self.issued_at = datetime.utcfromtimestamp(account['iat'])
        self.not_before = datetime.utcfromtimestamp(account['nbf'])
        self.expires = datetime.utcfromtimestamp(account['exp'])

    def _get_pub_key(self):
        url = urljoin(self.url, 'public_key/')
        resp = requests.get(url)

        if resp.status_code != 200:
            raise SessionKeyError('Could not retrieve public key from user service')

        key = resp.text
        return key
        
    def verify(self):
        """
        Verifies the integrity of the token.  If the decode fails, exceptions
        will be raised.  See :py:func:`jwt.decode`.

        :returns: The decoded token.
        """
        key = self.pub_key
        decoded = jwt.decode(self.token, key, audience='@core')
        return decoded

class SessionKeyError(Exception):
    """
    Error raised when the public key cannot be retrieved from the user service.
    """
    pass
