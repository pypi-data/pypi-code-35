from __future__ import unicode_literals, print_function

import functools
import logging
from pprint import pformat
from time import sleep
from six.moves.urllib.parse import urlparse

import requests
from requests import HTTPError
from six.moves.urllib.parse import urljoin

logger = logging.getLogger(__name__)
MAX_RETRIES = 5


class ProviderHTTPClientException(Exception):
    def __init__(self, *args, **kwargs):
        super(ProviderHTTPClientException, self).__init__(*args)
        for key, value in kwargs:
            setattr(self, key, value)


class RetryableException(ProviderHTTPClientException):
    pass


class ProviderRequestProxy(object):
    def __init__(self, url, headers, timeout, retries=MAX_RETRIES, host=None, **kwargs):
        self.url = url
        self.headers = headers
        self.timeout = timeout
        self.retries = retries
        self.host = host
        self.raw = kwargs.get('raw', False)
        self.is_json = kwargs.get('json', True)

    def augment_request_arguments(self, **request_kwargs):
        self.headers.update(request_kwargs.get('headers', {}))
        url_override = request_kwargs.get('url', None)
        logger.debug('request_kwargs: {}'.format(request_kwargs))
        self.url = self.url.format(**request_kwargs)

        data = {
            'url': url_override if url_override else self.url,
            'headers': self.headers,
            'timeout': self.timeout,
        }
        if 'data' in request_kwargs:
            data['data'] = request_kwargs['data']
        if 'json' in request_kwargs:
            data['json'] = request_kwargs['json']
        if 'files' in request_kwargs:
            data['files'] = request_kwargs['files']
        if 'stream' in request_kwargs:
            data['stream'] = request_kwargs['stream']
        if 'params' in request_kwargs:
            data['params'] = request_kwargs['params']
        return data

    def get(self, **request_arguments):
        return self.request_with_retry('get', **request_arguments)

    def head(self, **request_arguments):
        return self.request_with_retry('head', **request_arguments)

    def option(self, **request_arguments):
        return self.request_with_retry('option', **request_arguments)

    def post(self, **request_arguments):
        return self.request_with_retry('post', **request_arguments)

    def put(self, **request_arguments):
        return self.request_with_retry('put', **request_arguments)

    def patch(self, **request_arguments):
        return self.request_with_retry('patch', **request_arguments)

    def delete(self, object_id, **request_arguments):
        return self.request_with_retry('delete', **request_arguments)

    def format_return_data(self, response):
        if response.status_code == 204 or self.raw:
            return response
        elif self.is_json:
            try:
                return response.json()
            except ValueError as e:
                if 'JSON' not in getattr(e, 'message', ''):
                    raise
                logger.exception('Failed to decode json file with error message: %s', e)
                return {}
        else:
            return response.content()

    def request_with_retry(self, method, **request_arguments):
        request_arguments = self.augment_request_arguments(**request_arguments)
        retries = 0

        while retries < self.retries:
            try:
                response = getattr(requests, method)(**request_arguments)
                try:
                    if 400 <= response.status_code < 500:
                        http_error_msg = '%s Client Error: %s for url: %s %s' % \
                                         (response.status_code,
                                          response.reason,
                                          response.url,
                                          response.content)
                        raise ProviderHTTPClientException(http_error_msg)
                    # TODO: add more retryable exceptions code
                    elif response.status_code == 502:
                        raise RetryableException('Deployment in progress')
                    elif 500 <= response.status_code < 600:
                        response.raise_for_status()
                except HTTPError as exc:
                    logger.exception(response.content)
                    raise

            except (requests.Timeout, RetryableException):
                logger.debug('Retry request %s %s', method, request_arguments['url'])
                retries += 1
                sleep(5)
            except requests.ConnectionError as e:
                raise ProviderHTTPClientException('Service is not working with error: %s' % e)
            else:
                break  # Exits while loop
        else:
            raise ProviderHTTPClientException('Failed to do request after {} tries'.format(MAX_RETRIES))

        return self.format_return_data(response)


def remote_service(path, headers=None, timeout=120, json=True, raw=False):
    if headers is None:
        headers = {}
    assert isinstance(headers, dict), 'Headers should be a dict!'

    safe_methods = ['get', 'head', 'options']
    unsafe_methods = ['post', 'put', 'patch', 'delete']

    def wrapper(func):
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            if not isinstance(self, ReboticsBaseProvider):
                raise TypeError('This decorator should be used only for subclasses Rebotics Base Providers')

            url = urljoin(self.host, path)
            authentication_headers = self.get_authentication_headers()
            headers.update(authentication_headers)

            session = ProviderRequestProxy(url, headers, timeout, retries=self.retries, json=json, raw=raw, host=self.host)
            self.session = session

            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                logger.exception(e)
                raise

        return inner

    return wrapper


# noinspection PyMethodMayBeStatic
class ReboticsBaseProvider(object):
    def __init__(self, host, **kwargs):
        self.host = host
        # TODO: add host checking

        self.headers = kwargs.get('headers', {})
        self.data = kwargs.get('data', {})
        self.session = None
        self.retries = kwargs.get('retries', MAX_RETRIES)
        self.domain = urlparse(self.host).netloc

    def get_authentication_headers(self):
        return self.headers if self.headers else {}

    @remote_service('/ping/', json=False)
    def ping(self, session, **kwargs):
        return session.get()

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, pformat({
            'host': self.host,
            'headers': self.headers,
        }))
