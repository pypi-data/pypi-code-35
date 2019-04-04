## @file PbWS.py
# @brief Protobuf Web Signature
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


from   pbose.core import pb_object
from   pbose.core.PbWA import PbWSHeaderAlg
from   pbose.core.PbWK import PbWK
from   pbose.exceptions import AlreadySignedException
from   pbose.protobuf import PbWS_pb2


################################################################################
# PbWS
################################################################################


class PbWS(pb_object):


  __protobuf__ = PbWS_pb2.PbWS


  # @special_property('header', PbWSHeader, PbWS_pb2.PbWSHeader)


  @property
  def header(self):
    return PbWSHeader(self.protobuf.header)


  @header.setter
  def header(self, header):
    if isinstance(header, PbWSHeader):
      self.protobuf.header.CopyFrom(header.protobuf)
    elif isinstance(header, PbWS_pb2.PbWSHeader):
      self.protobuf.header.CopyFrom(header)
    else:
      raise TypeError("Not a valid PbWS header.")


  @property
  def protected(self):
    return PbWSHeader(self.protobuf.protected)


  @protected.setter
  def protected(self, protected):
    if isinstance(protected, PbWSHeader):
      self.protobuf.protected.CopyFrom(protected.protobuf)
    elif isinstance(protected, PbWS_pb2.PbWSHeader):
      self.protobuf.protected.CopyFrom(protected)
    else:
      raise TypeError("Not a valid PbWS protected header.")


  @property
  def signed(self):
    return self.signature != b''


  def sign(self, key):
    if self.signed:
      raise AlreadySignedException()
    signature = key.sign(data=self.protobuf.payload)
    self.signature = signature


  def verify(self, key):
    key.verify(data=self.protobuf.payload, signature=self.signature)


################################################################################
# PbWSHeader
################################################################################


class PbWSHeader(pb_object):


  __protobuf__ = PbWS_pb2.PbWSHeader


  @property
  def pbwk(self):
    return PbWK(self.protobuf.pbwk)


  @pbwk.setter
  def pbwk(self, pbwk):
    if isinstance(pbwk, PbWK):
      self.protobuf.pbwk.CopyFrom(pbwk.protobuf)
    elif isinstance(pbwk, PbWS_pb2.PbWK):
      self.protobuf.pbwk.CopyFrom(pbwk)
    else:
      raise TypeError("Not a valid PbWK.")
