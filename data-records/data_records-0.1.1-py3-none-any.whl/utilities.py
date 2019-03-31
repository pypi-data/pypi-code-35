"""
Utility functions not directly tied to any class or module.
"""
import builtins
from typing import List, Any


class _MissingType:
    """Reference Type for when defaults are missing"""
    pass


MISSING = _MissingType()


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
