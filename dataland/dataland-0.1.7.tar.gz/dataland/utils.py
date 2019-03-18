import abc
import os
import time
from collections import OrderedDict
from functools import wraps
from typing import Any, Callable, Dict


def qualname(obj, default: str = "<unknown>", level: int = 1) -> str:
    module = getattr(obj, "__module__", default)
    name = getattr(obj, "__qualname__", default)
    joined = ".".join([nm for nm in [module, name] if nm])

    return ".".join(joined.split(".")[-level:])


def deprecated(cls_or_fn=None, replaced_by=None):
    """A Wrapper to mark any implementations(classes or functions) as deprecated

    Args:
        cls_or_fn (object): class or function to wrap
        replaced_by (Union[str, object]): replacement object, pass the object itself or its name in string

    Examples:

    >>> def new_foo():
            pass

    >>> @deprecated(replaced_by=new_foo):
        def old_foo():
            pass

    >>> old_foo()  # will print the warning message: [WARNING] `old_foo` is deprecated, and will be replaced by: `new_foo`

    Return:
        the wrapped object (object)
    """

    def wrapper(_callable):
        @wraps(_callable)
        def inner(*args, **kwargs):
            replaced = (
                replaced_by
                if isinstance(replaced_by, str)
                else qualname(replaced_by, "")
            )
            replacement = f", and will be replaced by: `{replaced}`" if replaced else ""

            print(f"\n[WARNING] `{qualname(_callable)}` is deprecated{replacement}\n")

            return _callable(*args, **kwargs)

        return inner

    if cls_or_fn:
        return wrapper(cls_or_fn)

    else:
        return wrapper


class SimpleTemplate:

    __slots__ = ("_template", "_default_params")

    @classmethod
    def join_from(
        cls,
        other: "SimpleTemplate",
        template: str,
        sep: str = os.path.sep,
        **defaut_params: str,
    ) -> "SimpleTemplate":

        return cls(
            sep.join([other.template, template]),
            **dict(**other.default_params, **defaut_params),
        )

    def __init__(self, template: str, **default_params):

        self._template = template
        self._default_params = default_params

    @property
    def template(self) -> str:
        return self._template

    @property
    def default_params(self) -> Dict:
        return self._default_params

    def __call__(self, **params: str):
        populates = {k: params.get(k, v) for k, v in self.default_params.items()}
        return self.template.format(**populates)

    def to_str(self) -> str:
        return str(self)

    def __str__(self):
        return self.template.format(**self.default_params)

    def __repr__(self):
        return f"<ST: {str(self)}>"


def _rgetattr(root_obj: Any, attr_name: str, allow_none: bool = True):
    """Get the attribute from a nested object structure"""
    if root_obj is None:
        return

    if not (isinstance(attr_name, str) and len(attr_name) > 0):
        raise ValueError(f"Invalid attribute name, got: {attr_name}")

    dot: int = attr_name.find(".")

    if dot < 0:
        return (
            getattr(root_obj, attr_name, None)
            if allow_none
            else getattr(root_obj, attr_name)
        )

    elif dot == 0 or (dot == len(attr_name) - 1):
        raise ValueError(
            f"Invalid attribute name, can't start/end with dot(.), got: {attr_name}"
        )

    else:
        parent_name = attr_name[:dot]
        child_name = attr_name[dot + 1 :]  # noqa: E203

        sub_obj = (
            getattr(root_obj, parent_name, None)
            if allow_none
            else getattr(root_obj, parent_name)
        )

        return _rgetattr(sub_obj, child_name, allow_none)


def _rsetattr(root_obj: Any, attr_name: str, value: Any):

    # TODO

    return root_obj


