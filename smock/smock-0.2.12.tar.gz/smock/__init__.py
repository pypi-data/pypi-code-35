import json
import yaml
import logging


logger = logging.getLogger(__name__)

"""
SMock -- Serverboards Mock library -- Mock comfortably.

This library helps to mock function and method calls, getting the data
from an external yaml file.
"""


class MockWrapper:
    """
    Wraps all the data returned by the mocked function to behave like a
    dictionary, like an object, like a function... like almost everything you
    may need
    """

    def __init__(self, data):
        self.__data = data

    def __getattr__(self, key):
        if isinstance(self, dict):
            if key not in self.__data:
                raise AttributeError("'%s' not found" % key)
            return wrapped(self.__getitem__(key))
        if key == '_MockWrapper__data':
            raise AttributeError("_MockWrapper__data not found")
        return getattr(self.__data, key)

    def __call__(self):
        return self

    def __getitem__(self, key):
        return wrapped(self.__data[key])

    def __str__(self):
        return str(self.__data)

    def __repr__(self):
        return repr(self.__data)

    def __eq__(self, other):
        # A bit convoluted, but if both are MockWrappers, after two clls the real objects are just tested for eq.
        return other.__eq__(self.__data)

    def __le__(self, other):
        return other.__ge__(self.__data)

    def __lt__(self, other):
        return other.__gt__(self.__data)

    def __ge__(self, other):
        return other.__le__(self.__data)

    def __gt__(self, other):
        return other.__lt__(self.__data)

    def __len__(self):
        return len(self.__data)

    def __int__(self):
        return int(self.__data)

    def __float__(self):
        return float(self.__data)

    def __hash__(self):
        return self.__data.__hash__()

    def __not__(self):
        return not self.__data

    def __or__(self, other):
        if isinstance(other, MockWrapper):
            other = other.__data
        return self.__data or other

    def __and__(self, other):
        if isinstance(other, MockWrapper):
            other = other.__data
        return self.__data and other

    def __xor__(self, other):
        if isinstance(other, MockWrapper):
            other = other.__data
        return self.__data ^ other

    def __add__(self, other):
        if isinstance(other, MockWrapper):
            other = other.__data
        return self.__data + other

    def __sub__(self, other):
        if isinstance(other, MockWrapper):
            other = other.__data
        return self.__data - other

    def __mul__(self, other):
        if isinstance(other, MockWrapper):
            other = other.__data
        return self.__data * other

    def __truediv__(self, other):
        if isinstance(other, MockWrapper):
            other = other.__data
        return self.__data / other

    def __floordiv__(self, other):
        if isinstance(other, MockWrapper):
            other = other.__data
        return self.__data // other

    def __bool__(self):
        return bool(self.__data)

    def __neg__(self):
        return -self.__data

    # def keys(self):
    #     return self.__data.keys()
    #
    def get(self, key, defv=None):
        return wrapped(self.__data.get(key, defv))

    def to_json(self):
        return json.dumps(self.__data)


class MockWrapperList(MockWrapper, list):
    def __init__(self, data):
        MockWrapper.__init__(self, data)
        list.__init__(self, data)


class MockWrapperDict(MockWrapper, dict):
    def __init__(self, data):
        MockWrapper.__init__(self, data)
        dict.__init__(self, data)


def wrapped(data):
    if isinstance(data, MockWrapper):
        return data
    if isinstance(data, dict):
        return MockWrapperDict(data)
    if isinstance(data, list):
        return MockWrapperList(data)
    if isinstance(data, str) and data.startswith("file:"):
        with open(data[5:]) as fd:
            return fd.read()
    return MockWrapper(data)


def mock_match(A, B):
    """
    Checked for params on a mocked function is as expected

    It is necesary as sometimes we get a tuple and at the mock data we have
    lists.

    Examples:
    ```
    >>> mock_match("A", "A")
    True
    >>> mock_match("A", "B")
    False
    >>> mock_match(["A", "B", "C"], ["A", "B", "C"])
    True
    >>> mock_match(["A", "B", "C"], "*")
    True

    ```
    """
    if B == '*':  # always match
        return True
    if isinstance(A, (tuple, list)) and isinstance(B, (tuple, list)):
        return all(mock_match(a, b) for (a, b) in zip(A, B))
    if type(A) != type(B):
        return False
    if isinstance(A, dict):
        for k, v in A.items():
            if k not in B:
                return False
            if not mock_match(v, B[k]):
                return False
        return True
    return A == B


