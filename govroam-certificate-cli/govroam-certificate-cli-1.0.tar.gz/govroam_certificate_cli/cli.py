#!/usr/bin/env python

from simple_roaming_certificate import gencerts

import os,sys,getopt

def main(argv):
  c=u'GB'
  st=u'England'
  l=u'Manchester'
  o=u'WorkPlace'
  ou=u'WorkUnit'
  cn=u'Placeholder'
  crldp=u'http://placeholder/crldp'
  passphrase=b'something'
  directory=u'/tmp'
  bits=2048
  
  try:
    opts, args = getopt.getopt(argv,"c:s:l:o:u:n:r:p:d:b:")
  except getopt.GetoptError:
    print "cli.py -c <County> -s <State> -l <Location> -o <Organisation> -ou <Organisation Unit> -n <CN> -r <CRLDP> -p <password> -d <Output Directory> -b<2048|4096>"
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-c':
      c=unicode(arg, "utf-8")
    if opt == '-s':
      st=unicode(arg, "utf-8")
    if opt == '-l':
      l=unicode(arg, "utf-8")
    if opt == '-o':
      o=unicode(arg, "utf-8")
    if opt == '-u':
      ou=unicode(arg, "utf-8")
    if opt == '-n':
      cn=unicode(arg, "utf-8")
    if opt == '-r':
      crldp=unicode(arg, "utf-8")
    if opt == '-p':
      passphrase=arg
    if opt == '-d':
      directory=unicode(arg, "utf-8")
    if opt == '-b':
      bits=arg

  if not os.path.exists(directory):
    os.makedirs(directory)

  if not ( ( bits == 2048 ) or ( bits == 4096 ) ):
    print "Bits must be set to 2048 or 4096"
    sys.exit(2)
        
  csrsubject, cacert, cakey_enc, csrkey_enc, servercert, crlcert = gencerts(c,st,l,o,ou,cn,crldp,passphrase,bits)

  with open (directory + '/rootca.pem','w') as f:
    f.write(cacert)
    f.close
  
  with open (directory + '/root-key.pem','w') as f:
    f.write(cakey_enc)
    f.close
  
  with open (directory + '/server-cert.pem','w') as f:
    f.write(servercert)
    f.close
  
  with open (directory + '/server-key.pem','w') as f:
    f.write(csrkey_enc)
    f.close
  
  with open (directory + '/list.crl','w') as f:
    f.write(crlcert)
    f.close
  
if __name__ == "__main__":
  main(sys.argv[1:])
    

