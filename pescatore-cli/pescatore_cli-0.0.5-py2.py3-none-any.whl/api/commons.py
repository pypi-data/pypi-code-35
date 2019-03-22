import requests

from .. import settings


def _get_headers(custom=None):
    headers = {
        'content-type': 'application/json'
    }

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
        headers['X-Consumer-Groups'] = settings.PESCATORE_CLI_CONSUMER_GROUPS_HEADER

    # merge headers
    if custom is not None and type(custom) == dict:
        headers = {**headers, **custom}

    return headers


def make_request(path, params, payload=None, method='GET', headers=None):
    timeout = settings.REQUEST_TIMEOUT
    headers = _get_headers(headers)
    url = '{base_url}{path}'.format(base_url=settings.PESCATORE_BASE_URL,
                                    path=path)
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
