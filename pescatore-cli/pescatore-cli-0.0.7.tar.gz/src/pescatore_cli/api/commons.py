import requests

from .. import settings


def _get_headers(custom=None):
    headers = {
        'content-type': 'application/json',
        'X-Forwarded-Host': 'pescatore.pescatore'
    }

    if settings.PESCATORE_CLI_DOMAIN is not None:
        headers['X-Forwarded-Host'] = settings.PESCATORE_CLI_DOMAIN

    if settings.PESCATORE_CLI_API_KEY is not None:
        headers['Authorization'] = '{0} {1}'.format(
            settings.PESCATORE_CLI_API_KEY_HEADER,
            settings.PESCATORE_CLI_API_KEY)

    elif settings.PESCATORE_CLI_JWT is not None:
        headers['Authorization'] = '{0} {1}'.format(
            settings.PESCATORE_CLI_JWT_HEADER,
            settings.PESCATORE_CLI_JWT)

    if settings.PESCATORE_CLI_CONSUMER_HEADER is not None:
        headers['X-Consumer-Username'] = settings.PESCATORE_CLI_CONSUMER_HEADER

    if settings.PESCATORE_CLI_CONSUMER_GROUPS_HEADER is not None:
        headers[
            'X-Consumer-Groups'] = settings.PESCATORE_CLI_CONSUMER_GROUPS_HEADER

    # merge headers
    if custom is not None and type(custom) == dict:
        headers = {**headers, **custom}

    return headers


def make_request(path, params, payload=None, method='GET', headers=None,
                 consumer_id=None):
    timeout = settings.REQUEST_TIMEOUT

    if consumer_id is not None:
        if headers is not None and type(headers) == dict:
            headers['X-Consumer-Username']
        else:
            headers = {
                'X-Consumer-Username': consumer_id
            }

    headers = _get_headers(headers)
    url = '{base_url}{path}'.format(base_url=settings.PESCATORE_BASE_URL,
                                    path=path)

    print('Requesting', url, 'with headers', headers)

    if settings.DEBUG:
        print('CALLING', url, 'with method', method, 'and payload', payload)

    if method == 'GET':
        response = requests.get(url=url, headers=headers, params=params,
                                timeout=timeout)
    elif method == 'POST':
        response = requests.post(url=url, headers=headers, params=params,
                                 json=payload,
                                 timeout=timeout)
    elif method == 'DELETE':
        response = requests.delete(url=url, headers=headers, params=params,
                                   timeout=timeout)

    response.raise_for_status()

    response.encoding = response.apparent_encoding

    data = response.json()

    return data
