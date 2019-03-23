from Crypto.PublicKey import ECC

def m(s):
    bs = int(s).to_bytes(66, 'big')
    h = bs.hex()
    return ''.join(['\\x'+h[k:k+2] for k in range(0, len(h), 2)])

def n(s):
    while s>0:
        print("0x%016X, " % (s & 0xFFFFFFFFFFFFFFFF), end="")
        s >>= 64
    print("")

Gx = 0x000000c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66
Gy = 0x0000011839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650

print(n(Gx))
print(n(Gy))

#G = ECC._curves['p521'].G
#p = ECC._curves['p521'].p
#R = 2**576

#print(m(p))

#x = G.x * R % p
#y = G.y * R % p

#print(n(x))
#print(n(y))

#p = int(ECC._curve.p)
#b = int(ECC._curve.b)

#a = ECC.EccPoint(0xDE2444BEBC8D36E682EDD27E0F271508617519B3221A8FA0B77CAB3989DA97C9,
#            0xC093AE7FF36E5380FC01A5AAD1E66659702DE80F53CEC576B6350B243042A256)

#x = int(a.x)
#y = int(a.y)
#lhs = (y**2) % p
#rhs = (x**3 -3*x + b) % p
#print(hex(lhs))
#print(hex(rhs))

#print(m(0xc51e4753afdec1e6b6c6a5b992f43f8dd0c7a8933072708b6522468b2ffb06fd))
#print("----------------")
#k = a * 0xc51e4753afdec1e6b6c6a5b992f43f8dd0c7a8933072708b6522468b2ffb06fd
#print(m(k.x))
#print(m(k.y))
