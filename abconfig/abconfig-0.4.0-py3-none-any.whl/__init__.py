__version__ = '0.4.0'

from os import getcwd
from copy import deepcopy
from functools import reduce

from abconfig.common import Container
from abconfig.load import File, Env


class ABConfig(Container):
    file = getcwd() + '/config.json'
    loaders = (File, Env,)
    _reserved_attr = (
        'loaders',
        'file',
    )

    def __init__(self, **kwargs):
        super().__init__()
        self._args = self._attrs(**kwargs)
        self._data = self._get(**self._args)

    def _get(self, **kwargs):
        result = dict()
        for name, value in kwargs.items():
            result.update(self._load(name, value))
        return result

    def _load(self, name, source):
        values = deepcopy(source)
        for loader in self.loaders:
            if reduce(lambda a, b: a or b,
                    map(
                        lambda x: isinstance(values, x),
                        (int, str, bool, list, tuple))
                    ):
                read = loader(
                    prefix=None,
                    source=(name,),
                    path=self.file
                ).get()
                if read: values = read[name]

            elif isinstance(values, dict):
                read = loader(
                    prefix=name,
                    source=source.keys(),
                    path=self.file
                ).get()
                if read: values.update(read)

        return {name: values}

    def _attrs(self, **kwargs):
        result = {}
        for attr in type(self).__dict__.keys():
            if (attr[:2] != '__' and attr[:1] != '_' and
                    attr not in self._reserved_attr):
                result.update({str(attr): getattr(self, attr)})

        if kwargs: result.update(kwargs)
        return result
