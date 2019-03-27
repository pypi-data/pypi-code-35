import decimal
import datetime
import enum
import uuid
from dataclasses import fields, is_dataclass
from typing import Any, Callable, Iterable, Tuple


def unstructure(value: Any) -> Any:
    """Returns dictionary, composed of simple types, given a value of a
    particular type.

    :param value: An object that you would like to convert into a serializable
        object.

    Usage::

      >>> import datetime
      >>> import dataclass_structor

      >>> dataclass_structor.unstructure(datetime.date(2018, 9, 5))
      "2018-09-05"
    """
    for condition, conversion in _UNSTRUCTURE_VALUE_CONDITION_CONVERSION_PAIRS:
        if condition(value):
            return conversion(value)

    raise ValueError(f"Could not unstructure: {value}")


_UNSTRUCTURE_VALUE_CONDITION_CONVERSION_PAIRS: Iterable[Tuple[Callable, Callable]] = [
    (lambda v: v is None, lambda v: v),
    (lambda v: isinstance(v, str), lambda v: v),
    (lambda v: isinstance(v, float), lambda v: v),
    (lambda v: isinstance(v, int), lambda v: v),
    (lambda v: isinstance(v, decimal.Decimal), str),  # `str` is a constructor here
    (lambda v: isinstance(v, uuid.UUID), str),
    (lambda v: isinstance(v, enum.Enum), lambda v: v.name),
    (
        lambda v: isinstance(v, (datetime.datetime, datetime.date)),
        lambda v: v.isoformat(),
    ),
    (lambda v: isinstance(v, list), lambda v: [unstructure(i) for i in v]),
    (lambda v: isinstance(v, tuple), lambda v: tuple([unstructure(i) for i in v])),
    (
        lambda v: isinstance(v, set),
        lambda v: set([unstructure(i) for i in v]),  # pylint: disable=R1718
    ),
    (
        lambda v: isinstance(v, dict),
        lambda value: {k: unstructure(v) for k, v in value.items()},
    ),
    (
        is_dataclass,
        lambda v: {f.name: unstructure(getattr(v, f.name)) for f in fields(v)},
    ),
    (
        lambda v: hasattr(v, "__slots__"),
        lambda v: {f: unstructure(getattr(v, f)) for f in v.__slots__},
    ),
]
