## @file conftest.py
# @brief Configuration for tests
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


import json
from   pbose.core.PbWA import PbWKAlg
from   pbose.core.PbWK import PbWK, PbWKSet, PbWKType, PbWKUse, PbWKKeyOps
import pytest
import six


################################################################################
# Algorithm Keys
################################################################################


def properties_for_alg(alg):
  alg_str = six.viewkeys(PbWKAlg.Enum)[alg]
  return dict(
    alg=alg,
    kid='test_' + alg_str,
    x5u='https://test_' + alg_str,
    x5c=[b'test'],
    x5t=b'test',
    x5t_s256=b'test',
  )


keys = [
  properties_for_alg(alg)
  for alg in PbWK.__alg_map__
]


keys_ec = [
  properties_for_alg(alg)
  for alg, alg_props in six.iteritems(PbWK.__alg_map__) if PbWKType.EC == alg_props['kty']
]


keys_rsa = [
  properties_for_alg(alg)
  for alg, alg_props in six.iteritems(PbWK.__alg_map__) if PbWKType.RSA == alg_props['kty']
]


keys_oct = [
  properties_for_alg(alg)
  for alg, alg_props in six.iteritems(PbWK.__alg_map__) if PbWKType.OCT == alg_props['kty']
]


keys_sign = [
  properties_for_alg(alg)
  for alg, alg_props in six.iteritems(PbWK.__alg_map__) if PbWKKeyOps.SIGN in alg_props['key_ops']
]


keys_encrypt = [
  properties_for_alg(alg)
  for alg, alg_props in six.iteritems(PbWK.__alg_map__) if PbWKKeyOps.ENCRYPT in alg_props['key_ops']
]


keys_wrapkey = [
  properties_for_alg(alg)
  for alg, alg_props in six.iteritems(PbWK.__alg_map__) if PbWKKeyOps.WRAPKEY in alg_props['key_ops']
]


@pytest.fixture
def key(request):
  properties = request.param
  return PbWK.generate_for_alg(**properties)


@pytest.fixture
def keyset():
  keyset = PbWKSet()
  for key_properties in keys:
    keyset.append(PbWK.generate_for_alg(**key_properties))
  return keyset
