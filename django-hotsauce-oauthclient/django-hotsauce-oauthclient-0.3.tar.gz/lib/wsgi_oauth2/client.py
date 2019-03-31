#!/usr/bin/env python
import sys
import logging
log = logging.getLogger(__name__)

PY3K = sys.version_info[0] == 3

#import requests
import json

try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
    from urllib.error import HTTPError
except ImportError:
    # python27
    from urllib2 import urlopen, HTTPError
    from urllib import urlencode

from oauthlib.oauth2 import WebApplicationClient

from .controller import OAuthController
from .provider import google
from .util import AccessToken

__all__ = ['GoogleOAuthClient', 'GoogleClient']

class GoogleOAuthClient(WebApplicationClient):
    """Client for :class:`Service`.

    :param service: service the client connects to
    :type service: :class:`Service`
    :param client_id: client id
    :type client_id: :class:`basestring`, :class:`numbers.Integral`
    :param client_secret: client secret key
    :type client_secret: :class:basestring`
    :param \*\*extra: additional arguments for authorization e.g.
                      ``scope='email,read_stream'``

    """

    #: (:class:`Service`) The service the client connects to.
    service = google

    #: (:class:`basestring`) The client id.
    # client_id = None

    #: (:class:`basestring`) The client secret key.
    # client_secret = None

    #: (:class:`dict`) The additional arguments for authorization e.g.
    #: ``{'scope': 'email,read_stream'}``.

    def __init__(self, client_id, **kwargs):
        super(GoogleClient, self).__init__(client_id, **kwargs)
        #log.debug("client ID=%s"%self.client_id)
        #log.debug("redirect URL=%s"%self.redirect_url)

    def make_authorize_url(self, redirect_uri, state=None):
        """Makes an authorize URL.

        :param redirect_uri: callback url
        :type redirect_uri: :class:`basestring`
        :param state: optional state to get when the user returns to
                      callback
        :type state: :class:`basestring`
        :returns: generated authorize url
        :rtype: :class:`basestring`

        """
        query = dict(self.token)
        query.update(client_id=self.client_id,
                     redirect_uri=self.redirect_url,
                     response_type='code',
                     scope=self.scope)
        if state is not None:
            query['state'] = state
        return '{0}?{1}'.format(self.service.authorize_endpoint,
                                urlencode(query))

    def load_username(self, access_token):
        """Load a username from the configured service suitable for the
        REMOTE_USER variable. A valid :class:`AccessToken` is provided to allow
        access to authenticated resources provided by the service. For GitHub
        the 'login' variable is used.

        :param access_token: a valid :class:`AccessToken`

        .. versionadded:: 0.1.2

        """
        self.service.load_username(access_token)

    def is_user_allowed(self, access_token):
        return self.service.is_user_allowed(access_token)

    def request_access_token(self, redirect_uri, code):
        """Requests an access token.

        :param redirect_uri: ``redirect_uri`` that was passed to
                             :meth:`make_authorize_url`
        :type redirect_uri: :class:`basestring`
        :param code: verification code that authorize endpoint provides
        :type code: :class:`code`
        :returns: access token and additional data
        :rtype: :class:`AccessToken`

        """
        #log.debug("access token: %s" % self.access_token)

        form = {'code': code,
                'client_id': self.client_id,
                'client_secret': self.access_token,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code'}
        try:
            if PY3K:
                u = urlopen(self.service.access_token_endpoint, 
                    bytes(urlencode(form), 'utf8'))
            else:
                u = urlopen(self.service.access_token_endpoint,
                    urlencode(form))
            m = u.info()
        except HTTPError as ex:
            raise ex
        
        try:
            # Python 2
            content_type = m.gettype()
        except AttributeError:
            # Python 3
            content_type = m.get_content_type()
        if content_type == 'application/json':
            data = json.load(u)
            
        else:
            data = dict(
                (k.decode('utf-8')
                 if not isinstance(k, str) and isinstance(k, bytes)
                 else k, v)
                for k, v in urlparse.parse_qs(u.read()).items()
            )
        u.close()
        return AccessToken(data)




    def wsgi_middleware(self, *args, **kwargs):
        """Wraps a WSGI application."""
        wsgi_app = args[0]
        return OAuthController(wsgi_app, **kwargs)

GoogleClient = GoogleOAuthClient

