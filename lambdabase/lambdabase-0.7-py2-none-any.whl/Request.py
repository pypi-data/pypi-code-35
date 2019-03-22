import bleach
from abc import ABCMeta, abstractmethod


class Request(object):
    """
    The base request object. All requests coming into
    they system should extend this class
    """
    __metaclass__ = ABCMeta
    _data = {}
    _headers = {}
    _identity = {}

    def __init__(self, data=None, headers=None, claims=None):
        self._data = data
        self._headers = headers
        self._claims = claims

    @abstractmethod
    def validate(self):
        pass

    @property
    def data(self):
        if self._data is None:
            self._data = {}
        return self._data

    @property
    def headers(self):
        if self._headers is None:
            self._headers = {}
        return self._headers

    @property
    def correlation_id(self):
        return self._data.get('correlation_id')

    @correlation_id.setter
    def correlation_id(self, value):
        self._data['correlation_id'] = value

    @classmethod
    def make_clean(cls, value):
        return bleach.clean(value, tags=[], attributes={}, strip=True)


class AuthenticatedRequest(Request):
    """
    The base request object. All authenticated requests coming into
    they system should extend this class. It is assumed that the
    request has passed through an API Gateway IAM Authorizer and
    that cognito identity IDs have been populated.
    """
    __metaclass__ = ABCMeta

    @property
    def claims(self):
        if self._claims is None:
            self._claims = {}
        return self._claims

    @property
    def user_id(self):
        return self.claims.get("sub")

    @property
    def username(self):
        return self.claims.get('cognito:username')

