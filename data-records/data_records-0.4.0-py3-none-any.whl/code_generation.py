"""Generate the functions on a class programmatically to create a data record."""
import inspect
from functools import partial
from typing import Tuple, Any, List, Callable

from .exceptions import CannotMutateRecordError
from .coerce_types import coerce_type
from .field import Field
from .utilities import MISSING, _set_new_attribute, _create_fn


def process_class(cls):
    """
    Main DataRecord Handling Class.

    Adds __init__, __repr__, __setattr__, __delattr__, replace, extract and __doc__ to decorated class
    """
    _ensure_annotations(cls)
    fields = Field.list_for_class(cls)
    _ensure_defaulted_order(fields)
    _set_new_attribute(cls, '_record_fields', fields)
    _set_new_attribute(cls, '__init__', _init_fn(fields))
    _set_new_attribute(cls, '__repr__', _repr_fn(fields))
    set_fn, del_fn = _frozen_get_del_attr(cls, fields)
    _set_new_attribute(cls, '__setattr__', set_fn)
    _set_new_attribute(cls, '__delattr__', del_fn)
    _set_new_attribute(cls, 'replace', _replace_fn())
    _set_new_attribute(cls, 'extract', _extract_fn())
    _set_new_attribute(cls, 'from_dict', _from_dict_fn())
    _set_new_attribute(cls, 'from_iter', _from_iter_fn())
    _set_new_attribute(cls, '__slots__', [field.name for field in fields])
    _set_new_attribute(cls, '__hash__', _hash_fn(fields))
    _set_new_attribute(cls, '__eq__', _equal_fn())
    if not getattr(cls, '__doc__'):
        cls.__doc__ = f"{cls.__name__}{str(inspect.signature(cls)).replace(' -> None', '')}"
    return cls


def _from_dict_fn() -> classmethod:
    """Add class method to create class from dict"""
    return classmethod(_create_fn(
        'from_dict',
        ['cls', 'from_dict'],
        ['return cls(**from_dict)'],
    ))


def _from_iter_fn() -> classmethod:
    """Add class method to create class from iterable"""
    return classmethod(_create_fn(
        'from_iter',
        ['cls', 'from_iter'],
        ['return cls(*from_iter)'],
    ))


def _equal_fn() -> Callable:
    """Compare this hash to others hash"""
    return _create_fn(
        '__eq__',
        ['self', 'other'],
        [
            'if other.__class__ is self.__class__:',
            ' return other.__hash__() == self.__hash__()',
            'return NotImplemented'
        ],
        return_type=bool
    )


def _hash_fn(fields: List[Field]) -> Callable:
    data_tuple = '(' + ''.join(f'str(self.{field.name}), ' for field in fields) + ')'
    return _create_fn(
        '__hash__',
        ['self'],
        [f"return hash({data_tuple})"]
    )


def _ensure_annotations(cls) -> None:
    """
    Make sure that all of the fields on a class are annotated
    """

    def _not_dunder_or_callable(name_type: Tuple[str, Any]) -> bool:
        """Predicate to check that key value pairs in dict are not dunder or functions"""
        name, type_hint = name_type
        return not name.startswith('__') and not callable(type_hint)

    fields = filter(_not_dunder_or_callable, cls.__dict__.items())
    for key, _ in fields:
        if key not in cls.__dict__.get('__annotations__', {}):
            raise TypeError(f'{key!r} is a field with no type annotation')


def _ensure_defaulted_order(fields: List[Field]) -> None:
    """Ensure that defaulted arguments come after non defaulted ones"""
    seen_default = False
    for field in fields:
        if field.default is not MISSING:
            seen_default = True
        elif seen_default:
            raise TypeError(f'non-default argument {field.name!r} follows default argument')


def _replace_fn():
    """Generate the replace function for a data record"""
    return _create_fn(
        'replace',
        ['self', '**kwargs'],
        ['return self.__class__(**{**self.__dict__, **kwargs})']
    )


def _extract_fn():
    """Generate the extract function for a data record"""
    return _create_fn(
        'extract',
        ['self', '*args'],
        ['return tuple(getattr(self, arg) for arg in args)'],
        return_type=tuple
    )


def _init_field(self_name: str, _globals, field: Field) -> str:
    """Create string of assignment to be run inside the init function for a particular field"""
    default_name = f'_dflt_{field.name}'
    if field.default is not MISSING:
        _globals[default_name] = field.default
    return f"__builtins__.object.__setattr__({self_name},{field.name!r},coerce_type({field.name},__type_{field.name}))"


def _init_arg(field: Field) -> str:
    """Create argument string for a field for init"""
    default = '' if field.default is MISSING else f'=_dflt_{field.name}'
    return f"{field.name}:_type_{field.name}{default}"


def _init_fn(fields: List[Field]) -> Callable:
    """Generate the __init__ function for the data record."""
    _globals = {'MISSING': MISSING, 'coerce_type': coerce_type}
    _locals = {f'_type_{f.name}': f.type for f in fields}
    self_name = 'self' if 'self' not in fields else '__dataclass_self__'
    arg_strings = [self_name] + list(map(_init_arg, fields)) + [f"__type_{f.name}=_type_{f.name}" for f in fields] + [
        '**kwargs']
    body_lines = list(map(partial(_init_field, self_name, _globals), fields)) or ['pass']
    return _create_fn(
        '__init__',
        arg_strings,
        body_lines,
        _globals=_globals,
        _locals=_locals,
        return_type=None,
    )


def _repr_fn(fields: List[Field]) -> Callable:
    """Generate the __repr__ function for a data record"""
    props_str = ', '.join(f'{f.name}={{self.{f.name}!r}}' for f in fields)
    repr_func_str = 'return self.__class__.__qualname__ + f"(' + props_str + ')"'
    return _create_fn(
        '__repr__',
        ['self'],
        [repr_func_str],
        return_type=str,
    )


def _frozen_get_del_attr(cls, fields) -> Tuple[Callable, Callable]:
    """Generate both the __setattr__ and __delattr__ functions"""
    _globals = {
        'cls': cls,
        'CannotMutateRecordError': CannotMutateRecordError
    }
    fields_str = '(' + ''.join(f"{repr(f.name)}, " for f in fields) + ')'
    return (
        _create_fn(
            '__setattr__',
            ['self', 'name', 'value'],
            [
                f'if type(self) is cls or name in {fields_str}:',
                ' raise CannotMutateRecordError(f"cannot assign to field {name!r}")',
                'super(cls, self).__setattr__(name, value)',
            ],
            _globals=_globals,
        ),
        _create_fn(
            '__delattr__',
            ['self', 'name'],
            [
                f'if type(self) is cls or name in {fields_str}:',
                ' raise CannotMutateRecordError(f"cannot delete to field {name!r}")',
                'super(cls, self).__delattr__(name, value)',
            ],
            _globals=_globals,
        ),
    )
