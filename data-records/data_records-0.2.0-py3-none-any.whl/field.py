"""
Fields are wrappers around the declarations on classes.
"""
from typing import List

from .utilities import MISSING


class Field:
    """Temporary wrapper around  a field used for parsing fields on a data record"""
    __slots__ = ('name', 'type', 'default')

    def __init__(self, name, annotated_type, default):
        self.name = name
        self.type = annotated_type
        self.default = default

    def __repr__(self):
        return f"Field({self.name}, {self.type}, {self.default})"

    @staticmethod
    def list_for_class(target_class) -> List['Field']:
        """Generate a list of fields from a class"""
        annotations = target_class.__dict__.get('__annotations__', {})

        def _make_field(name_type: tuple) -> 'Field':
            name, annotated_type = name_type
            return Field(name, annotated_type, getattr(target_class, name, MISSING))

        return list(map(_make_field, annotations.items()))
