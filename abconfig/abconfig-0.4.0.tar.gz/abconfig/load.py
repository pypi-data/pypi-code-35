from os import environ

from .common import Loader
from .file import Yaml, Json


class Env(Loader):
    """ Usage:
            Environment.read(prefix=value, source=dict)
    """
    def default_handler(self, *args, **kwargs):
        result = dict()
        prefix = kwargs.get('prefix', None)
        for key in kwargs.get('source'):
            var_name = prefix + '_' + key if prefix else key
            value = environ.get(var_name.upper(), None)
            if value: result.update({key: value})
        return result


class File(Loader):
    """ Usage:
            File.read(prefix=value, source=value, path=value)
    """

    _drivers = (
        Json,
        Yaml,
    )

    def default_handler(self, *args, **kwargs):
        result = dict()
        path = kwargs.get('path')
        prefix = kwargs.get('prefix', None)
        for key in kwargs.get('source'):
            read = self._read_file(path, prefix if prefix else key)
            if isinstance(read, dict):
                value = read.get(key, None)
                if value: result.update({key: value})
            elif read:
                result.update({key: read})
        return result

    def _read_file(self, path, section):
        for driver in self._drivers:
            try:
                read = driver(path).get()
                if not section in read.values():
                    for value in read.values():
                        if isinstance(value, dict) and section in value:
                            return value[section]
                return read[section]
            except Exception:
                continue
        return {}
