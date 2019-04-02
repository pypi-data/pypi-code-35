# built-in
import os.path
from hashlib import sha256
from urllib.parse import unquote

# app
from ._cached_property import cached_property


class _PathLink:
    def __init__(self, link):
        self.short = link.split('#')[0]
        self.long = link

    @classmethod
    def parse(cls, link):
        if '@' in link:
            return
        if link.startswith('file://'):
            link = link[len('file://'):]
        if '://' in link:
            return

        path = link.replace('/', os.path.sep).split('#')[0]
        if not cls._check(path):
            return

        return cls(link)

    @staticmethod
    def _check(path: str) -> bool:
        raise NotImplementedError

    @property
    def name(self):
        # get last part of path
        path = os.path.abspath(self.short.replace('/', os.path.sep))
        name = os.path.basename(path)

        # drop all extensions, because in Python package name has no dots
        name = name.split('.')[0]
        # pip can return urlencoded name
        name = unquote(name)
        return name or None

    @cached_property
    def hash(self) -> str:
        with open(self.short, 'rb') as stream:
            content = stream.read()
        hasher = sha256()
        hasher.update(content)
        return 'sha256:' + hasher.hexdigest()

    def __str__(self):
        return self.long

    def __repr__(self) -> str:
        return '{}({})'.format(type(self).__name__, str(self))


class FileLink(_PathLink):

    @staticmethod
    def _check(path: str) -> bool:
        if os.path.isfile(path):
            return True
        if '://' in path:
            return False
        return path.endswith('.py')


class DirLink(_PathLink):

    @staticmethod
    def _check(path: str) -> bool:
        return os.path.isdir(path)
