from urllib.parse import urlparse, parse_qs
from .. import exceptions, settings
from .proxy import ObjectProxy
from .transport import RequestsTransport


class RequestBundle(object):
    def __init__(self, client, included):
        self.client = client
        self.included = included


class Client(object):
    def __init__(self, access_token=None, client_id=None, client_secret=None):
        if client_id is None:
            client_id = settings.CLIENT_ID

        if client_secret is None:
            client_secret = settings.CLIENT_SECRET

        if not client_id:
            raise exceptions.ConfigurationError(
                'Missing PODIANT_CLIENT_ID setting.'
            )

        if not client_secret:
            raise exceptions.ConfigurationError(
                'Missing PODIANT_CLIENT_SECRET setting.'
            )

        self.__cache = {}
        self.__transport = RequestsTransport(
            client_id,
            client_secret,
            access_token
        )

    def load(self, path, **query):
        response = self.__transport.get(path, **query)
        data = response['data']
        return data

    def get(self, path, **params):
        response = self.__transport.get(path, **params)
        data = response['data']

        if isinstance(data, list):
            while True:
                for datum in data:
                    yield self.__proxy__(
                        datum['type'],
                        urlparse(datum['links']['self']).path[1:],
                        id=datum['id'],
                        attributes=datum['attributes'],
                        links=datum['links'],
                        meta=datum.get('meta', {}),
                        relationships=datum.get('relationships', {}),
                        included=response.get('included')
                    )

                links = response.get('links', {})
                if links.get('next'):
                    query = parse_qs(urlparse(links['next']).query)
                    params['page'] = query['page'][0]
                    response = self.__transport.get(path, **params)
                    data = response['data']
                else:
                    break
        else:
            yield self.__proxy__(
                data['type'],
                urlparse(data['links']['self']).path[1:],
                id=data['id'],
                attributes=data['attributes'],
                links=data['links'],
                meta=data.get('meta', {}),
                relationships=data.get('relationships', {}),
                included=response.get('included')
            )

    def post(self, path, data):
        response = self.__transport.post(path, data)
        data = response['data']

        if isinstance(data, list):
            return [
                self.__proxy__(
                    datum['type'],
                    urlparse(datum['links']['self']).path[1:],
                    id=datum['id'],
                    attributes=datum['attributes'],
                    links=datum['links'],
                    meta=datum.get('meta', {}),
                    relationships=datum.get('relationships', {}),
                    included=response.get('included')
                ) for datum in data
            ]

        return self.__proxy__(
            data['type'],
            urlparse(data['links']['self']).path[1:],
            id=data['id'],
            attributes=data['attributes'],
            links=data['links'],
            meta=data.get('meta', {}),
            relationships=data.get('relationships', {}),
            included=response.get('included')
        )

    def patch(self, path, data):
        response = self.__transport.patch(path, data)
        data = response['data']

        return {
            'type': data['type'],
            'id': data['id'],
            'attributes': data['attributes'],
            'links': data['links'],
            'meta': data.get('meta', {}),
            'relationships': data.get('relationships', {}),
            'included': response.get('included')
        }

    def __proxy__(self, kind, path, qs={}, **kwargs):
        cls_name = '%sEntity' % (
            kind.replace('-', ' ').title().replace(' ', '')
        )

        cls = type(cls_name, (ObjectProxy,), {})
        included = kwargs.pop('included', {})
        return cls(
            bundle=RequestBundle(self, included),
            path=path,
            query=qs,
            kind=kind,
            **kwargs
        )

    def __getattr__(self, attr):
        kind = attr.replace('_', '-')
        if kind not in self.__cache:
            self.__cache[kind] = self.__proxy__(kind, '%s/' % kind)

        return self.__cache[kind]
