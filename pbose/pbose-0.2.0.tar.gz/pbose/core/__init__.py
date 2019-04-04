## @file __init__.py
# @brief Init for pbose.core
#
# @copyright
# Copyright 2018 PbOSE <https://pbose.io>
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##


from abc import ABCMeta, abstractmethod, abstractproperty
import base64
from google.protobuf import json_format
from six import add_metaclass


@add_metaclass(ABCMeta)
class pb_object(object):


  @staticmethod
  @abstractmethod
  def __protobuf__():
    """ Set equal to the desired protobuf message. """


  @classmethod
  def init_protobuf_with_properties_before(cls, **properties):
    return properties


  @classmethod
  def init_protobuf_with_properties_after(cls, protobuf):
    return protobuf


  @classmethod
  def init_protobuf_with_properties(cls, **properties):
    properties = cls.init_protobuf_with_properties_before(**properties)
    protobuf = cls.__protobuf__(**properties)
    return cls.init_protobuf_with_properties_after(protobuf)


  def __init__(self, protobuf=None, **properties):
    if protobuf is not None:
      self.protobuf = protobuf
    else:
      self.protobuf = self.init_protobuf_with_properties(**properties)


  @property
  def protobuf(self):
    return self._protobuf


  @protobuf.setter
  def protobuf(self, protobuf):
    self._protobuf = protobuf


  def __getattr__(self, attr):
    if attr.startswith('_'):
      raise AttributeError("'pb_object' object has no attribute '{}'".format(attr))
    else:
      return getattr(self.protobuf, attr)


  def __setattr__(self, attr, value):
    try:
      return setattr(self._protobuf, attr, value)
    except Exception as e:
      return super(pb_object, self).__setattr__(attr, value)


  def __eq__(self, other):
    if isinstance(other, type(self)):
      return self.protobuf == other.protobuf
    else:
      return False


  def __str__(self):
    return str(self.protobuf)


  def __getstate__(self):
    return self.to_bytes()


  def __setstate__(self, state):
    self.protobuf = self.__protobuf__.FromString(state)


  def __copy__(self):
    return type(self).from_bytes(self.to_bytes())


  def __deepcopy__(self, memo):
    return type(self).from_bytes(self.to_bytes())


  ##############################################################################
  # Format
  ##############################################################################


  def to_bytes(self):
    return self.protobuf.SerializeToString()


  @classmethod
  def from_bytes(cls, bytes):
    protobuf = cls.__protobuf__.FromString(bytes)
    return cls(protobuf)


  def to_b64(self, urlsafe=False):
    if urlsafe:
      return base64.urlsafe_b64encode(self.to_bytes())
    else:
      return base64.standard_b64encode(self.to_bytes())


  @classmethod
  def from_b64(cls, b64, urlsafe=False):
    if urlsafe:
      return cls.from_bytes(base64.urlsafe_b64decode(b64))
    else:
      return cls.from_bytes(base64.standard_b64decode(b64))


  def to_json_after(self, json):
    return json


  def to_json(self):
    json = json_format.MessageToDict(self.protobuf, preserving_proto_field_name=True)
    return self.to_json_after(json)


  @classmethod
  def from_json_before(cls, json):
    return json


  @classmethod
  def from_json(cls, json):
    json = cls.from_json_before(json)
    protobuf = cls.__protobuf__()
    json_format.ParseDict(json, protobuf)
    return cls(protobuf)
