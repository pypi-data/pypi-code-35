from collections import OrderedDict
from itertools import chain, repeat, islice
from pathlib import Path, PurePosixPath

from ruamel.yaml import YAML

from .fields.field import Field
from .manager import Manager
from .repository import Repository
from .section import Section


class PathDescriptor:
    def __init__(self, key):
        self.key = key

    def __get__(self, obj, cls):
        if obj:
            if hasattr(obj, self.key):
                return PurePosixPath(cls.path, f'{getattr(obj, self.key)}.yml')
            else:
                raise ValueError(f'Missing {self.key} for model')
        else:
            return PurePosixPath(f'{cls.__name__.lower()}s')


class Model(Section):
    class DoesNotExist(Exception):
        pass

    def __init_subclass__(cls, repository=None, **kwargs):
        super().__init_subclass__()
        cls.objects = Manager(cls)

        if not repository:
            repository = kwargs.pop('repo', None)
        if isinstance(repository, Repository):
            cls.repository = repository
        elif repository:
            cls.repository = Repository(repository)
        else:
            cls.repository = None

        class DoesNotExist(Model.DoesNotExist):
            pass
        cls.DoesNotExist = DoesNotExist

    def __init__(self, _=None, *, key=None, **kwargs):
        self.key = key
        self._loaded_key = None
        self.version = None

        super().__init__(_=_, **kwargs)

    def __repr__(self):
        if not self._loaded_key and self.version:
            return f'{type(self).__name__}(key={self.key!r}, version={self.version!r})'
        else:
            return super().__repr__().replace('(', f'(key={self.key!r}, ', 1)

    def __getattribute__(self, name):
        if name != '_type_hints' and name in self._type_hints and self.is_reference:
            self.load()

        return object.__getattribute__(self, name)

    def __eq__(self, other):
        assert type(self) == type(other)
        if self.is_reference or other.is_reference:
            return (self.is_reference or not self.dirty) and \
                   (other.is_reference or not other.dirty) and \
                   self.version == other.version
        else:
            return super().__eq__(other)

    def __hash__(self):
        if self.dirty:
            raise ValueError("Dirty models can't be hashed")
        return hash((self.key, self.version))

    path = PathDescriptor('key')
    _loaded_path = PathDescriptor('_loaded_key')

    @property
    def is_reference(self):
        return bool(not self._loaded_key and self.version)

    def versions(self):
        if self.version:
            path = self._loaded_path if self._loaded_key else self.path
            commits = self.repository.git('log', '--format=oneline', '--follow', self.version, '--', path)
            return OrderedDict(islice(chain(line.split(maxsplit=1), repeat('')), 2) for line in commits.splitlines())
        else:
            return OrderedDict()

    def load(self):
        data = YAML(typ='safe').load(self.repository.git('show', f'{self.version}:{self.path}'))
        self.deserialize(data, version=self.version)

        self._loaded_key = self.key
        self.dirty = False

    def save(self, message=''):
        with self.repository.commit(message) as work_tree:
            file = Path(work_tree, self.path)
            file.parent.mkdir(parents=True, exist_ok=True)

            with file.open('w', encoding='utf-8') as handle:
                YAML(typ='safe').dump(self.serialize() or {}, handle)

            if self._loaded_key and self.key != self._loaded_key:
                self.repository.git('rm', self.__loaded_file)

            self._loaded_key = self.key
            self.repository.git('add', file)

        self.version = self.repository.git('rev-parse', 'HEAD')
        self.dirty = False

    def delete(self, message=''):
        with self.repository.commit(message) as work_tree:
            file = Path(work_tree, self.path)
            self.repository.git('rm', file)

        self.version = None
        self.dirty = True


class ModelField(Field):
    type = Model

    def is_serialized(self, value):
        return isinstance(value, str)

    def is_deserialized(self, value):
        return isinstance(value, self.type)

    def _serialize(self, value):
        return value.key

    def _deserialize(self, value):
        return self.concrete_type.objects.get(key=value, version=self.version)
