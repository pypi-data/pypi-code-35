# -*- coding: utf-8 -*-

import difflib
import functools

import multipledispatch
import deepdiff
import pprintpp
import pytest


class Registry:
    def __init__(self, dispatcher=None):
        self.dispatcher = dispatcher or multipledispatch.Dispatcher("pytest_diff")

    def register(self, *types):
        if len(types) == 1:
            types = (types[0], types[0])
        return self.dispatcher.register(*types)


registry = Registry()


def _assertrepr_compare_equal_same_type(right, left):
    """Compare two objects of approximately the same type.

    The argument order is reversed so that `assert left == right` causes `right`
    to be the "new value".
    """
    return ["", repr(left), "==", repr(right), *registry.dispatcher(right, left)]


@functools.singledispatch
def to_diffable(obj):
    return obj


@registry.register(object, object)
def diff(right: object, left: object):
    return pprintpp.pformat(
        deepdiff.DeepDiff(to_diffable(left), to_diffable(right))
    ).splitlines()


@registry.register(str, str)
def diff(right, left):
    for line in difflib.ndiff(right.splitlines(), left.splitlines()):
        if line.startswith("?"):
            # Remove added newline character.
            yield line[:-1]
        else:
            yield line


def pytest_assertrepr_compare(op, left, right):
    """Use DeepDiff to display why left and right aren't equal."""

    if op != "==":
        return None

    return _assertrepr_compare_equal_same_type(left, right)


# TODO: Perhaps add functionality like this:
# @pytest.mark.diff(view="tree")
# def test_something():
#     a = {1: {2: 4}}
#     b = {1: {2: 4}}
#     assert a == b
