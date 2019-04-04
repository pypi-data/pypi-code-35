## @file test_pbwk.py
# @brief Tests for PbWK
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


from   cryptography.exceptions import InvalidSignature
from   cryptography.hazmat.primitives.asymmetric import ec, rsa
from   pbose.core.PbWA import PbWKType
from   pbose.core.PbWK import PbWK, PbWKSet
import pytest
import os
import six
from   tests.fixtures.pbwk import keys, keys_ec, keys_rsa, keys_oct, keys_sign, keys_encrypt, keys_wrapkey


################################################################################
# PbWK
################################################################################


@pytest.mark.parametrize('key', keys, indirect=True)
def test_generate_for_alg(key):
  assert isinstance(key, PbWK)


def test_generate_for_alg_error(mocker):
  with pytest.raises(AssertionError):
    PbWK.generate_for_alg(alg=None)
  mocker.patch.dict("pbose.core.PbWK.PbWK.__alg_map__", dict(none=dict(kty=None)))
  with pytest.raises(TypeError):
    PbWK.generate_for_alg(alg='none')


def test_from_key_error():
  with pytest.raises(TypeError):
    PbWK.from_key(key=None)


def test_extract_key_error(mocker):
  with pytest.raises(TypeError):
    PbWK().extract_key()
  mocker.patch("pbose.core.PbWK.PbWK.extract_key")
  with pytest.raises(TypeError):
    PbWK().extract_private_key()
  with pytest.raises(TypeError):
    PbWK().extract_public_key()


@pytest.mark.parametrize('key', keys, indirect=True)
def test_pbwk_jwk(key):
  key_from_pbwk = PbWK.from_bytes(key.to_bytes())
  assert key == key_from_pbwk
  key_from_jwk = PbWK.from_json(key_from_pbwk.to_json())
  assert key == key_from_jwk


@pytest.mark.parametrize('key', keys_ec, indirect=True)
def test_generate_ec_private_key(key):
  private_key = key.extract_private_key()
  assert isinstance(private_key, ec.EllipticCurvePrivateKey)
  public_key = key.extract_public_key()
  assert isinstance(public_key, ec.EllipticCurvePublicKey)
  public_key = PbWK.from_key(public_key).extract_public_key()
  assert isinstance(public_key, ec.EllipticCurvePublicKey)


def test_generate_ec_private_key_error():
  with pytest.raises(TypeError):
    PbWK.generate_ec_private_key(crv=None)


def test_from_ec_key_error(mocker):
  with pytest.raises(TypeError):
    PbWK.from_ec_key(key=None)
  with pytest.raises(TypeError):
    key = mocker.Mock(spec=ec.EllipticCurvePrivateKey)
    key.curve = None
    key.private_numbers = mocker.Mock(spec=ec.EllipticCurvePrivateNumbers)
    PbWK.from_ec_key(key=key)


@pytest.mark.parametrize('key', keys_rsa, indirect=True)
def test_generate_rsa_private_key(key):
  private_key = key.extract_private_key()
  assert isinstance(private_key, rsa.RSAPrivateKey)
  public_key = key.extract_public_key()
  assert isinstance(public_key, rsa.RSAPublicKey)
  public_key = PbWK.from_key(public_key).extract_public_key()
  assert isinstance(public_key, rsa.RSAPublicKey)
  assert key.to_json()['e'] == 'AQAB'


def test_from_rsa_key_error(mocker):
  with pytest.raises(TypeError):
    PbWK.from_rsa_key(key=None)


@pytest.mark.parametrize('key', keys_oct, indirect=True)
def test_generate_oct_private_key(key):
  private_key = key.extract_private_key()
  assert isinstance(private_key, six.binary_type)


def test_from_oct_key_error(mocker):
  with pytest.raises(TypeError):
    PbWK.from_oct_key(key=None)


@pytest.mark.parametrize('key', keys, indirect=True)
def test_decrypt(key):
  with pytest.raises(NotImplementedError):
    key.decrypt(ciphertext=None)


@pytest.mark.parametrize('key', keys, indirect=True)
def test_encrypt(key):
  with pytest.raises(NotImplementedError):
    key.encrypt(plaintext=None)


@pytest.mark.parametrize('key', keys, indirect=True)
def test_exchange(key):
  with pytest.raises(NotImplementedError):
    key.exchange(peer_public_key=None, algorithm=None)


@pytest.mark.parametrize('key', keys_sign, indirect=True)
def test_sign_and_verify(key):
  data = os.urandom(64)
  signature = key.sign(data)
  key.verify(data, signature)


@pytest.mark.parametrize('key', keys_sign, indirect=True)
def test_verify_invalid(key):
  data = os.urandom(64)
  signature = os.urandom(64)
  with pytest.raises(InvalidSignature):
    key.verify(data, signature)


def test_sign_error(mocker):
  mocker.patch("pbose.core.PbWK.PbWK.extract_private_key")
  with pytest.raises(TypeError):
    PbWK().sign(b'')


def test_verify_error(mocker):
  mocker.patch("pbose.core.PbWK.PbWK.extract_public_key")
  with pytest.raises(TypeError):
    PbWK().verify(b'', b'')


################################################################################
# PbWKSet
################################################################################


def test_keyset(keyset):
  keys = list()
  for key in keyset:
    assert(isinstance(key, PbWK))
    keys.append(key)
  keyset_b = PbWKSet()
  keyset_b.extend(keys)
  assert(keyset_b == keyset)
  for i, key in enumerate(keyset):
    assert(keyset_b[i] == key)


def test_pbwkset_jwkset(keyset):
  keyset_from_pbwkset = PbWKSet.from_bytes(keyset.to_bytes())
  assert(keyset == keyset_from_pbwkset)
  keyset_from_jwkset = PbWKSet.from_json(keyset_from_pbwkset.to_json())
  assert(keyset == keyset_from_jwkset)
