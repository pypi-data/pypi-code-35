import itertools
import sys

IS_PYTHON_2 = sys.version[0] == '2'

if IS_PYTHON_2:
    string_types = (str, unicode)
    zip_ = itertools.izip

    # noqa: E303

    def escape_string(string):
        return string.encode("string_escape")

else:  # python3 and above
    string_types = (str,)
    zip_ = zip

    # noqa: E303

    def escape_string(string):
        # in python3, 'string_escape' has become 'unicode_escape', but bytes is returned then,
        # that's why additional backward decode is needed
        return string.encode("unicode_escape").decode("utf-8")


def pairwise(iterable):
    if not iterable:
        return iterable
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip_(a, b)
