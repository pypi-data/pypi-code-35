__all__ = ['gencerts']

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes

import datetime

def gen_cakey(bits):
  key = rsa.generate_private_key(
     public_exponent=65537,
     key_size=int(bits),
     backend=default_backend()
  )
  return key

def output_key_encrypted(key,passphrase):
     return key.private_bytes(
     encoding=serialization.Encoding.PEM,
     format=serialization.PrivateFormat.TraditionalOpenSSL,
     encryption_algorithm=serialization.BestAvailableEncryption(passphrase),
  )

def output_key(key):
     return key.private_bytes(
     encoding=serialization.Encoding.PEM,
     format=serialization.PrivateFormat.TraditionalOpenSSL,
     encryption_algorithm=serialization.NoEncryption(),
  )

def output_cert(cert):
    return cert.public_bytes(serialization.Encoding.PEM)

def build_name(c,st,l,o,ou,cn):
  array = []
  if (c):
    array.append(x509.NameAttribute(NameOID.COUNTRY_NAME,c))
  if (st): 
    array.append(x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME,st))
  if (l):
    array.append(x509.NameAttribute(NameOID.LOCALITY_NAME,l))
  if (o):
    array.append(x509.NameAttribute(NameOID.ORGANIZATION_NAME,o))
  if (ou): 
    array.append(x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME,ou))
  if (cn):
    array.append(x509.NameAttribute(NameOID.COMMON_NAME,cn))

  return x509.Name(array)


def build_rootca(key,subject,issuer,duration):

  cert = x509.CertificateBuilder().subject_name(
    subject
  ).issuer_name(
    issuer
  ).public_key(
    key.public_key() 
  ).serial_number(
    x509.random_serial_number()
  ).not_valid_before(
    datetime.datetime.utcnow()
  ).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=duration)
  ).add_extension(
    x509.AuthorityKeyIdentifier.from_issuer_public_key(key.public_key()),
    critical=False,  
  ).add_extension(
    x509.SubjectKeyIdentifier.from_public_key(key.public_key()),
    critical=False,
  ).add_extension(
    x509.BasicConstraints(True,None),
    critical=True,
  ).sign(key, hashes.SHA256(), default_backend())

  return cert

def build_servercert(cakey,root,name,crldp,duration,subject,serverkey):

  builder = x509.CertificateBuilder().subject_name(
    subject
  ).issuer_name(
    root.issuer
  ).public_key(
    serverkey.public_key()
  ).serial_number(
    x509.random_serial_number()
  ).not_valid_before(
    datetime.datetime.utcnow()
  ).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=duration)
  ).add_extension(
    x509.KeyUsage(True,True,True,False,False,False,False,False,False),
    critical=True,
  ).add_extension(
    x509.SubjectAlternativeName([x509.DNSName(name)]),
    critical=False,
  ).add_extension(
    x509.BasicConstraints(False,None),
    critical=True,
  ).add_extension(
    x509.ExtendedKeyUsage([x509.ExtendedKeyUsageOID.SERVER_AUTH]),
    critical=False,
  ).add_extension(
    x509.AuthorityKeyIdentifier.from_issuer_public_key(root.public_key()),
    critical=False,
  ).add_extension(
    x509.SubjectKeyIdentifier.from_public_key(cakey.public_key()),
    critical=False,
  )
  
  if ( crldp ):
    builder = builder.add_extension(
      x509.CRLDistributionPoints(
         [x509.DistributionPoint(
            [x509.UniformResourceIdentifier(crldp)],
            None,
            None,
            None
         )
      ]
      ),
      critical=False,
    )
  
  cert = builder.sign(cakey, hashes.SHA256(), default_backend())

  return cert

def build_crl(key,issuer,duration):
  builder = x509.CertificateRevocationListBuilder()
  builder = builder.issuer_name(issuer)

  builder = builder.last_update(datetime.datetime.today())
  builder = builder.next_update(datetime.datetime.today() + datetime.timedelta(days=duration))
    
  revoked_cert = x509.RevokedCertificateBuilder().serial_number(
    x509.random_serial_number()
  ).revocation_date(
    datetime.datetime.today()
  ).build(default_backend())

  crl = builder.sign(
    private_key=key, algorithm=hashes.SHA256(),
    backend=default_backend()
  )

  return crl
    
def gencerts(c,st,l,o,ou,cn,crldp,passphrase,bits):

## Build Root CA

  casubject = caissuer = build_name(c,st,l,o,ou,u'Root CA')

  cakey = gen_cakey(bits)

  cacert = build_rootca(cakey,casubject,caissuer,36500)

## Misc

  key = gen_cakey(bits)

  subject = build_name(c,st,l,o,ou,cn)

## Build Server Cert

  servercert = build_servercert(cakey,cacert,cn,crldp,36500,subject,key)

  crlcert = build_crl(cakey,caissuer,36500)

  return subject,output_cert(cacert),output_key_encrypted(cakey,passphrase),output_key_encrypted(key,passphrase),output_cert(servercert),output_cert(crlcert)
  