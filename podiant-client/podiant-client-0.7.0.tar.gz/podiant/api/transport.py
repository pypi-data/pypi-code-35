from json.decoder import JSONDecodeError
from .. import exceptions, settings
import requests


class RequestsTransport(object):
    def __init__(self, client_id, client_secret, access_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token

    def _request(self, method, path, *args, **kwargs):
        proto = 'https' if settings.SSL else 'http'
        url = '%s://%s/%s' % (proto, settings.DOMAIN, path)

        params = kwargs.pop('params', {})
        params['client_id'] = self.client_id

        if self.access_token:
            params['access_token'] = self.access_token

        method = getattr(requests, method.lower())
        response = method(
            url,
            params=params,
            headers={
                'Authorization': 'Bearer %s' % self.client_secret,
                'Content-Type': 'application/vnd.api+json',
                'Accepts': 'application/vnd.api+json'
            },
            verify=False,
            *args,
            **kwargs
        )

        try:
            json = response.json()
        except JSONDecodeError:
            raise exceptions.BadResponseError(
                'Server did not reply with JSON-API data.'
            )

        if response.status_code == 400:
            raise exceptions.BadRequestError(
                json['error'].get('detail') or json['error'].get('title'),
                json['error'].get('meta')
            )

        if response.status_code == 401:
            raise exceptions.UnauthorizedError(
                json['error'].get('detail') or json['error'].get('title'),
                json['error'].get('meta')
            )

        if response.status_code == 403:
            raise exceptions.ForbiddenError(
                json['error'].get('detail') or json['error'].get('title'),
                json['error'].get('meta')
            )

        if response.status_code == 404:
            raise exceptions.NotFoundError(
                json['error'].get('detail') or json['error'].get('title'),
                json['error'].get('meta')
            )

        if response.status_code == 405:
            raise exceptions.MethodNotAllowedError(
                json['error'].get('detail') or json['error'].get('title'),
                json['error'].get('meta')
            )

        if response.status_code == 406:
            raise exceptions.NotAcceptableError(
                json['error'].get('detail') or json['error'].get('title'),
                json['error'].get('meta')
            )

        if response.status_code == 409:
            raise exceptions.ConflictError(
                json['error'].get('detail') or json['error'].get('title'),
                json['error'].get('meta')
            )

        if response.status_code == 415:
            raise exceptions.UnsupportedMediaTypeError(
                json['error'].get('detail') or json['error'].get('title'),
                json['error'].get('meta')
            )

        if response.status_code == 422:
            raise exceptions.UnprocessableEntityError(
                json['error'].get('detail') or json['error'].get('title'),
                json['error'].get('meta')
            )

        if response.status_code < 200 or response.status_code >= 400:
            raise exceptions.UnknownError(
                json['error'].get('detail') or json['error'].get('title'),
                json['error'].get('meta')
            )

        return json

    def get(self, path, **kwargs):
        return self._request('GET', path, params=kwargs)

    def post(self, path, data={}):
        return self._request('POST', path, json=data)

    def patch(self, path, data={}):
        return self._request('PATCH', path, json=data)
