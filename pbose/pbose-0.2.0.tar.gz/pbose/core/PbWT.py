## @file PbWT.py
# @brief Protobuf Web Token
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
from   pbose.core.PbWS import PbWS
from   pbose.protobuf import PbWT_pb2


class PbWT(PbWS):


  @property
  def payload(self):
    return PbWTClaims.from_bytes(self.protobuf.payload)


  @payload.setter
  def payload(self, payload):
    if isinstance(payload, PbWS_pb2.PbWTClaims):
      payload = PbWTClaims(payload)
    if isinstance(payload, PbWTClaims):
      self.protobuf.payload = payload.to_bytes()
    else:
      raise TypeError("Not a valid PbWT payload.")


class PbWTClaims(pb_object):


  __protobuf__ = PbWT_pb2.PbWTClaims
