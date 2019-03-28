"""
Data Record Module.
"""
from typing import Dict

from data_records.coerce_types import coerce_type


class DataRecord:
    """
    Data Record with Type Coercion.
    """
    __aliases__: Dict[str, str] = {}

    @classmethod
    def from_dict(cls, from_dict):
        """
        Method to create a dataclass from a dict.
        Checks that all non-optional fields are in the provided dict.
        Casts all empty strings to None (Athena returns empty string instead of none).
        Tries to Coerce any data types to the annotated type.
        """
        cleaned_args = {}
        for key, type_hint in cls.__annotations__.items():  # noqa
            data = from_dict.get(key, None)
            if data is None:
                data = from_dict.get(cls.__aliases__.get(key), None)  # type: ignore
            if key not in from_dict:
                if not hasattr(type_hint, '__args__') or type(None) not in type_hint.__args__:  # noqa
                    raise KeyError(key)
            if data == "":
                data = None
            cleaned_args[key] = coerce_type(data, type_hint)
        return cls(**cleaned_args)  # type: ignore
