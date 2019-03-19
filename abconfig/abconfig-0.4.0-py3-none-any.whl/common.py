class Container:
    _base_classes = ('Container', 'ABConfig')

    def __init__(self):
        if type(self).__name__ in self._base_classes:
            raise NotImplementedError

    def __getattr__(self, attr):
        if not attr in type(self._data).__dict__.keys():
            raise AttributeError
        return getattr(self._data, attr)

    def __getitem__(self, item):
        return self.get(item)

    def get(self, item=None, default=None):
        if not item:
            return self._data
        if not item in self._data:
            return default
        return self._data[item]


class Loader(Container):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._data = self.default_handler(*args, **kwargs)

    def default_handler(self, *args, **kwargs):
        raise NotImplementedError


class Cache(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        if not args[0] in cls.instances:
            cls.instances[args[0]] = super(Cache, cls).__call__(*args, **kwargs)
        return cls.instances[args[0]]


class CachedObj(Loader, metaclass=Cache):
    """ Created once and stored in the Cache.instances dictionary,
        first positional arg is unique object id to be created
    """
