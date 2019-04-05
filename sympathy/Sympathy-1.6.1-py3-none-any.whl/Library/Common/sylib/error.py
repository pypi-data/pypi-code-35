# -*- coding: utf-8 -*-
# Copyright (c) 2018, System Engineering Software Society
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
from __future__ import (print_function, division, unicode_literals,
                        absolute_import)
from collections import OrderedDict


class ErrorHandling(object):

    def fail(self, error):
        raise error

    @property
    def is_error(self):
        return False


_basic_error_options = OrderedDict([
    ('error', 'Error'),
    ('empty', 'Create Empty Item')])

_basic_list_error_options = OrderedDict([
    ('error', 'Error'),
    ('empty', 'Create Empty Item'),
    ('skip', 'Skip Item')])


_error_names = ['error', 'exception', 'fail']


class BasicErrorHandling(ErrorHandling):

    def __init__(self, options, key_or_index):
        self._options = options

        if self._options.get(key_or_index) is not None:
            self._key = key_or_index
        else:
            self._key = list(self._options.keys())[key_or_index]

    def keys(self):
        return self._options.keys()

    def descriptions(self):
        return self._options.values()

    @property
    def is_error(self):
        if self._key.lower() in _error_names:
            return True


class ErrorStrategy(object):
    def __init__(self, options, handling_factory):
        self._options = options
        self._handling = handling_factory

    def keys(self):
        return self._options.keys()

    @property
    def descriptions(self):
        return self._options.values()

    @property
    def options(self):
        return self._options

    def is_error(self, key_or_index):
        return self._handling(
            self._options, key_or_index).is_error


_strategies = {
    'basic': ErrorStrategy(
        _basic_error_options,
        BasicErrorHandling),
    'basic_list': ErrorStrategy(
        _basic_list_error_options,
        BasicErrorHandling)
}


def strategy(name):
    return _strategies[name]
