from abc import ABC
from functools import lru_cache


fields = []


def field(type, **kwargs):
    field = _field(type)
    field.context = kwargs
    return field


@lru_cache(maxsize=None)
def _field(concrete_type):
    generic_type = _resolve_typing(concrete_type)
    field = next(field for field in fields if field.handles(generic_type))
    return field(concrete_type)


def _resolve_typing(type):
    return _resolve_typing(type.__origin__) if hasattr(type, '__origin__') else type


class ResolveTypeDescriptor:
    def __init__(self):
        self.resolved = None

    def __get__(self, _, cls):
        if not self.resolved:
            self.resolved = _resolve_typing(cls.type)
        return self.resolved


class DependencyDescriptor:
    def __get__(self, _, cls):
        return cls.generic_type.__mro__


# TODO: Add repr
class Field(ABC):
    type = None
    nullable = False
    dependencies = DependencyDescriptor()

    def __init_subclass__(cls):
        super().__init_subclass__()
        cls.generic_type = ResolveTypeDescriptor()

        if cls.type:
            dependency_indices = (idx for idx, cls_ in enumerate(fields) if cls_.generic_type in cls.dependencies)
            idx = next(dependency_indices, len(fields))
            fields.insert(idx, cls)

        elif hasattr(cls, 'types'):
            for type_ in cls.types:
                name = next(getattr(type_, attr) for attr in ['__name__', '_name'] if hasattr(type_, attr))
                type(f'{cls.__name__}{name.title()}', (cls,), {'type': type_})

    def __init__(self, concrete_type):
        self.concrete_type = concrete_type
        self.context = {}

    def __getattr__(self, name):
        if name in self.context:
            return self.context[name]
        else:
            raise AttributeError(f'Missing "{name}" in context')

    @classmethod
    def handles(cls, type):
        return hasattr(type, '__mro__') and issubclass(type, cls.generic_type)

    def is_serialized(self, value):
        return value is not None

    def is_deserialized(self, value):
        return value is not None

    def serialize(self, value):
        if self.is_deserialized(value):
            return self._serialize(value)
        elif self.is_serialized(value):
            return value
        else:
            raise ValueError(f'Invalid type {type(value)!r} for field {self!r}')

    def deserialize(self, value):
        if self.is_serialized(value):
            return self._deserialize(value)
        elif self.is_deserialized(value):
            return value
        else:
            raise ValueError(f'Invalid type {type(value)!r} for field {self!r}')

    def _serialize(self, value):
        raise NotImplementedError

    def _deserialize(self, value):
        raise NotImplementedError
