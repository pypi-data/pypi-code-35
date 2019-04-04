## @file test_pbws.py
# @brief Tests for PbWS
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


from   cryptography.hazmat.primitives.asymmetric import ec, rsa
from   pbose.core.PbWA import PbWKType
from   pbose.core.PbWK import PbWKUse
from   pbose.core.PbWS import PbWS, PbWSHeader
from   pbose.exceptions import AlreadySignedException
import pytest
import six
from   tests.fixtures.pbwk import keys, keys_ec, keys_rsa, keys_oct, keys_sign, keys_encrypt, keys_wrapkey


################################################################################
# PbWS
################################################################################


def test_init_empty():
  pbws = PbWS(
    protected=b'',
    header=b'',
    payload=b'',
    signature=b'',
  )


@pytest.mark.parametrize('key', keys_sign, indirect=True)
def test_sign_and_verify_payload(key):
  pbws = PbWS(
    protected=b'',
    header=b'',
    payload=b'',
  )
  pbws.sign(key)
  pbws.verify(key)
  with pytest.raises(AlreadySignedException):
    pbws.sign(key)


################################################################################
# PbWSHeader
################################################################################
