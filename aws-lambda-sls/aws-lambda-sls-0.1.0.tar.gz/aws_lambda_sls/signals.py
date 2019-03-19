# coding:utf-8
"""
signal define.
"""
from blinker import Namespace


_signals = Namespace()

lambda_invoke_exception = _signals.signal("lambda_invoke_exception")
