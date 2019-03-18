# ------- #
# Imports #
# ------- #

from types import SimpleNamespace
from .makeGenericCallFn import makeGenericCallFn
from .getTypedResult import getTypedResult
from ..decorators.argIsCallable import argIsCallable


# ---- #
# Main #
# ---- #


@argIsCallable
def map_(mapperFn):
    fnName = map_.__name__
    callMapperFn = makeGenericCallFn(mapperFn, 3, fnName)

    def map_inner(collection):
        typedMap = getTypedResult(collection, typeToMap, fnName)
        return typedMap(callMapperFn, collection)

    return map_inner


# ------- #
# Helpers #
# ------- #


def map_list(callMapperFn, aList):
    result = []
    for idx, el in enumerate(aList):
        result.append(callMapperFn(el, idx, aList))

    return result


def map_simpleNamespace(callMapperFn, aSimpleNamespace):
    result = SimpleNamespace()
    for key, val in aSimpleNamespace.__dict__.items():
        setattr(result, key, callMapperFn(val, key, aSimpleNamespace))

    return result


typeToMap = {list: map_list, SimpleNamespace: map_simpleNamespace}