def mock_res(name, data, args=[], kwargs={}):
    """
    Given a name, data and call parameters, returns the mocked result

    If there is no matching result, raises an exception that can be used to
    prepare the mock data.

    This can be used for situations where you mock some function like data;
    for example at [Serverboards](https://serverboards.io), we use it to
    mock RPC calls.

    Its also used internally on every other mocking.
    """
    data = data.get(name)
    if not data:
        logger.error("unknown method for mocking: %s: { args: %s, kwargs: %s }" % (
            name, try_json_dump(args), try_json_dump(kwargs)
        ))
        raise Exception(
            "unknown method for mocking: %s: { args: %s, kwargs: %s }" % (
                name, try_json_dump(args), try_json_dump(kwargs)
            )
        )
    for res in data:
        if mock_match(args, res.get("args", [])) and mock_match(kwargs, res.get("kwargs", {})):
            if 'error' in res:
                logger.debug("Mock result error: %s" % res["error"])
                raise Exception(res["error"])

            if 'result:raw' in res:
                return res["result:raw"]

            result = res["result"]
            logger.debug("Mock result: %s" % res["result"])
            if isinstance(result, (int, str)):
                return result
            return wrapped(result)

    logger.error(
        "unknown data for mocking: %s: { args: %s, kwargs: %s }" % (
            name, try_json_dump(args), try_json_dump(kwargs)
        ))

    raise Exception(
        "unknown data for mocking: %s: { args: %s, kwargs: %s }" % (
            name, try_json_dump(args), try_json_dump(kwargs)
        )
    )


def mock_method(name, data, calls=None):
    """
    Returns a function that mocks an original function.

    If calls is a list, the call is appended.
    """
    def mockf(*args, **kwargs):
        logger.debug("Mock call %s(%s, %s)" % (name, args, kwargs))
        if calls is not None:
            calls.append({
                "name": name,
                "args": args,
                "kwargs": kwargs,
            })
        return mock_res(name, data, args, kwargs)
    return mockf


def mock_method_async(name, data, calls=None):
    """
    Returns an async function that mocks an original async function
    """
    async def mockf(*args, **kwargs):
        logger.debug("Mock async call %s(%s, %s)" % (name, args, kwargs))
        if calls is not None:
            calls.append({
                "name": name,
                "args": args,
                "kwargs": kwargs,
            })
        return mock_res(name, data, args, kwargs)
    return mockf


class SMock:
    """
    Encapsulates mocking calls so it's easier to load data and mock methods

    Example:

    ```python
    >>> import requests
    >>> smocked = SMock("tests/data.yaml")
    >>> requests.get = smocked.mock_method("requests.get")
    >>> res = requests.get("https://mocked.url")
    >>> res.status_code
    200
    >>> res.content
    'Gocha!'
    >>> res.json()
    {'text': 'Gocha too!'}

    ```

    The mock file is a yaml file with each mocked function as keys, and
    `args`/`kwargs` as calling args and kwargs, and `result` the result.

    Several mockfiles can be passed in, and they will add possible calls
    to be mocked.

    Check `tests/data.yaml` for an example at the source code.
    """

    def __init__(self, *mockfiles):
        self._data = {}

        # Can set several mockfiles, and they just previous list of methods
        for mockfile in mockfiles:
            self.load(mockfile)

        self.calls = []

    def load(self, mockfile):
        with open(mockfile) as fd:
            for k, v in yaml.safe_load(fd).items():
                d = self._data.get(k, [])
                v = d + v
                self._data[k] = v

    def mock_res(self, name, args=[], kwargs={}):
        """
        Calls `mock_res`

        Mock by args:
        ```
        >>> smock = SMock("tests/data.yaml")
        >>> res = smock.mock_res("requests.get", ["https://mocked.url"])
        >>> res.status_code
        200

        ```

        Using "*" as args, as fallback. As there is no kwargs, use default:
        ```
        >>> res = smock.mock_res("requests.get", ["https://error.mocked.url"])
        >>> res.status_code
        404

        ```

        Using "*" as kwargs:
        ```
        >>> res = smock.mock_res("requests.get",
        ...         ["https://mocked.url"],
        ...         {'data': 'data'})
        >>> res.status_code
        200
        >>> res.content
        'Mocked query'

        ```
        """
        return mock_res(name, self._data, args, kwargs)

    def mock_method(self, name):
        """
        Calls `mock_method`
        """
        return mock_method(name, self._data, self.calls)

    async def mock_method_async(self, name):
        """
        Calls `mock_method_async`
        """
        return await mock_method_async(name, self._data)


def try_json_dump(data):
    return json.dumps(data, default=lambda _: "*")


# monkey patch, to allow json encode of smock objects
default_json_encode = json.JSONEncoder.default


def json_encode_smock(_self, obj):
    if isinstance(obj, MockWrapper):
        return obj.to_json()
    return default_json_encode(obj)


json.JSONEncoder.default = json_encode_smock


if __name__ == '__main__':
    print("Testing smock...")
    import doctest
    import sys
    res = doctest.testmod()
    if not res.failed:
        print("Done:", res)
    else:
        print("Failed:", res)
    sys.exit(res.failed)
