# Copyright (c) 2016-2017, System Engineering Software Society
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
import os
import six
import sys
import json
import collections


_fs_encoding = sys.getfilesystemencoding()
fs_encoding = _fs_encoding


def _fs_decode_list(list_):
    return [x.decode(_fs_encoding) for x in list_]


def _fs_encode_list(list_):
    return [x.encode(_fs_encoding) for x in list_]


def environ_wrapper(environ=os.environ):
    return environ


OS = os
SYS = sys


def py_file(file_):
    if isinstance(file_, six.binary_type):
        file_ = file_.decode(_fs_encoding)
    return os.path.abspath(file_)


def py_file_dir(file_):
    return os.path.dirname(py_file(file_))


def encode(string, encoding):
    if isinstance(string, six.binary_type):
        return string
    return string.encode(encoding)


def decode(string, encoding):
    if isinstance(string, six.text_type):
        return string
    return string.decode(encoding)


def fs_encode(string):
    return encode(string, _fs_encoding)


def fs_decode(string):
    return decode(string, _fs_encoding)


def str_(string, encoding='ascii', errors='strict'):
    if isinstance(string, str):
        return string
    return string.decode(encoding, errors)


_dict = {}
_odict = collections.OrderedDict()
_dict_iters = set(type(x) for x in [
    _dict.keys(), _dict.values(), _dict.items(),
    _odict.keys(), _odict.values(), _odict.items()])


def dict_encoder(obj):
    if type(obj) in _dict_iters:
        return list(obj)
    return obj


def json_dumps(*args, **kwargs):
    return json.dumps(*args, default=dict_encoder, **kwargs)


def samefile(filename1, filename2):
    return os.path.samefile(filename1, filename2)


def deepcopy(obj):
    return json.loads(json_dumps(obj), object_hook=collections.OrderedDict)


if six.PY3 and sys.version_info.minor < 6:
    OrderedDict = collections.OrderedDict
else:
    # Python3.6 and forward should have ordered dict.
    OrderedDict = dict
