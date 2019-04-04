## @file PbWK.py
# @brief Protobuf Web Key
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


import os
from   bitstring import BitArray
from   cryptography.hazmat.backends import default_backend
from   cryptography.hazmat.primitives import hashes, hmac
from   cryptography.hazmat.primitives.asymmetric import ec, rsa, padding
import six
from   pbose.core import pb_object
from   pbose.core.PbWA import PbWKAlg, PbWKType, PbWKTypeECCurve
from   pbose.protobuf import PbWK_pb2
from   pbose.protobuf.PbWK_pb2 import PbWKUse, PbWKKeyOps


EC_CRV_MIN = PbWKTypeECCurve.P_256
RSA_KEY_SIZE_MIN = 2048
OCT_KEY_SIZE_MIN = 128


################################################################################
# PbWK
################################################################################


class PbWK(pb_object):


  __protobuf__ = PbWK_pb2.PbWK


  __alg_map__ = {
    PbWKAlg.HS256: dict(
      kty=PbWKType.OCT,
      key_size=256,
      use=PbWKUse.SIG,
      key_ops=[PbWKKeyOps.SIGN, PbWKKeyOps.VERIFY],
    ),
    PbWKAlg.HS384: dict(
      kty=PbWKType.OCT,
      key_size=384,
      use=PbWKUse.SIG,
      key_ops=[PbWKKeyOps.SIGN, PbWKKeyOps.VERIFY],
    ),
    PbWKAlg.HS512: dict(
      kty=PbWKType.OCT,
      key_size=512,
      use=PbWKUse.SIG,
      key_ops=[PbWKKeyOps.SIGN, PbWKKeyOps.VERIFY],
    ),
    PbWKAlg.RS256: dict(
      kty=PbWKType.RSA,
      use=PbWKUse.SIG,
      key_ops=[PbWKKeyOps.SIGN, PbWKKeyOps.VERIFY],
    ),
    PbWKAlg.RS384: dict(
      kty=PbWKType.RSA,
      use=PbWKUse.SIG,
      key_ops=[PbWKKeyOps.SIGN, PbWKKeyOps.VERIFY],
    ),
    PbWKAlg.RS512: dict(
      kty=PbWKType.RSA,
      use=PbWKUse.SIG,
      key_ops=[PbWKKeyOps.SIGN, PbWKKeyOps.VERIFY],
    ),
    PbWKAlg.ES256: dict(
      kty=PbWKType.EC,
      crv=PbWKTypeECCurve.P_256,
      use=PbWKUse.SIG,
      key_ops=[PbWKKeyOps.SIGN, PbWKKeyOps.VERIFY],
    ),
    PbWKAlg.ES384: dict(
      kty=PbWKType.EC,
      crv=PbWKTypeECCurve.P_384,
      use=PbWKUse.SIG,
      key_ops=[PbWKKeyOps.SIGN, PbWKKeyOps.VERIFY],
    ),
    PbWKAlg.ES512: dict(
      kty=PbWKType.EC,
      crv=PbWKTypeECCurve.P_521,
      use=PbWKUse.SIG,
      key_ops=[PbWKKeyOps.SIGN, PbWKKeyOps.VERIFY],
    ),
    PbWKAlg.PS256: dict(
      kty=PbWKType.RSA,
      use=PbWKUse.SIG,
      key_ops=[PbWKKeyOps.SIGN, PbWKKeyOps.VERIFY],
    ),
    PbWKAlg.PS384: dict(
      kty=PbWKType.RSA,
      use=PbWKUse.SIG,
      key_ops=[PbWKKeyOps.SIGN, PbWKKeyOps.VERIFY],
    ),
    PbWKAlg.PS512: dict(
      kty=PbWKType.RSA,
      use=PbWKUse.SIG,
      key_ops=[PbWKKeyOps.SIGN, PbWKKeyOps.VERIFY],
    ),
    PbWKAlg.RSA1_5: dict(
      kty=PbWKType.RSA,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.WRAPKEY, PbWKKeyOps.UNWRAPKEY],
    ),
    PbWKAlg.RSA_OAEP: dict(
      kty=PbWKType.RSA,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.WRAPKEY, PbWKKeyOps.UNWRAPKEY],
    ),
    PbWKAlg.RSA_OAEP_256: dict(
      kty=PbWKType.RSA,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.WRAPKEY, PbWKKeyOps.UNWRAPKEY],
    ),
    PbWKAlg.A128KW: dict(
      kty=PbWKType.OCT,
      key_size=128,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.WRAPKEY, PbWKKeyOps.UNWRAPKEY],
    ),
    PbWKAlg.A192KW: dict(
      kty=PbWKType.OCT,
      key_size=192,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.WRAPKEY, PbWKKeyOps.UNWRAPKEY],
    ),
    PbWKAlg.A256KW: dict(
      kty=PbWKType.OCT,
      key_size=256,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.WRAPKEY, PbWKKeyOps.UNWRAPKEY],
    ),
    PbWKAlg.DIR: dict(
      kty=PbWKType.OCT,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.ENCRYPT, PbWKKeyOps.DECRYPT],
    ),
    PbWKAlg.ECDH_ES: dict(
      kty=PbWKType.EC,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.ENCRYPT, PbWKKeyOps.DECRYPT],
    ),
    PbWKAlg.ECDH_ES_A128KW: dict(
      kty=PbWKType.EC,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.WRAPKEY, PbWKKeyOps.UNWRAPKEY],
    ),
    PbWKAlg.ECDH_ES_A192KW: dict(
      kty=PbWKType.EC,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.WRAPKEY, PbWKKeyOps.UNWRAPKEY],
    ),
    PbWKAlg.ECDH_ES_A256KW: dict(
      kty=PbWKType.EC,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.WRAPKEY, PbWKKeyOps.UNWRAPKEY],
    ),
    PbWKAlg.A128GCMKW: dict(
      kty=PbWKType.OCT,
      key_size=128,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.WRAPKEY, PbWKKeyOps.UNWRAPKEY],
    ),
    PbWKAlg.A192GCMKW: dict(
      kty=PbWKType.OCT,
      key_size=192,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.WRAPKEY, PbWKKeyOps.UNWRAPKEY],
    ),
    PbWKAlg.A256GCMKW: dict(
      kty=PbWKType.OCT,
      key_size=256,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.WRAPKEY, PbWKKeyOps.UNWRAPKEY],
    ),
    PbWKAlg.PBES2_HS256_A128KW: dict(
      kty=PbWKType.OCT,
      key_size=128,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.WRAPKEY, PbWKKeyOps.UNWRAPKEY],
    ),
    PbWKAlg.PBES2_HS384_A192KW: dict(
      kty=PbWKType.OCT,
      key_size=192,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.WRAPKEY, PbWKKeyOps.UNWRAPKEY],
    ),
    PbWKAlg.PBES2_HS512_A256KW: dict(
      kty=PbWKType.OCT,
      key_size=256,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.WRAPKEY, PbWKKeyOps.UNWRAPKEY],
    ),
    PbWKAlg.A128CBC_HS256: dict(
      kty=PbWKType.OCT,
      key_size=128,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.ENCRYPT, PbWKKeyOps.DECRYPT],
    ),
    PbWKAlg.A192CBC_HS384: dict(
      kty=PbWKType.OCT,
      key_size=192,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.ENCRYPT, PbWKKeyOps.DECRYPT],
    ),
    PbWKAlg.A256CBC_HS512: dict(
      kty=PbWKType.OCT,
      key_size=256,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.ENCRYPT, PbWKKeyOps.DECRYPT],
    ),
    PbWKAlg.A128GCM: dict(
      kty=PbWKType.OCT,
      key_size=128,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.ENCRYPT, PbWKKeyOps.DECRYPT],
    ),
    PbWKAlg.A192GCM: dict(
      kty=PbWKType.OCT,
      key_size=192,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.ENCRYPT, PbWKKeyOps.DECRYPT],
    ),
    PbWKAlg.A256GCM: dict(
      kty=PbWKType.OCT,
      key_size=256,
      use=PbWKUse.ENC,
      key_ops=[PbWKKeyOps.ENCRYPT, PbWKKeyOps.DECRYPT],
    ),
  }


  @staticmethod
  def _flatten_properties(properties):
    for prop in ['kty_prop_ec', 'kty_prop_rsa', 'kty_prop_oct']:
      kty_prop = properties.pop(prop, {})
      properties.update(kty_prop)
    return properties


  @staticmethod
  def _unflatten_properties(properties):
    kty_prop = {}
    for prop in list(properties.keys()):
      if prop in ['crv', 'x', 'y', 'd']:
        kty_prop[prop] = properties.pop(prop)
        if prop not in ['d']: # 'd' is shared by both EC and RSA
          properties['kty_prop_ec'] = kty_prop
      if prop in ['n', 'e', 'd', 'p', 'q', 'dp', 'dq', 'qi', 'oth']:
        if prop not in ['d']: # 'd' is shared by both EC and RSA
          kty_prop[prop] = properties.pop(prop) # 'd' was popped above in EC
          properties['kty_prop_rsa'] = kty_prop
      if prop in ['k']:
        kty_prop[prop] = properties.pop(prop)
        properties['kty_prop_oct'] = kty_prop
    return properties


  @classmethod
  def init_protobuf_with_properties_before(cls, **properties):
    return cls._unflatten_properties(properties)


  ##############################################################################
  # Format
  ##############################################################################


  def to_json_after(self, json):
    # flatten
    json = self._flatten_properties(json)
    # touch-ups
    if 'kty' in json:
      if 'OCT' in json['kty']:
        json['kty'] = json['kty'].lower()
    if 'crv' in json:
      json['crv'] = json['crv'].replace('_', '-')
    if 'use' in json:
      json['use'] = json['use'].lower()
    if 'key_ops' in json:
      json['key_ops'] = [key_op.lower().replace('key', 'Key').replace('bits', 'Bits') for key_op in json['key_ops']]
    if 'alg' in json:
      if json['alg'] in ['NONE', 'DIR']:
        json['alg'] = json['alg'].lower()
      count = (1, 1)
      if json['alg'] in ['RSA1_5']:
        count = (0, 0)
      if json['alg'] in ['RSA_OAEP_256']:
        count = (2, 0)
      json['alg'] = json['alg'].replace('_', '-', count[0]).replace('_', '+', count[1])
    if 'x5t_s256' in json:
      json['x5t#S256'] = json.pop('x5t_s256')
    return json


  @classmethod
  def from_json_before(cls, json):
    # touch-ups
    if 'kty' in json:
      json['kty'] = json['kty'].upper()
    if 'crv' in json:
      json['crv'] = json['crv'].replace('-', '_')
    if 'use' in json:
      json['use'] = json['use'].upper()
    if 'key_ops' in json:
      json['key_ops'] = [key_op.upper() for key_op in json['key_ops']]
    if 'alg' in json:
      json['alg'] = json['alg'].upper().replace('-', '_').replace('+', '_')
    if 'x5t#S256' in json:
      json['x5t_s256'] = json.pop('x5t#S256')
    # PbWK Type
    return cls._unflatten_properties(json)


  ##############################################################################
  # Cryptography
  ##############################################################################


  @classmethod
  def generate_for_alg(cls, **properties):
    assert 'alg' in properties
    assert properties['alg'] in cls.__alg_map__
    properties.update(cls.__alg_map__[properties['alg']])
    # key type
    if properties['kty'] == PbWKType.EC:
      if 'crv' not in properties:
        properties['crv'] = EC_CRV_MIN
      key = cls.generate_ec_private_key(**properties)
    elif properties['kty'] == PbWKType.RSA:
      if 'key_size' not in properties:
        properties['key_size'] = RSA_KEY_SIZE_MIN
      key = cls.generate_rsa_private_key(**properties)
    elif properties['kty'] == PbWKType.OCT:
      if 'key_size' not in properties:
        properties['key_size'] = OCT_KEY_SIZE_MIN
      key = cls.generate_oct_private_key(**properties)
    else:
      raise TypeError()
    return key


  def extract_key(self):
    if self.kty == PbWKType.EC:
      if self.kty_prop_ec.crv == PbWKTypeECCurve.P_256:
        key_size = 256
        x = BitArray(bytes=self.kty_prop_ec.x, length=key_size).uint
        y = BitArray(bytes=self.kty_prop_ec.y, length=key_size).uint
        public_numbers = ec.EllipticCurvePublicNumbers(x, y, ec.SECP256R1())
      elif self.kty_prop_ec.crv == PbWKTypeECCurve.P_384:
        key_size = 384
        x = BitArray(bytes=self.kty_prop_ec.x, length=key_size).uint
        y = BitArray(bytes=self.kty_prop_ec.y, length=key_size).uint
        public_numbers = ec.EllipticCurvePublicNumbers(x, y, ec.SECP384R1())
      elif self.kty_prop_ec.crv == PbWKTypeECCurve.P_521:
        key_size = 521
        x = BitArray(bytes=self.kty_prop_ec.x, length=key_size).uint
        y = BitArray(bytes=self.kty_prop_ec.y, length=key_size).uint
        public_numbers = ec.EllipticCurvePublicNumbers(x, y, ec.SECP521R1())
      # return private_key or public_key
      if self.kty_prop_ec.d:
        d = BitArray(bytes=self.kty_prop_ec.d, length=key_size).uint
        private_numbers = ec.EllipticCurvePrivateNumbers(d, public_numbers)
        key = private_numbers.private_key(default_backend())
      else:
        key = public_numbers.public_key(default_backend())
    elif self.kty == PbWKType.RSA:
      n = BitArray(bytes=self.kty_prop_rsa.n).uint
      e = BitArray(bytes=self.kty_prop_rsa.e).uint
      public_numbers = rsa.RSAPublicNumbers(e, n)
      # return private_key or public_key
      if self.kty_prop_rsa.d:
        d = BitArray(bytes=self.kty_prop_rsa.d).uint
        p = BitArray(bytes=self.kty_prop_rsa.p).uint
        q = BitArray(bytes=self.kty_prop_rsa.q).uint
        dmp1 = BitArray(bytes=self.kty_prop_rsa.dp).uint
        dmq1 = BitArray(bytes=self.kty_prop_rsa.dq).uint
        iqmp = BitArray(bytes=self.kty_prop_rsa.qi).uint
        private_numbers = rsa.RSAPrivateNumbers(p, q, d, dmp1, dmq1, iqmp, public_numbers)
        key = private_numbers.private_key(default_backend())
      else:
        key = public_numbers.public_key(default_backend())
    elif self.kty == PbWKType.OCT:
      key_size = len(self.kty_prop_oct.k)*8
      assert(key_size % 8 == 0)
      key = BitArray(bytes=self.kty_prop_oct.k, length=key_size).bytes
    else:
      raise TypeError()
    return key


  def extract_private_key(self):
    key = self.extract_key()
    if self.kty == PbWKType.EC:
      assert(isinstance(key, ec.EllipticCurvePrivateKey))
    elif self.kty == PbWKType.RSA:
      assert(isinstance(key, rsa.RSAPrivateKey))
    elif self.kty == PbWKType.OCT:
      assert(isinstance(key, six.binary_type))
    else:
      raise TypeError()
    return key


  def extract_public_key(self):
    key = self.extract_key()
    if self.kty == PbWKType.EC:
      if isinstance(key, ec.EllipticCurvePrivateKey):
        key = self.extract_private_key().public_key()
      assert(isinstance(key, ec.EllipticCurvePublicKey))
    elif self.kty == PbWKType.RSA:
      if isinstance(key, rsa.RSAPrivateKey):
        key = self.extract_private_key().public_key()
      assert(isinstance(key, rsa.RSAPublicKey))
    elif self.kty == PbWKType.OCT:
      # TODO decide if this make sense
      pass
    else:
      raise TypeError()
    return key


  @classmethod
  def from_key(cls, key, **properties):
    if isinstance(key, (ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey)):
      key = cls.from_ec_key(key, **properties)
    elif isinstance(key, (rsa.RSAPrivateKey, rsa.RSAPublicKey)):
      key = cls.from_rsa_key(key, **properties)
    elif isinstance(key, six.binary_type):
      key = cls.from_oct_key(key, **properties)
    else:
      raise TypeError()
    return key


  ##############################################################################
  # EC
  ##############################################################################


  @classmethod
  def generate_ec_private_key(cls, crv, **properties):
    if crv == PbWKTypeECCurve.P_256:
      curve = ec.SECP256R1()
    elif crv == PbWKTypeECCurve.P_384:
      curve = ec.SECP384R1()
    elif crv == PbWKTypeECCurve.P_521:
      curve = ec.SECP521R1()
    else:
      raise TypeError()
    key = ec.generate_private_key(curve, default_backend())
    return cls.from_key(key, **properties)


  @classmethod
  def from_ec_key(cls, key, **properties):
    # PbWK Type
    properties['kty'] = PbWKType.EC
    # PBWK Type Properties
    private_numbers = None
    if isinstance(key, ec.EllipticCurvePrivateKey):
      private_numbers = key.private_numbers()
      public_numbers = private_numbers.public_numbers
    elif isinstance(key, ec.EllipticCurvePublicKey):
      public_numbers = key.public_numbers()
    else:
      raise TypeError()
    # PBWK Type Properties Curve
    if isinstance(key.curve, ec.SECP256R1):
      properties['crv'] = PbWKTypeECCurve.P_256
    elif isinstance(key.curve, ec.SECP384R1):
      properties['crv'] = PbWKTypeECCurve.P_384
    elif isinstance(key.curve, ec.SECP521R1):
      properties['crv'] = PbWKTypeECCurve.P_521
    else:
      raise TypeError()
    # PbWK Type Properties
    properties['x'] = BitArray(uint=public_numbers.x, length=key.key_size).tobytes().lstrip(b'\x00')
    properties['y'] = BitArray(uint=public_numbers.y, length=key.key_size).tobytes().lstrip(b'\x00')
    properties['d'] = BitArray(uint=private_numbers.private_value, length=key.key_size).tobytes().lstrip(b'\x00') if private_numbers else b''
    # done
    return cls(**properties)


  ##############################################################################
  # RSA
  ##############################################################################


  @classmethod
  def generate_rsa_private_key(cls, key_size, public_exponent=65537, **properties):
    key = rsa.generate_private_key(public_exponent, key_size, default_backend())
    return cls.from_key(key, **properties)


  @classmethod
  def from_rsa_key(cls, key, **properties):
    # PbWK Type
    properties['kty'] = PbWKType.RSA
    # PBWK Type Properties
    private_numbers = None
    if isinstance(key, rsa.RSAPrivateKey):
      private_numbers = key.private_numbers()
      public_numbers = private_numbers.public_numbers
    elif isinstance(key, rsa.RSAPublicKey):
      public_numbers = key.public_numbers()
    else:
      raise TypeError()
    # PbWK Type Properties
    properties['n'] = BitArray(uint=public_numbers.n, length=key.key_size).tobytes().lstrip(b'\x00')
    properties['e'] = BitArray(uint=public_numbers.e, length=key.key_size).tobytes().lstrip(b'\x00')
    properties['d'] = BitArray(uint=private_numbers.d, length=key.key_size).tobytes().lstrip(b'\x00') if private_numbers else b''
    properties['p'] = BitArray(uint=private_numbers.p, length=key.key_size).tobytes().lstrip(b'\x00') if private_numbers else b''
    properties['q'] = BitArray(uint=private_numbers.q, length=key.key_size).tobytes().lstrip(b'\x00') if private_numbers else b''
    properties['dp'] = BitArray(uint=private_numbers.dmp1, length=key.key_size).tobytes().lstrip(b'\x00') if private_numbers else b''
    properties['dq'] = BitArray(uint=private_numbers.dmq1, length=key.key_size).tobytes().lstrip(b'\x00') if private_numbers else b''
    properties['qi'] = BitArray(uint=private_numbers.iqmp, length=key.key_size).tobytes().lstrip(b'\x00') if private_numbers else b''
    # done
    return cls(**properties)


  ##############################################################################
  # Symmetric
  ##############################################################################


  @classmethod
  def generate_oct_private_key(cls, key_size, **properties):
    assert(key_size % 8 == 0)
    key = os.urandom(int(key_size/8))
    return cls.from_key(key, **properties)


  @classmethod
  def from_oct_key(cls, key, **properties):
    # PbWK Type
    properties['kty'] = PbWKType.OCT
    # PBWK Type Properties
    private_number = None
    if isinstance(key, six.binary_type):
      private_number = key
      key_size = len(key)*8
    else:
      raise TypeError()
    # PbWK Type Properties
    properties['k'] = BitArray(bytes=private_number, length=key_size).tobytes().lstrip(b'\x00') if private_number else b''
    # done
    return cls(**properties)


  ##############################################################################
  # Interface
  ##############################################################################


  def decrypt(self, ciphertext, algorithm=None, padding=None, mode=None):
    raise NotImplementedError()


  def encrypt(self, plaintext, algorithm=None, padding=None, mode=None):
    raise NotImplementedError()


  def exchange(self, peer_public_key, algorithm):
    raise NotImplementedError()


  def sign(self, data):
    assert(isinstance(data, six.binary_type))
    key = self.extract_private_key()
    if self.alg == PbWKAlg.HS256:
      h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
      h.update(data)
      signature = h.finalize()
    elif self.alg == PbWKAlg.HS384:
      h = hmac.HMAC(key, hashes.SHA384(), backend=default_backend())
      h.update(data)
      signature = h.finalize()
    elif self.alg == PbWKAlg.HS512:
      h = hmac.HMAC(key, hashes.SHA512(), backend=default_backend())
      h.update(data)
      signature = h.finalize()
    elif self.alg == PbWKAlg.RS256:
      signature = key.sign(data, padding.PKCS1v15(), hashes.SHA256())
    elif self.alg == PbWKAlg.RS384:
      signature = key.sign(data, padding.PKCS1v15(), hashes.SHA384())
    elif self.alg == PbWKAlg.RS512:
      signature = key.sign(data, padding.PKCS1v15(), hashes.SHA512())
    elif self.alg == PbWKAlg.ES256:
      # TODO check that signature is the correct format
      # currently in DER format as defined in RFC3279
      signature = key.sign(data, ec.ECDSA(hashes.SHA256()))
    elif self.alg == PbWKAlg.ES384:
      # TODO check that signature is the correct format
      # currently in DER format as defined in RFC3279
      signature = key.sign(data, ec.ECDSA(hashes.SHA384()))
    elif self.alg == PbWKAlg.ES512:
      # TODO check that signature is the correct format
      # currently in DER format as defined in RFC3279
      signature = key.sign(data, ec.ECDSA(hashes.SHA512()))
    elif self.alg == PbWKAlg.PS256:
      signature = key.sign(data, padding.PSS(padding.MGF1(hashes.SHA256()), padding.PSS.MAX_LENGTH), hashes.SHA256())
    elif self.alg == PbWKAlg.PS384:
      signature = key.sign(data, padding.PSS(padding.MGF1(hashes.SHA384()), padding.PSS.MAX_LENGTH), hashes.SHA384())
    elif self.alg == PbWKAlg.PS512:
      signature = key.sign(data, padding.PSS(padding.MGF1(hashes.SHA512()), padding.PSS.MAX_LENGTH), hashes.SHA512())
    else:
      raise TypeError()
    return signature


  def verify(self, data, signature):
    assert(isinstance(data, six.binary_type))
    assert(isinstance(signature, six.binary_type))
    key = self.extract_public_key()
    if self.alg == PbWKAlg.HS256:
      h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
      h.update(data)
      h.verify(signature)
    elif self.alg == PbWKAlg.HS384:
      h = hmac.HMAC(key, hashes.SHA384(), backend=default_backend())
      h.update(data)
      h.verify(signature)
    elif self.alg == PbWKAlg.HS512:
      h = hmac.HMAC(key, hashes.SHA512(), backend=default_backend())
      h.update(data)
      h.verify(signature)
    elif self.alg == PbWKAlg.RS256:
      key.verify(signature, data, padding.PKCS1v15(), hashes.SHA256())
    elif self.alg == PbWKAlg.RS384:
      key.verify(signature, data, padding.PKCS1v15(), hashes.SHA384())
    elif self.alg == PbWKAlg.RS512:
      key.verify(signature, data, padding.PKCS1v15(), hashes.SHA512())
    elif self.alg == PbWKAlg.ES256:
      # TODO check that signature is the correct format
      # currently in DER format as defined in RFC3279
      key.verify(signature, data, ec.ECDSA(hashes.SHA256()))
    elif self.alg == PbWKAlg.ES384:
      # TODO check that signature is the correct format
      # currently in DER format as defined in RFC3279
      key.verify(signature, data, ec.ECDSA(hashes.SHA384()))
    elif self.alg == PbWKAlg.ES512:
      # TODO check that signature is the correct format
      # currently in DER format as defined in RFC3279
      key.verify(signature, data, ec.ECDSA(hashes.SHA512()))
    elif self.alg == PbWKAlg.PS256:
      key.verify(signature, data, padding.PSS(padding.MGF1(hashes.SHA256()), padding.PSS.MAX_LENGTH), hashes.SHA256())
    elif self.alg == PbWKAlg.PS384:
      key.verify(signature, data, padding.PSS(padding.MGF1(hashes.SHA384()), padding.PSS.MAX_LENGTH), hashes.SHA384())
    elif self.alg == PbWKAlg.PS512:
      key.verify(signature, data, padding.PSS(padding.MGF1(hashes.SHA512()), padding.PSS.MAX_LENGTH), hashes.SHA512())
    else:
      raise TypeError()


################################################################################
# PbWKSet
################################################################################


class PbWKSet(pb_object):


  __protobuf__ = PbWK_pb2.PbWKSet


  def append(self, key):
    assert(isinstance(key, PbWK))
    self.keys.extend([key.protobuf])


  def extend(self, keys):
    for key in keys:
      self.append(key)


  def __iter__(self):
    for key in self.keys:
      yield PbWK(key)


  def __getitem__(self, index):
    return PbWK(self.keys[index])


  ##############################################################################
  # Format
  ##############################################################################


  def to_json(self):
    json = dict()
    json['keys'] = list()
    for key in self:
      json['keys'].append(key.to_json())
    return json


  @classmethod
  def from_json(cls, json):
    self = cls()
    for jwk in json['keys']:
      self.append(PbWK.from_json(jwk))
    return self
