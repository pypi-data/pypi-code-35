## @file instancing.py
# @brief I4T Instancing Token
#
# @copyright
# Copyright 2018 I4T <https://i4t.io>
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


import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

from i4t.protobuf import Firmware_pb2
from i4t.protobuf.common_pb2 import HashType
from i4t.protobuf.Firmware_pb2 import FirmwareFileType

from pbose.core import pb_object
from pbose.core.PbWT import PbWT


class FirmwareToken(PbWT):


  TOKEN_TYPE = 'x.i4t.ft'


  @property
  def payload(self):
    return FirmwareTokenClaims.from_bytes(self.protobuf.payload)


  @payload.setter
  def payload(self, payload):
    if isinstance(payload, Firmware_pb2.FirmwareTokenClaims):
      payload = FirmwareTokenClaims(payload)
    if isinstance(payload, FirmwareTokenClaims):
      self.protobuf.payload = payload.to_bytes()
    else:
      raise TypeError("Not a valid FirmwareToken payload.")


class FirmwareTokenClaims(pb_object):


  __protobuf__ = Firmware_pb2.FirmwareTokenClaims


  __file_type_map__ = { # TODO
    FirmwareFileType.TAR_GZ: "tar.gz",
  }


  @classmethod
  def from_file(cls, version, file_path, inline_binary=False):
    if not os.path.isfile(file_path):
      raise ValueError("{} is not a file".format(file_path))
    with open(file_path, 'rb') as fp:
      if inline_binary:
        raise NotImplementedError()
      else:
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend()) # TODO
        chunksize = 1024
        chunk = fp.read(chunksize)
        while chunk:
          digest.update(chunk)
          chunk = fp.read(chunksize)
        file_hash = digest.finalize()
    properties = dict(
      version=version,
      size=os.path.getsize(file_path),
      file_name=os.path.basename(file_path),
      file_type=FirmwareFileType.TAR_GZ, # TODO
      file_hash=file_hash,
      file_hash_type=HashType.SHA256, # TODO
    )
    print(properties)
    return cls(**properties)
