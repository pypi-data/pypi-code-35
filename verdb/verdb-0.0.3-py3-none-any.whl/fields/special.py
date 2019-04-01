from abc import ABC
from typing import Union

from .field import field, Field


class SpecialField(Field, ABC):
    dependencies = []

    @classmethod
    def handles(cls, type):
        raise NotImplementedError


class UnionField(SpecialField):
    type = Union

    def __init__(self, field):
        super().__init__(field)

        if not field.__args__:
            raise TypeError('Union fields must specify possible types')

    @classmethod
    def handles(cls, type):
        return type is Union

    def is_serialized(self, value):
        return True
    is_deserialized = is_serialized

    def _serialize(self, value):
        for type in self.concrete_type.__args__:
            try:
                return field(type, **self.context).serialize(value)
            except ValueError:
                pass

        raise ValueError(f'{value!r} is not in {self.concrete_type!r}')

    def _deserialize(self, value):
        for type in self.concrete_type.__args__:
            try:
                return field(type, **self.context).deserialize(value)
            except ValueError:
                pass

        raise ValueError(f'{value!r} is not in {self.concrete_type!r}')


class OptionalField(UnionField):
    dependencies = [Union]
    default = None
