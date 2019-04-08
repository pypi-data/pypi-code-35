from datetime import date
from dateutil.parser import parse as parse_date
from types import GeneratorType
from urllib.parse import urlparse


class DictProxy(object):
    def __init__(self, request, data):
        self.__request = request
        self.__data = data

    def __getattr__(self, attr):
        try:
            return self.__data[attr]
        except KeyError:
            raise AttributeError(
                '\'%s\' has no attribute \'%s\'' % (
                    type(self).__name__,
                    attr
                )
            )


class AttributeProxy(object):
    def __init__(self, request, name):
        self.__locked = True
        self.__request = request
        self.__name = name
        self.__populated = False
        self.__value = None

    def __getvalue__(self):
        if not self.__populated:
            self.__request.__populate__()

        return self.__value

    def __setvalue__(self, value):
        self.__value = value
        self.__populated = True

    def __abs__(self):
        return self.__getvalue__().__abs__()

    def __and__(self, other):
        return self.__getvalue__().__and__(other)

    def __bool__(self):
        return bool(self.__getvalue__())

    def __ceil__(self):
        return self.__getvalue__().__ceil__()

    def __cmp__(self, other):
        return self.__getvalue__().__cmp__(other)

    def __dir__(self):
        return self.__getvalue__().__dir__()

    def __doc__(self):
        return self.__getvalue__().__doc__()

    def __eq__(self, other):
        return self.__getvalue__() == other

    def __float__(self):
        return self.__getvalue__().__float__()

    def __floor__(self):
        return self.__getvalue__().__floor__()

    def __format__(self, f):
        return self.__getvalue__().__format__(f)

    def __ge__(self, other):
        return self.__getvalue__() >= other

    def __get__(self, key):
        return self.__getvalue__().__get__(key)

    def __gt__(self, other):
        return self.__getvalue__() > other

    def __hash__(self):
        return self.__getvalue__().__hash__()

    def __int__(self):
        return int(self.__getvalue__())

    def __iter__(self):
        return self.__getvalue__().__iter__()

    def __le__(self, other):
        return self.__getvalue__() <= other

    def __len__(self):
        return len(self.__getvalue__())

    def __lt__(self, other):
        return self.__getvalue__() < other

    def __ne__(self, other):
        return self.__getvalue__() != other

    def __or__(self, other):
        return self.__getvalue__() or other

    def __pos__(self):
        return self.__getvalue__().__pos__()

    def __repr__(self):
        return self.__getvalue__().__repr__()

    def __round__(self, *args):
        return self.__getvalue__().__round__(*args)

    def __str__(self):
        return str(self.__getvalue__())

    def __getattr__(self, attr):
        value = self.__getvalue__()
        return getattr(value, attr)

    def __call__(self, **kwargs):
        path = '%s%s/' % (self.__request.path, self.__name)
        return self.__request.bundle.client.post(path, kwargs)

    def to(self, totype):
        try:
            converter = {
                'str': str,
                'unicode': str,
                'int': int,
                'float': float,
                'bool': bool,
                'list': list,
                'tuple': tuple,
                'set': set,
                'dict': dict,
                'date': parse_date,
                'datetime': parse_date
            }[totype]
        except KeyError:
            raise TypeError('Unknown type: \'%s\'', totype)

        return converter(self.__getvalue__())


class RelationshipProxy(object):
    def __init__(self, request, data):
        urlparts = urlparse(data['links']['related'])

        self.__path = urlparts.path[1:]
        self.__request = request
        self.__populated = False
        self.__value = None

        if 'data' in data:
            if not self.__populated:
                self.__value = []

            single = False
            if isinstance(data['data'], dict):
                data['data'] = [data['data']]
                single = True

            for item in data['data']:
                for inclusion in request.bundle.included:
                    if item['type'] == inclusion['type']:
                        if item['id'] == inclusion['id']:
                            cls_name = '%sEntity' % (
                                item['type'].replace(
                                    '-', ' '
                                ).title().replace(
                                    ' ', ''
                                )
                            )

                            cls = type(cls_name, (ObjectProxy,), {})
                            self.__value.append(
                                cls(
                                    bundle=request.bundle,
                                    path=inclusion['links']['self'],
                                    kind=item['type'],
                                    id=item['id'],
                                    attributes=inclusion['attributes'],
                                    links=inclusion['links'],
                                    meta=inclusion.get('meta', {}),
                                    relationships=inclusion.get(
                                        'relationships',
                                        {}
                                    )
                                )
                            )

            if single and any(self.__value):
                self.__value = self.__value[0]
                self.__populated = True
            elif not single:
                self.__populated = True

    def __getvalue__(self):
        if not self.__populated:
            self.__value = self.__request.bundle.client.get(self.__path)

        return self.__value

    def __len__(self):
        self.__getvalue__()

        if isinstance(self.__value, GeneratorType):
            self.__value = list(self.__value)

        return len(self.__value)

    def __iter__(self):
        return self.__getvalue__().__iter__()

    def __getattr__(self, attr):
        return getattr(self.__getvalue__(), attr)


