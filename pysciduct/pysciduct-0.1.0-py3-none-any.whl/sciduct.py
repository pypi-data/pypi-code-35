import requests
import json
from urllib.parse import urljoin
from sciduct.exceptions import RPCError
from sciduct.session import Session
from functools import wraps

def check_response_errors(func):
    @wraps(func)
    def _decorator(self, *args, **kwargs):
        resp = func(self, *args, **kwargs)
        resp.raise_for_status()
        return resp
    return _decorator

class SciDuctServiceClientBase():
    """
    Generic SciDuct Service that all other services inherit.

    :param token: Token to use for authentication.
    :type token: str
    :param url: Base URL for the service.
    :type url: str
    """
    def __init__(self, session, url='http://localhost/'):
        if type(session) is Session:
            self.session = session
        else:
            raise TypeError('session must be type Session')

        self.url = url

    __service_name__ = 'sciduct'

    @classmethod
    def rpc(cls, method):
        def decorator(func):
            @wraps(func)
            def decorated(self, *params):
                params = func(self, *params)

                headers = self._get_rpc_headers()
                payload = self._get_rpc_payload(method, params)
                resp = requests.post(self.url, headers=headers, json=payload).json()

                rpc_error_msg = None
                if 'error' in resp:
                    error = resp['error']
                    code = error['code']
                    message = error['message']
                    param_list = ','.join(map(str, params))

                    # Adapted from
                    # http://docs.python-requests.org/en/master/_modules/requests/models/#Response.raise_for_status
                    if 400 <= code < 500:
                        rpc_error_msg = '{0} Client Error: {1} for rpc: {2}({3})'\
                                .format(code, message, method, param_list)

                    elif 500 <= code < 600:
                        rpc_error_msg = '{0} Server Error: {1} for rpc: {2}({3})'\
                                .format(code, message, method, param_list)

                if rpc_error_msg is not None:
                    raise RPCError(rpc_error_msg, rpc_call=payload)

                return resp['result']
            return decorated
        return decorator

    def _get_rpc_headers(self):
        """
        Get headers for an RPC call.  Used internally by :py:func:`_rpc_call`.
        """
        return {
            'content-type': 'application/jsonrequest',
            'authorization': self.session.token
        }

    @staticmethod
    def _get_rpc_payload(command, params):
        """
        Build the payload for an RPC call.  Used internally by
        :py:func:`_rpc_call`.

        :param command: Method name.
        :param params: List of parameters.
        """
        return {
            'method': command,
            'params': params,
            'jsonrpc': '2.0'
        }

    __app_json = 'application/json'
    @check_response_errors
    def _get(self, path, accept=__app_json, **kwargs):
        """
        Perform a GET request.

        :param path: The request will be sent to `self.url + path`.
        :type path: str
        :param accept: The mime type to accept in the response.
        :type accept: str
        :param kwargs: Keyword parameters are passed on to the
            :py:func:`requests.get` call.
        :returns: a :py:class:`requests.response` as returned by
            :py:func:`requests.get`
        """
        headers = {
            'accept': accept,
            'authorization': self.session.token
        }
        url = urljoin(self.url, path)
        return requests.get(url, headers=headers, **kwargs)

    @check_response_errors
    def _post_json(self, path, body, accept=None, **kwargs):
        url = urljoin(self.url, path)
        headers = {
            'content-type': 'application/json',
            'authorization': self.session.token
        }
        if accept is not None:
            headers['accept'] = accept

        return requests.post(url, headers=headers, json=body, **kwargs)
