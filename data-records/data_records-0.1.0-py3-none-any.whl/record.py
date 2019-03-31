"""
Data Record Module.
"""
import builtins
import inspect
from functools import partial
from typing import List, Any, Callable, Tuple

from .coerce_types import coerce_type


class CannotMutateRecordError(AttributeError):
    """Error message thrown when editing or deleting fields on a data record"""
    pass


class _MissingType:
    """Reference Type for when defaults are missing"""
    pass


MISSING = _MissingType()


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


def datarecord(_cls=None):
    """
    Wrapper class to handle the decorator being called with or without parens
    """

    def wrap(cls):
        return _process_class(cls)

    if _cls is None:
        return wrap
    return wrap(_cls)


def _process_class(cls):
    """
    Main DataRecord Handling Class.

    Adds __init__, __repr__, __setattr__, __delattr__, replace, extract and __doc__ to decorated class
    """
    fields = Field.list_for_class(cls)
    _set_new_attribute(cls, '__init__', _init_fn(fields))
    _set_new_attribute(cls, '__repr__', _repr_fn(fields))
    set_fn, del_fn = _frozen_get_del_attr(cls, fields)
    _set_new_attribute(cls, '__setattr__', set_fn)
    _set_new_attribute(cls, '__delattr__', del_fn)
    _set_new_attribute(cls, 'replace', _replace_fn())
    _set_new_attribute(cls, 'extract', _extract_fn())
    _set_new_attribute(cls, '__slots__', [field.name for field in fields])
    if not getattr(cls, '__doc__'):
        cls.__doc__ = f"{cls.__name__}{str(inspect.signature(cls)).replace(' -> None', '')}"
    return cls


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
        ['return tuple(getattr(self, arg) for arg in args)']
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
        [repr_func_str]
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
            ['self', 'name', 'value'],
            [
                f'if type(self) is cls or name in {fields_str}:',
                ' raise CannotMutateRecordError(f"cannot delete to field {name!r}")',
                'super(cls, self).__delattr__(name, value)',
            ],
            _globals=_globals,
        ),
    )


def _create_fn(name: str, args: List[str], body: List[str], *, _globals=None, _locals=None, return_type: Any = MISSING):
    """Create a function with a given scope using exec"""
    _globals = _globals if _globals is not None else {}
    _locals = _locals if _locals is not None else {}
    _globals.setdefault('__builtins__', builtins)
    return_annotation = ''
    if return_type is not MISSING:
        _locals['_return_type'] = return_type
        return_annotation = '->_return_type'
    arg_str: str = ', '.join(args)
    body_str: str = '\n'.join(f' {b}' for b in body)
    function_definition = f'def {name}({arg_str}){return_annotation}:\n{body_str}'
    exec(function_definition, _globals, _locals)  # noqa
    return _locals[name]


def _set_new_attribute(cls, name, value):
    """
    Never overwrites an existing attribute.  Returns True if the
    attribute already exists.
    """
    if name in cls.__dict__:
        return True
    setattr(cls, name, value)
    return False
