# Copyright (c) 2013, System Engineering Software Society
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the System Engineering Software Society nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.
# IN NO EVENT SHALL SYSTEM ENGINEERING SOFTWARE SOCIETY BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import inspect
import collections

import numpy as np


class LogicOperator(object):
    @staticmethod
    def nand(arr1, arr2):
        """
        Logical nand operator. Equivalent to np.logical_not(np.logical_and).
        """
        return np.logical_not(np.logical_and(arr1, arr2))

    @staticmethod
    def nor(arr1, arr2):
        """
        Logical nor operator. Equivalent to np.logical_not(np.logical_or).
        """
        return np.logical_not(np.logical_or(arr1, arr2))


class Statistics(object):
    @staticmethod
    def median(arr):
        """
        Median. Equivalent to np.ma.median except for the case where all values
        are masked. This function then returns NaN.
        """
        res = np.ma.median(arr)
        if res is np.ma.masked:
            res = np.float64('nan')
        return res


# TODO: docstrings and eval text should match better.
ARITHMETICS_OPS = [
    ("+ (plus)", "a + b", "Plus"),
    ("- (minus)", "a - b", "Minus"),
    ("* (times)", "a * b", "Multiplication"),
    ("** (power)", "a ** b", "Power."),
    ("/ (true division)", "a / b", "Division."),
    ("// (floor division)", "a // b", "floor division or integer division"),
    ("% (remainder)", "a % b", inspect.getdoc(np.mod)),
    ("divmod (floor division and remainder)", "divmod(a, b)",
     inspect.getdoc(divmod)),
]


# TODO: docstrings and eval text should match better.
COMPARATORS = [
    ("== (equal)", "a == b", inspect.getdoc(np.equal)),
    ("!= (not equal)", "a != b",
     inspect.getdoc(np.not_equal)),
    ("> (more than)", "a > b", inspect.getdoc(np.greater)),
    ("< (less than)", "a < b", inspect.getdoc(np.less)),
    (">= (more or equal)", "a >= b",
     inspect.getdoc(np.greater_equal)),
    ("<= (less or equal)", "a <= b",
     inspect.getdoc(np.less_equal)),
]


LOGIC_OPS = [
    ("not", "np.logical_not(a)",
     inspect.getdoc(np.logical_not)),
    ("and", "np.logical_and(a, b)",
     inspect.getdoc(np.logical_and)),
    ("or", "np.logical_or(a, b)",
     inspect.getdoc(np.logical_or)),
    ("all", "all(a)",
     inspect.getdoc(all)),
    ("any", "any(a)",
     inspect.getdoc(any)),
    ("xor", "np.logical_xor(a, b)",
     inspect.getdoc(np.logical_xor)),
    ("nand", "ca.nand(a, b)",
     inspect.getdoc(LogicOperator.nand)),
    ("nor", "ca.nor(a, b)",
     inspect.getdoc(LogicOperator.nor)),
]


# TODO: docstrings and eval text should match better.
BITWISE = [
    ("~ (not)", "~a", inspect.getdoc(np.bitwise_not)),
    ("& (and)", "a & b", inspect.getdoc(np.bitwise_and)),
    ("| (or)", "a | b", inspect.getdoc(np.bitwise_or)),
    ("^ (xor)", "a ^ b", inspect.getdoc(np.bitwise_xor)),
    ("<< (left shift)", "a << value", inspect.getdoc(np.left_shift)),
    (">> (right shift)", "a >> value",
     inspect.getdoc(np.right_shift)),
]


OPERATORS = collections.OrderedDict([
    ("Arithmetics", ARITHMETICS_OPS),
    ("Comparators", COMPARATORS),
    ("Logics", LOGIC_OPS),
    ("Bitwise", BITWISE),
])


STATISTICS = [
    ("Sum", "sum(a)", inspect.getdoc(sum)),
    ("Min", "min(a)", inspect.getdoc(min)),
    ("Max", "max(a)", inspect.getdoc(max)),
    ("Mean", "np.mean(a)", inspect.getdoc(np.mean)),
    ("Standard deviation", "np.std(a)", inspect.getdoc(np.std)),
    ("Median", "ca.median(a)", inspect.getdoc(np.ma.median)),
    ("Percentile", "np.percentile(a, value)",
     inspect.getdoc(np.percentile)),
]


GUI_DICT = collections.OrderedDict([
        ("Operators", OPERATORS),
        ("Statistics", STATISTICS),
    ])
