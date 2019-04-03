import urllib
import requests

from dappy.methods import (
    GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, PATCH, TRACE
)

from dappy.exceptions import (
    NotSupportedException,
    RequestFailedException,
)


# Users use this the define and endpoint for an API
class Endpoint:
    def __init__(self, name, path, formatter=None, methods=[GET], default_query={}, default_params={}, default_headers={}, query_map={}):
        self.name = name
        self.path = self._prepend_slash(path)
        self.formatter = formatter
        self.methods = methods
        self.default_query = default_query
        self.default_params = default_params
        self.default_headers = default_headers
        self.query_map = query_map

    def _prepend_slash(self, path):
        if path.startswith('/'):
            return path
        else:
            return '/' + path



# Wrapper around Endpoint that actually contains the request logic
class CompleteEndpoint:

    def __init__(self, scheme, netloc, endpoint, formatter):
        self.scheme = scheme
        self.netloc = netloc
        self.endpoint = endpoint
        self.formatter = formatter

    def __call__(self, query={}, params=None, supplied_headers=None):
        return self.get(query=query, params=params, supplied_headers=supplied_headers)

    # Send a call to an API endpoint
    def get(self, query={}, params=None, supplied_headers=None):
        self._check_method(GET)
        url = self._build_url(query, params)
        headers = self._build_headers(supplied_headers)
        result = requests.get(url, headers=headers)
        request_ok_or_except(result)
        return self.formatter(result)

    # TODO: Make these other methods make sense
    def head(self, query={}, params=None, supplied_headers=None):
        self._check_method(HEAD)
        url = self._build_url(query, params)
        headers = self._build_headers(supplied_headers)
        result = requests.head(url, headers=headers)
        request_ok_or_except(result)
        return self.formatter(result)

    def post(self, data, query={}, params=None, supplied_headers=None):
        self._check_method(POST)
        url = self._build_url(query, params)
        headers = self._build_headers(supplied_headers)
        result = requests.post(url, data=data, headers=headers)
        request_ok_or_except(result)
        return self.formatter(result)

    def put(self, data, query={}, params=None, supplied_headers=None):
        self._check_method(PUT)
        url = self._build_url(query, params)
        headers = self._build_headers(supplied_headers)
        result = requests.put(url, data=data, headers=headers)
        request_ok_or_except(result)
        return self.formatter(result)

    def delete(self, query={}, params=None, supplied_headers=None):
        self._check_method(DELETE)
        url = self._build_url(query, params)
        headers = self._build_headers(supplied_headers)
        result = requests.delete(url, headers=headers)
        request_ok_or_except(result)
        return self.formatter(result)

    def connect(self, query={}, params=None, supplied_headers=None):
        self._check_method(CONNECT)
        url = self._build_url(query, params)
        headers = self._build_headers(supplied_headers)
        result = requests.connect(url, headers=headers)
        request_ok_or_except(result)
        return self.formatter(result)

    def options(self, query={}, params=None, supplied_headers=None):
        self._check_method(OPTIONS)
        url = self._build_url(query, params)
        headers = self._build_headers(supplied_headers)
        result = requests.options(url, headers=headers)
        request_ok_or_except(result)
        return self.formatter(result)

    def patch(self, query={}, params=None, supplied_headers=None):
        self._check_method(PATCH)
        url = self._build_url(query, params)
        headers = self._build_headers(supplied_headers)
        result = requests.patch(url, headers=headers)
        request_ok_or_except(result)
        return self.formatter(result)

    def trace(self, query={}, params=None, supplied_headers=None):
        self._check_method(TRACE)
        url = self._build_url(query, params)
        headers = self._build_headers(supplied_headers)
        result = requests.patch(url, headers=headers)
        request_ok_or_except(result)
        return self.formatter(result)

    # Build the request url from what parts we have
    def _build_url(self, query={}, params=None):
        self._add_default_query(query)
        self._add_default_params(params)
        self._map_query(query)
        return urllib.parse.urlunparse((
            self.scheme,
            self.netloc,
            self.endpoint.path,
            params,
            urllib.parse.urlencode(query),
            None
        ))

    """
        Cycles through default params and adds them
        if a value wasn't submitted for that param.
    """
    def _add_default_query(self, query_params):
        for key in self.endpoint.default_query:
            if key not in query_params:
                query_params[key] = self.endpoint.default_query[key]

    def _add_default_params(self, params):
        for key in self.endpoint.default_params:
            if key not in params:
                params[key] = self.endpoint.default_params[key]

    # Allows a standard interface for APIs
    # Maps provided param keys to what the API expects
    def _map_query(self, query_params):
        for key_from, key_to in self.endpoint.query_map.items():
            if key_from in query_params:
                query_params[key_to] = query_params[key_from]
                del query_params[key_from]

    # Throws an error if method is not supported
    def _check_method(self, method):
        if method not in self.endpoint.methods:
            raise NotSupportedException((
                '{0} is not supported for this API endpoint'
            ).format(method.upper()))
    
    def _build_headers(self, supplied_headers):
        headers = {}
        headers.update(self.endpoint.default_headers)
        if supplied_headers is not None:
            headers.update(supplied_headers)
        return headers


def request_ok_or_except(request):
    if not request.ok:
        raise RequestFailedException(
            'Request failed with status code {}'.format(request.status_code),
            request
        )