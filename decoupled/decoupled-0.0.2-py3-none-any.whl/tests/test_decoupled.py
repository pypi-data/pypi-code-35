# These are tests. Do we really need docstrings?
# pylint: disable=missing-docstring

# See https://github.com/PyCQA/pylint/issues/259#thread-subscription-status
# pylint: disable=no-value-for-parameter

import time
import multiprocessing
import os
from inspect import getfullargspec

import pytest

from decoupled import decoupled, ChildTimeoutError, ChildCrashedError


def test_func_is_run_with_correct_parameters():
    @decoupled()
    def func(positional_param, named_param):
        assert positional_param == 42
        assert named_param == 'foo'

    func(42, named_param='foo')


def test_normal_returns_work():
    @decoupled()
    def func():
        return 42

    assert func() == 42


def test_exceptions_are_passed_through():
    @decoupled()
    def func():
        raise ValueError()

    with pytest.raises(ValueError):
        func()


def test_timeout_causes_an_exception():
    @decoupled(timeout=1)
    def func():
        time.sleep(2)

    with pytest.raises(ChildTimeoutError):
        func()


def test_children_are_gone():
    @decoupled(timeout=1)
    def func():
        time.sleep(2)

    try:
        func()
    except ChildTimeoutError:
        pass

    time.sleep(.1)

    assert multiprocessing.active_children() == []


def test_crashing_causes_an_exception():
    @decoupled()
    def func():
        os._exit(1)  # pylint: disable=protected-access

    with pytest.raises(ChildCrashedError):
        func()


def test_decoreated_functions_keep_signatures():
    @decoupled()
    def func1(positional, named=42):  # pylint: disable=unused-argument
        pass

    def func2(positional, named=42):  # pylint: disable=unused-argument
        pass

    assert getfullargspec(func1) == getfullargspec(func2)
