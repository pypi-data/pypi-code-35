"""Easier JSON navigation and exploration."""

import ast
import json
from pprint import pformat
from typing import Any, Dict, Iterator, List, Mapping, Optional, Sequence, Union


__all__ = ('EZJL', 'EZJD', 'as_traversable', 'traverse')

EZJsonValues = Optional[Union['EZJL', 'EZJD', str, float, int]]

DEFAULT_SEP = '.'
DEFAULT_MAP = '^'
DEFAULT_MAP_KEY = '__key'


def _slice_to_str(slice_: slice) -> str:
    """
    Stringify slice to resemble user input.

    :param slice_: Slice to stringify
    :return: String representation of slice
    """
    start = slice_.start if slice_.start is not None else ''
    stop = slice_.stop if slice_.stop is not None else ''
    step = f'{slice_.step}' if slice_.step is not None else ''

    return f'{start}:{stop}{step}'


def _str_to_slice(str_: str) -> slice:
    """
    Naive conversion of string to slice.

    :param str_: String representation of slice
    :return: Slice
    """
    return slice(*map(lambda s: int(s) if s else None, str_.split(':')))


def traverse(value, path, *,
             traversed: str = '',
             sep: str = DEFAULT_SEP,
             map_char: str = DEFAULT_MAP,
             dict_key_key: str = DEFAULT_MAP_KEY):
    """
    Traverse structure, returning the resulting value.

    :param value: Structure to traverse
    :param path: Path of traversal
    :param traversed: Path already traversed
    :param sep: Path separator
    :param map_char: Path mapping character
    :param dict_key_key: Key in path representing dictionary key
    :return: Value at path
    """
    # Empty path
    if path == '':
        return value

    # Non-string path
    if isinstance(path, (int, slice)):
        return value[path]

    if not isinstance(path, str):
        error_msg = f'Unsupported path {path!r} of type {type(path).__name__}'
        if isinstance(value, list):
            raise IndexError(error_msg)
        raise KeyError(error_msg)

    remaining = path.split(sep)
    while remaining:
        bit = remaining.pop(0)
        traversed = f'{traversed}{sep}{bit}'
        error_msg = f'Error traversing {path!r}, failed from {traversed!r} to {bit!r}: '  # noqa

        # Flag to map over return value
        map_ret = False

        # Handle list
        if isinstance(value, list):
            # Interpret index
            try:
                if bit.endswith(map_char):
                    map_ret = True
                    bit = bit[:-len(map_char)]
                if ':' in bit:
                    index = _str_to_slice(bit)
                else:
                    index = int(bit)
            except (ValueError, TypeError):
                raise IndexError(error_msg + 'bad sequence index')

            # Access index
            try:
                value = value[index]
            except IndexError:
                raise IndexError(error_msg + 'index does not exist')

        # Handle dict
        elif isinstance(value, dict):
            if bit == map_char:
                map_ret = True
                value_ = []
                for k, v in value.items():
                    v = v.copy()
                    v[dict_key_key] = v.get(dict_key_key, k)
                    value_.append(v)
                value = value_
            else:
                try:
                    value = value[bit]
                except KeyError:
                    raise KeyError(error_msg + 'no such key')

        # Handle mapping
        if map_ret:
            retval = []
            for n, val in enumerate(value):
                try:
                    traversed_val = traverse(val, sep.join(remaining),
                                             traversed=traversed,
                                             sep=sep,
                                             map_char=map_char,
                                             dict_key_key=dict_key_key)
                    if isinstance(traversed_val, _EZBase):
                        traversed_val = traversed_val._traversed
                    retval.append(traversed_val)
                except (KeyError, IndexError) as e:
                    raise IndexError(error_msg + f'failed on {n}') from e
            return retval

    return value


class _EZIter(Iterator[Any]):

    def __init__(self, underlying: '_EZBase'):
        self._underlying = underlying
        self._pos = 0
        self._iter = iter(underlying._traversed)

    def __next__(self) -> Any:
        if isinstance(self._underlying, EZJL):
            if self._pos >= len(self._underlying):
                raise StopIteration()
            value = self._underlying[str(self._pos)]
            self._pos += 1
            return value
        return next(self._iter)