class ObjectProxy(object):
    def __init__(
        self,
        bundle, path, query={},
        kind=None, id=None, attributes=None,
        links=None, relationships=None, meta=None
    ):
        self.__bundle = bundle
        self.__path = path
        self.__query = query
        self.__id = id
        self.__kind = kind
        self.__cache = {}
        self.__attributes = attributes if attributes is not None else {}
        self.__rels = relationships if relationships is not None else {}
        self.__dirty = {}

        if links is not None:
            cls_name = '%sLinkCollection' % (
                kind.replace('-', ' ').title().replace(' ', '')
            )

            cls = type(
                cls_name,
                (DictProxy,),
                {}
            )

            self.__links = cls(self, links)

        if meta is not None:
            cls_name = '%sMetaCollection' % (
                kind.replace('-', ' ').title().replace(' ', '')
            )

            cls = type(
                cls_name,
                (DictProxy,),
                {}
            )

            self.__meta = cls(self, meta)

    def __repr__(self):
        if self.__id is not None:
            return '<%s %s>' % (
                type(self).__name__,
                self.__id
            )

        return '<%s>' % type(self).__name__

    def __str__(self):
        return self.__repr__()

    def dict(self):
        if self.__id is None or self.__kind is None:
            self.__populate__()

        if self.__id is None:
            raise AttributeError(
                '\'%s\' has no attribute \'dict\'' % (
                    type(self).__name__
                )
            )

        d = dict(**self.__attributes)
        d['id'] = self.__id

        return d

    def include(self, *items):
        include = self.__query.get('include', '').split(',')
        include.extend(items)
        self.__query['include'] = ','.join(
            sorted(
                set(
                    [i for i in include if i and i.strip()]
                )
            )
        )

        return self

    def order_by(self, *fields):
        sort = self.__query.get('sort', '').split(',')
        sort.extend(fields)
        self.__query['sort'] = ','.join(
            sorted(
                set(
                    [s for s in sort if s and s.strip()]
                )
            )
        )

        return self

    def all(self):
        return self.filter()

    def __iter__(self):
        return self.all().__iter__()

    def filter(self, id=None, **kwargs):
        if id:
            Model = type(self)
            path = '%s%s/' % (self.__path, id)
            return Model(self.__bundle, path)

        query = dict(**self.__query)
        for key, value in kwargs.items():
            query['filter[%s]' % key] = value

        return self.__bundle.client.get(self.__path, **query)

    def only_published(self):
        query = dict(**self.__query)
        query['status'] = 'published'

        return self.__bundle.client.get(self.__path, **query)

    def __getattr__(self, attr):
        if attr == 'links':
            if self.__id is None and self.__kind is None:
                self.__populate__()

            return self.__links

        if attr == 'meta':
            if self.__id is None and self.__kind is None:
                self.__populate__()

            return self.__meta

        if attr in 'bundle':
            return self.__bundle

        if attr in 'path':
            return self.__path

        if attr in 'id':
            return self.__id

        if attr not in self.__cache:
            jsonapi_version = attr.replace('_', '-')
            self.__cache[attr] = AttributeProxy(self, jsonapi_version)

            if jsonapi_version in self.__attributes:
                self.__cache[attr].__setvalue__(
                    self.__attributes[jsonapi_version]
                )
            elif jsonapi_version in self.__rels:
                self.__cache[attr].__setvalue__(
                    RelationshipProxy(
                        self,
                        self.__rels[jsonapi_version]
                    )
                )

        return self.__cache[attr]

    def __setattr__(self, attr, value):
        if attr.startswith('_'):
            super().__setattr__(attr, value)
            return

        if self.__id is None and self.__kind is None:
            self.__populate__()

        jsonapi_version = attr.replace('_', '-')

        if jsonapi_version not in self.__attributes:
            raise AttributeError(
                '\'%s\' object has no attribute \'%s\'' % (
                    type(self).__name__,
                    attr
                )
            )

        v = None
        if isinstance(value, date):
            v = value.isoformat()
        else:
            v = value

        self.__cache[attr] = AttributeProxy(
            self, jsonapi_version
        )

        self.__cache[attr].__setvalue__(v)
        self.__dirty[jsonapi_version] = v

    def __populate__(self, data=None):
        if data is None:
            if self.__id is not None or self.__kind is not None:
                return

            data = self.__bundle.client.load(self.__path, **self.__query)

        self.__kind = data['type']
        self.__id = data['id']
        self.__attributes = data['attributes']
        self.__rels = data.get('relationships', {})
        self.__dirty = {}

        for jsonapi_version, value in data['attributes'].items():
            python_version = jsonapi_version.replace('-', '_')
            if python_version not in self.__cache:
                self.__cache[python_version] = AttributeProxy(
                    self, jsonapi_version
                )

            self.__cache[python_version].__setvalue__(value)

        for jsonapi_version, value in data.get('relationships', {}).items():
            python_version = jsonapi_version.replace('-', '_')
            if python_version not in self.__cache:
                self.__cache[python_version] = AttributeProxy(
                    self, jsonapi_version
                )

            self.__cache[python_version].__setvalue__(
                RelationshipProxy(self, value)
            )

        cls_name = '%sLinkCollection' % (
            data['type'].replace('-', ' ').title().replace(' ', '')
        )

        cls = type(
            cls_name,
            (DictProxy,),
            {}
        )

        self.__links = cls(self, data['links'])

        cls_name = '%sMetaCollection' % (
            data['type'].replace('-', ' ').title().replace(' ', '')
        )

        cls = type(
            cls_name,
            (DictProxy,),
            {}
        )

        self.__meta = cls(self, data.get('meta'))

    def save(self):
        if not any(self.__dirty.keys()):
            pass

        data = self.__bundle.client.patch(
            self.__path,
            {
                'data': {
                    'type': self.__kind,
                    'id': self.__id,
                    'attributes': self.__dirty
                }
            }
        )

        self.__populate__(data)
