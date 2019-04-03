from base64 import b64encode, b64decode
from enum import Enum

from .field import Field


class NoneField(Field):
    type = type(None)
    nullable = True

    def is_serialized(self, value):
        return value is None
    is_deserialized = is_serialized

    def _serialize(self, value):
        return None
    _deserialize = _serialize


class ScalarField(Field):
    types = bool, int, float, complex, str

    def is_serialized(self, value):
        return isinstance(value, self.type)
    is_deserialized = is_serialized

    def _serialize(self, value):
        return self.concrete_type(value)

    def _deserialize(self, value):
        return self.concrete_type(value)


class BinaryField(Field):
    types = bytes, bytearray, memoryview

    def is_serialized(self, value):
        return isinstance(value, str)

    def is_deserialized(self, value):
        return isinstance(value, self.types)

    def _serialize(self, value):
        return b64encode(value).decode()

    def _deserialize(self, value):
        return self.type(b64decode(value.encode()))


class EnumField(Field):
    type = Enum

    def is_deserialized(self, value):
        return isinstance(value, self.type)

    def _serialize(self, value):
        return value.value

    def _deserialize(self, value):
        return self.concrete_type(value)
