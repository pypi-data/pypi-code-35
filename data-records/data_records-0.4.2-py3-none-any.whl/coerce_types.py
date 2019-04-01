"""
Module for Coercing Types for data records.
"""
from copy import deepcopy
from typing import Any, TypeVar


def is_of_type(data, type_hint) -> bool:
    """
    Checks if data adheres to type_hint
    """
    if type_hint is Any or (data is None and type(None) == type_hint) or isinstance(data, type_hint.__class__):
        return True
    if getattr(type_hint, '_name', '') == 'List':
        return isinstance(data, list) and all([is_of_type(item, type_hint.__args__[0]) for item in data])
    if getattr(type_hint, '_name', '') == 'Set':
        return isinstance(data, set) and all([is_of_type(item, type_hint.__args__[0]) for item in data])
    if hasattr(type_hint, '__args__'):  # Recursively Check Union Types
        return any(map(lambda k: is_of_type(data, k), type_hint.__args__))
    return False


T = TypeVar('T')


def coerce_collection(data, type_hint):
    """
    Coercion for List and Set types
    """
    if isinstance(data, (list, set)):
        sub_type = type_hint.__args__[0]
        collection_type = list if getattr(type_hint, '_name') == 'List' else set
        cleaned_data = collection_type(coerce_type(item, sub_type) for item in data)
    else:
        try:
            cleaned_data = coerce_type(eval(data), type_hint)  # pylint:disable=eval-used
        except SyntaxError:
            raise ValueError(f'Data {data!r} cannot be coerced to {type_hint!r} from type {type(data)}')
    return cleaned_data


def coerce_union(data, type_hint):
    """Coerce Union Types in order of declared types"""
    for klass in type_hint.__args__:
        try:
            cleaned_data = coerce_type(data, klass)
            break
        except Exception:
            pass
    else:
        raise ValueError(f'Data {data!r} cannot be coerced to {type_hint!r} from type {type(data)}')
    return cleaned_data


def coerce_type(data, type_hint):
    """
    Function that takes data and a type hint and tries to coerce the data to the specified type.

    This function will not try to coerce `Any` or `Optional[Any]` Type hints. The primary
    difference between `Any` and `Optional[Any]` happens in an earlier step in the
    CreateableBase.create method, where `Optional[Any]` fields can be missing, where just
    `Any` fields have to be present but can be any type.
    """
    cleaned_data = deepcopy(data) if data != "" else None
    if not is_of_type(cleaned_data, type_hint):
        if hasattr(type_hint, '_record_fields'):
            cleaned_data = type_hint.from_dict(cleaned_data)
        elif not hasattr(type_hint, '__args__'):  # native type coercion
            cleaned_data = type_hint(cleaned_data)
        elif getattr(type_hint, '_name') in ('List', 'Set'):
            cleaned_data = coerce_collection(cleaned_data, type_hint)
        else:
            cleaned_data = coerce_union(cleaned_data, type_hint)
    return cleaned_data
