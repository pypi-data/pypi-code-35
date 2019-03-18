""" A straightforward API to perform basic RSA-based operations.

.. moduleauthor:: Christophe VG <contact@christophe.vg>

"""

__version__ = "1.0.0"

from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding


def generate_key_pair():
  key = rsa.generate_private_key(
     public_exponent=65537,
     key_size=2048,
     backend=default_backend()
  )
  return key, key.public_key()

def encode(key):
  if isinstance(key, rsa.RSAPublicKey):
    return key.public_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
  else:
    return key.private_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PrivateFormat.TraditionalOpenSSL,
      encryption_algorithm=serialization.NoEncryption()
    )

def decode(pem):
  try:
    pem = pem.encode("ascii","ignore") # unicode -> str
  except AttributeError:
    pass
  if b"PUBLIC KEY" in pem:
    return serialization.load_pem_public_key(
      pem,
      backend=default_backend()
    )
  else:
    return serialization.load_pem_private_key(
      pem,
      password=None,
      backend=default_backend()
    )

def sign(payload, key):
  return key.sign(
    payload,
    padding.PSS(
      mgf=padding.MGF1(hashes.SHA256()),
      salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
  )
  
def validate(payload, signature, key):
  key.verify(
    signature,
    payload,
    padding.PSS(
      mgf=padding.MGF1(hashes.SHA256()),
      salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
  )
  return True
