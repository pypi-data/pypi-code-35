import decimal
import datetime
import enum
import uuid
from typing import (
    get_type_hints,
    Any,
    Callable,
    Dict,
    List,
    Iterable,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)


T = TypeVar("T")  # pylint: disable=invalid-name


def structure(value: Any, goal_type: Any) -> Any:
    """Returns object given a value and type signature to be coerced into.

    :param value: A dict or list composed of primitive type (str, int, float)
        or a primitive type.
    :param goal_type: A type that you would like cast `value` into.

    Usage::

      >>> import datetime
      >>> import dataclass_structor
      >>> dataclass_structor.structure('2018-10-02', datetime.date)
      datetime.datetime(2018, 10, 2)
    """
    if value is None:
        return value
    if hasattr(goal_type, "__origin__") and goal_type.__origin__ is Union:
        return _structure_union(value, goal_type.__args__)
    return _structure_value(value, goal_type)


_STRUCTURE_UNION_TYPE_PRIORITY = (
    datetime.datetime,
    datetime.date,
    uuid.UUID,
    dict,
    list,
    set,
    float,
    int,
    str,
)


def _structure_union(value: Any, union_types: Tuple[Type[T]]) -> Optional[T]:
    results = {}
    for a_type in union_types:
        try:
            results[a_type] = structure(value, a_type)
        except ValueError:
            pass

    for a_type in _STRUCTURE_UNION_TYPE_PRIORITY:
        if a_type in results:
            return results[a_type]
    return None


def _get_types_from_object_or_its_constructor(goal_type):
    own_hints = get_type_hints(goal_type)
    if own_hints:
        return own_hints
    return get_type_hints(goal_type.__init__)


def _try_structure_object(value: Any, goal_type: Any) -> Any:
    try:
        return goal_type(
            **{
                k: structure(v, _get_types_from_object_or_its_constructor(goal_type)[k])
                for k, v in value.items()
            }
        )
    except (KeyError, ValueError):
        pass
    if issubclass(goal_type, dict):
        dict_value_type = goal_type.__args__[1]
        return {k: structure(v, dict_value_type) for k, v in value.items()}
    return None


def _try_convert_string_to_decimal(value):
    try:
        return decimal.Decimal(value)
    except decimal.InvalidOperation as ex:
        raise ValueError from ex


_STRUCTURE_STR_GOAL_TYPE_TO_CONVERSION_MAP: Dict[Type, Callable] = {
    int: int,
    float: float,
    decimal.Decimal: _try_convert_string_to_decimal,
    datetime.datetime: datetime.datetime.fromisoformat,
    datetime.date: datetime.date.fromisoformat,
    uuid.UUID: uuid.UUID,
}


def _try_structure_str(value: str, goal_type: Any) -> Any:
    conversion = _STRUCTURE_STR_GOAL_TYPE_TO_CONVERSION_MAP.get(goal_type)
    if conversion:
        try:
            return conversion(value)
        except ValueError as ex:
            raise ValueError(
                f"Could not convert {value} of type {type(value)} into a {goal_type}."
            ) from ex

    if hasattr(goal_type, "mro") and enum.Enum in goal_type.mro():
        if value in goal_type.__members__:
            return goal_type[value]
        try:
            return getattr(str, goal_type)
        except TypeError as ex:
            raise ValueError(
                f"Could not convert {value} of type {type(value)} into a {goal_type} enum."
            ) from ex
    return value


def _try_structure_int(value: int, goal_type: Any) -> Union[int, decimal.Decimal, str]:
    if goal_type == decimal.Decimal:
        return decimal.Decimal(value)
    if goal_type == str:
        return str(value)
    return value


def _try_structure_float(
    value: float, goal_type: Any
) -> Union[float, decimal.Decimal, None]:
    if goal_type == decimal.Decimal:
        return decimal.Decimal(value)
    if goal_type == float:
        return value
    return None


def _try_structure_list(value: List[Any], goal_type: Any) -> List[Any]:
    list_content_type = goal_type.__args__[0]
    return [structure(v, list_content_type) for v in value]


def _try_structure_set(value: Set[Any], goal_type: Any) -> Set:
    set_content_type = goal_type.__args__[0]
    return set(structure(v, set_content_type) for v in value)


def _try_structure_tuple(value: Tuple[Any], goal_type: Any) -> Tuple:
    tuple_content_types = goal_type.__args__
    return tuple(structure(value[i], t) for i, t in enumerate(tuple_content_types))


# When structuring values the first value in each pair is used as a condition
# which if true will attempt to structure the value using the second item in
# the pair. Both items in the pair will be called with the value as the first
# argument and the "goal type" as the second argument.
# The order of this list of pairs denotes what order values will be structured
# by.
_STRUCTURE_VALUE_CONDITION_CONVERSION_PAIRS: Iterable[Tuple[Callable, Callable]] = [
    (lambda v, gt: isinstance(v, dict), _try_structure_object),
    (lambda v, gt: getattr(gt, "_name", None) == "Tuple", _try_structure_tuple),
    (lambda v, gt: getattr(gt, "_name", None) == "Set", _try_structure_set),
    (lambda v, gt: getattr(gt, "_name", None) == "List", _try_structure_list),
    (lambda v, gt: isinstance(v, float), _try_structure_float),
    (lambda v, gt: isinstance(v, int), _try_structure_int),
    (lambda v, gt: isinstance(v, str), _try_structure_str),
]


def _structure_value(value: Any, goal_type: Type[T]) -> T:
    for condition, conversion in _STRUCTURE_VALUE_CONDITION_CONVERSION_PAIRS:
        if condition(value, goal_type):
            # This could be a good place for PEP 572 the assignment operator
            # but since Python 3.7 is a target we shall do without.
            obj = conversion(value, goal_type)
            if obj is not None:
                return obj
    raise ValueError(
        f"Could not structure: {value} of type {type(value)} into {goal_type}"
    )
