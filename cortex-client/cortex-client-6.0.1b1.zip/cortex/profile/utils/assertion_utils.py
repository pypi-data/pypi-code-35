from typing import Callable, Any

__all__ = [
    'first_arg_is_type_wrapper',
]


def first_arg_is_type_wrapper(_callable, tuple_of_types) -> Callable[[Any], bool]:
    return lambda x: x if not isinstance(x, tuple_of_types) else _callable(x)
