from functools import wraps
from typing import Any, Callable, Union

import regex

from ..utils import qualname


class String:
    """Alternative type for `str`, make it more `fluent` for nlp processing, the biggest benefits are `replace` and `apply`.

    `replace`: Support pattern replacement with `regex`, which is more powerful then builtin's `re` package
    `apply`: Define arbitrary function to process string

    Examples:
        >>> text = String('abcd')
        >>> text.replace(r'[ac]', lambda x: x.group(0).upper()).to_str()
        'AbCd'

        >>> text.upper().startswith('A')  # NOTE: return boolean
        True

        >>> text.apply(lambda x: 'A' * len(x)).to_str()
        'AAAA'
    """

    @property
    def value(self) -> str:
        return self._value

    def __init__(self, string):
        self._value = string

    def _wrap(self, func: Callable[[Any], str], *args, **kwargs) -> Callable:
        @wraps(func)
        def _inner(*args, **kwargs):
            return self.apply(func, *args, **kwargs)

        return _inner

    def __getattr__(self, name: str, *args, **kwargs):

        func = getattr(str, name, None)

        if callable(func):

            return self._wrap(func, *args, **kwargs)

        raise AttributeError(f"`String` object has no attribute `{name}`")

    def replace(self, pattern: str, repl: str, **kwargs) -> "String":
        """Relace the string by pattern match
        Return the string obtained by replacing the leftmost (or rightmost with a reverse pattern)
        non-overlapping occurrences of the `pattern` in string by the replacement `repl`

        Args:
            pattern (str): Pattern to match in the string, can be regular expression
            repl (str): Can be either a string or a callable; if a string,
                        backslash escapes in it are processed; if a callable,
                        it's passed the match object
                        and must return a replacement string to be used.
            **kwargs: Other keyword arguments fed into `regex.sub`

        Return:
            replaced string (String)

        References:
            regex: https://pypi.org/project/regex/
        """
        return self.__class__(regex.sub(pattern, repl, self._value, **kwargs))

    def apply(
        self, func: Callable, *args, allow_any: bool = True, **kwargs
    ) -> Union["String", Any]:
        """Apply arbitrary function to process string

        Args:
            func (Callable): function to apply
            allow_any (bool): If set to False, raise `TypeError` when the return value of the function is not a `str`

        Returns:
            processed string (String)

        """

        r = func(self._value, *args, **kwargs)

        if isinstance(r, str):
            return self.__class__(r)
        elif allow_any:
            return r
        else:
            raise TypeError(f"`{qualname(func)}` doesn't return `str`")

    def to_str(self) -> str:
        """Convert `String` back to `str`."""

        return self._value

    def __str__(self):

        return self.to_str()

    def __repr__(self):
        return f"<Str: {self._value}>"