class _EZBase:

    """Base container for traversable structures."""

    def __init__(self, root, *,
                 path: Union[int, slice, str] = '',
                 sep: str = DEFAULT_SEP,
                 map_char: str = DEFAULT_MAP,
                 dict_key_key: str = DEFAULT_MAP_KEY,
                 _traversed: Optional[Any] = None):
        """
        Create traversable container.

        :param root: Structure to traverse
        :param path: Path of traversal
        :param sep: Path separator
        :param map_char: Path mapping character
        :param dict_key_key: Key in path representing dictionary key
        :param _traversed: Pre-traversed value at the path
        """
        self._traversed = _traversed or traverse(root, path,
                                                 sep=sep,
                                                 map_char=map_char,
                                                 dict_key_key=dict_key_key)
        self._root = root
        if isinstance(path, int):
            self._path = str(path)
        elif isinstance(path, slice):
            self._path = _slice_to_str(path)
        elif isinstance(path, str):
            self._path = path
        else:
            raise ValueError("Path can only be int, slice or str")
        self._sep = sep
        self._map_char = map_char
        self._dict_key_key = dict_key_key

    @property
    def parent(self):
        """
        Parent or None if no parent exists.

        :return: Parent or None if no parent exists
        """
        if self._path == '':
            return None
        elif self._sep in self.path:
            parent_path = self.path.rsplit(sep=self._sep, maxsplit=1)[0]
        else:
            parent_path = ''
        return as_traversable(self._root,
                              path=parent_path,
                              sep=self._sep,
                              map_char=self._map_char,
                              dict_key_key=self._dict_key_key)

    @property
    def root(self):
        """
        Root of container.

        :return: Root of container
        """
        root = self
        while root.parent is not None:
            root = root.parent
        return root

    @property
    def path(self):
        """
        Current path of container.

        :return: Current path of container
        """
        return self._path

    @property
    def key(self):
        """
        Current key (last part of the path).

        :return: Current key (last part of the path)
        """
        return self._path.rsplit(self._sep)[-1]

    def __iter__(self) -> Iterator[Any]:
        return _EZIter(self)

    def __getitem__(self, path) -> EZJsonValues:
        value = traverse(self._traversed, path,
                         sep=self._sep,
                         map_char=self._map_char,
                         dict_key_key=self._dict_key_key)
        if not isinstance(value, (dict, list)):
            return value
        if self.path:
            new_path = f'{self.path}{self._sep}{path}'
        else:
            new_path = path
        return as_traversable(self._root,
                              path=new_path,
                              sep=self._sep,
                              map_char=self._map_char,
                              dict_key_key=self._dict_key_key,
                              _traversed=value)

    def get(self, path, default: EZJsonValues = None) -> EZJsonValues:
        """
        Exception-safe alternative of __getitem__ returning a default value.

        :param path: Path to traverse to
        :param default: Default value to return if path cannot be reached
        :return: Value at path or None if path cannot be reached
        """
        try:
            return self[path]
        except (IndexError, KeyError):
            return default

    def __len__(self) -> int:
        return len(self._traversed)

    def __repr__(self) -> str:
        name = type(self).__name__
        sep = '\n' + ' ' * (len(name) + 1)
        blob = sep.join(pformat(self._traversed, compact=True).splitlines())
        return (f'{name}({blob},'
                f'{sep}path={self._path!r},'
                f'{sep}sep={self._sep!r},'
                f'{sep}map_char={self._map_char!r},'
                f'{sep}dict_key_key={self._dict_key_key!r})')

    def __eq__(self, other) -> bool:
        return (isinstance(other, type(self)) and
                self._root == other._root and
                self._path == other._path and
                self._sep == other._sep and
                self._map_char == other._map_char and
                self._dict_key_key == other._dict_key_key)


class EZJL(_EZBase, Sequence[EZJsonValues]):

    """Sequence container for traversable structures."""


class EZJD(_EZBase, Mapping[str, EZJsonValues]):

    """Mapping container for traversable structures."""


def as_traversable(value: Union[str, Dict[str, Any], List[Any]], *,
                   path: str = '',
                   sep: str = DEFAULT_SEP,
                   map_char: str = DEFAULT_MAP,
                   dict_key_key: str = DEFAULT_MAP_KEY,
                   _traversed: Optional[Any] = None):
    """
    Traverse structure, returning the resulting value as EZJL or EZJD.

    :param value: Structure to traverse
    :param path: Path of traversal
    :param sep: Path separator
    :param map_char: Path mapping character
    :param dict_key_key: Key in path representing dictionary key
    :param _traversed: Pre-traversed value at the path
    :return: Value at path in EZJL or EZJD container
    """
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except ValueError:
            try:
                value = ast.literal_eval(value)
            except ValueError:
                raise ValueError('Could not interpret value as JSON or '
                                 'Python AST')
    if _traversed is None:
        _traversed = traverse(value, path,
                              sep=sep,
                              map_char=map_char,
                              dict_key_key=dict_key_key)
    if isinstance(_traversed, list):
        cls = EZJL
    elif isinstance(_traversed, dict):
        cls = EZJD
    else:
        raise ValueError(f'Bad type, unexpected {type(value).__name__}')
    return cls(value,
               path=path,
               sep=sep,
               map_char=map_char,
               dict_key_key=dict_key_key,
               _traversed=_traversed)
