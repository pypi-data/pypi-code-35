# -*- coding: utf-8 -*-

import difflib
import functools

import multipledispatch
import deepdiff
import pprintpp
import pytest


class Dispatcher:
    def __init__(self, namespace=None):
        self.namespace = {}

    def dispatch(self, function):
        return multipledispatch.dispatch(namespace=self.namespace)(function)


dispatcher = Dispatcher()


def _assertrepr_compare_equal_same_type(right, left):
    """Compare two objects of approximately the same type.

    The argument order is reversed so that `assert left == right` causes `right`
    to be the "new value".
    """
    return ["", repr(left), "==", repr(right), *diff(right, left)]


@functools.singledispatch
def to_diffable(obj):
    return obj


@dispatcher.dispatch
def diff(right: object, left: object):
    return pprintpp.pformat(
        deepdiff.DeepDiff(to_diffable(left), to_diffable(right))
    ).splitlines()


@dispatcher.dispatch
def diff(right: str, left: str):
    for line in difflib.ndiff(right.splitlines(), left.splitlines()):
        if line.startswith('?'):
            # Remove added newline character.
            yield line[:-1]
        else:
            yield line


def pytest_assertrepr_compare(op, left, right):
    """Use DeepDiff to display why left and right aren't equal."""

    if op != "==":
        return None
    if isinstance(left, type(right)) or isinstance(right, type(left)):
        return _assertrepr_compare_equal_same_type(left, right)
    return None


# TODO: Perhaps add functionality like this:
# @pytest.mark.diff(view="tree")
# def test_something():
#     a = {1: {2: 4}}
#     b = {1: {2: 4}}
#     assert a == b
