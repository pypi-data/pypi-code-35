from copy import deepcopy
from itertools import islice
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple, TypeVar, Union

from .curry import curry

T = TypeVar('T')
S = TypeVar('S')
X = TypeVar('X')
Y = TypeVar('Y')


@curry
def tap(function: Callable[[T], None], value: T) -> T:
    """
    Pipeline Tap Function.

    Takes whatever value in the pipeline, passes it to a procedure, and returns the
    original value.

    Great for debugging or for side-effects.

    >>> tap(print)('test')
    test
    'test'
    >>> tap(print, 'test')
    test
    'test'
    >>> tap(lambda x: print(f"The value of the pipeline is {x}"))('test')
    The value of the pipeline is test
    'test'
    """
    function(deepcopy(value))
    return value


def _clean_key(key: str) -> Union[str, int]:
    return int(key) if key.isdigit() else key


def _key_to_keypath(key: Union[List[str], str]) -> List[Union[int, str]]:
    if "." in key:
        keypath = list(map(_clean_key, str(key).split('.')))
    elif isinstance(key, (tuple, list)):
        keypath = list(map(_clean_key, key))
    else:
        keypath = [key]
    return keypath


@curry
def lens(key: Union[List[str], str], target: Union[object, Dict[str, Any]]) -> Any:
    """
    Dig Deeper into a object or dict.

    Given a key, list of keys, or a `.` separated key path, return a function that
    pulls that value from a given data structure, or returns None.

    Examples:
    >>> lens('a')({'a': 'foo'})
    'foo'
    >>> lens('a.b')({'a':{'b':'bar'}})
    'bar'
    >>> lens(['a', 'b'])({'a':{'b':'bar'}})
    'bar'
    >>> lens('a.0')({'a':['foo', 'bar']})
    'foo'
    """
    keypath = _key_to_keypath(key)
    _data = deepcopy(target)
    while keypath and _data is not None:
        k = keypath.pop(0)
        if isinstance(k, int) and isinstance(_data, (list, tuple)):
            _data = index(k, _data)
        elif isinstance(_data, dict):
            _data = _data.get(str(k), None)
        else:
            _data = getattr(_data, str(k), None)
    return _data


def sort(key_func: Callable[[Any], bool], reverse: bool = False) -> Callable[[Iterable[T]], Iterable[T]]:
    """
    Partial Application Shortcut for the Sorted Function.
    The outer function takes the key function and reverse
    returning an inner function that applies it to a given iterable.

    Examples:

    >>> sort(lambda x: x)([3,1,2])
    [1, 2, 3]
    >>> sort(lambda x: x, reverse=True)([3,1,2])
    [3, 2, 1]
    """

    def _inner(values: Iterable) -> Iterable:
        return sorted(values, key=key_func, reverse=reverse)

    return _inner


@curry
def take(n: int, iterable: Iterable[T]) -> Iterable[T]:
    """
    Take the first n items from an iterable.

    Example:
    >>> list(take(2)([1,2,3,4,5]))
    [1, 2]
    >>> list(take(2, [1,2,3,4,5]))
    [1, 2]
    >>> list(take(2)(range(1,100)))
    [1, 2]
    """
    return islice(iterable, n)


def clone(value: T) -> Tuple[T, T]:
    """
    Takes a value and returns a tuple of two of it

    Example:
    >>> clone(1)
    (1, 1)
    >>> clone('foo')
    ('foo', 'foo')
    """
    return (value, value)


@curry
def index(i: int, seq: Sequence[T]) -> Optional[T]:
    """
    Get the index of a Sequence and return it or None

    >>> index(1)([1,2,3])
    2
    >>> index(1, [1,2,3])
    2
    >>> index(5)([1,2,3])
    """
    try:
        return seq[i]
    except IndexError:
        return None


@curry
def contains(needle: T, haystack: Iterable[T]) -> bool:
    """
    A contains predicate builder. Returns a function that checks for the existance
    in another set.

    >>> contains(1)([1,2,3])
    True
    >>> contains(0)([1,2,3])
    False
    >>> contains(1, [1,2,3])
    True
    """
    return needle in haystack


@curry
def join(glue: str, parts: Iterable[str]) -> str:
    """
    Wrapper around join.

    >>> join(',')(['1', '2', '3'])
    '1,2,3'
    >>> join('.', ['1', '2', '3'])
    '1,2,3'
    """
    return glue.join(parts)


def flatten(nested: Iterable[Iterable[T]]) -> Iterable[T]:
    """
    Flatten an iterable of iterables

    >>> list(flatten([[1,2,3], [4,5,6], [7,8,9]]))
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    return (t for iterable in nested for t in iterable)


def not_none(obj: Any) -> bool:
    """
    Shorthand for is not none

    >>> not_none('a')
    True
    >>> not_none(None)
    False
    """
    return obj is not None


def flatmap(func: Callable[[Iterable[T]], Iterable[S]], inputs: Iterable[Iterable[T]]) -> Iterable[S]:
    """
    Shortcut to map -> flatten

    >>> list(flatmap(lambda x: [x * 2], range(5)))
    [0, 2, 4, 6, 8]
    """
    return (t for iterable in map(func, inputs) for t in iterable)


def zipmap(funcs: Tuple[Callable[[T], S], Callable[[X], Y]], inputs: Iterable[Tuple[T, X]]) -> Iterable[Tuple[S, Y]]:
    """
    Given a pair of functions, and a series of tuples,
    zip the functions to the tuples and return a stream of the results.

    >>> list(zipmap((lambda x: x * 2, lambda x : x**2), enumerate(range(5))))
    [(0, 0), (2, 1), (4, 4), (6, 9), (8, 16)]
    """
    f, g = funcs
    return ((f(x), g(y)) for x, y in inputs)
