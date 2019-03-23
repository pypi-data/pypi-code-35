from Crypto.PublicKey import ECC

def m(s):
    bs = int(s).to_bytes(32, 'big')
    h = bs.hex()
    return ''.join(['\\x'+h[k:k+2] for k in range(0, len(h), 2)])


def is_on_curve(x, y):
    x = int(x)
    y = int(y)
    b = int(ECC._curve.b)
    p = int(ECC._curve.p)
    lhs = (y**2) % p
    rhs = (x**3 -3*x + b) % p
    assert(lhs == rhs)

p = int(ECC._curve.p)
b = int(ECC._curve.b)

a = ECC._curve.G.copy()
print(m(a.x * 0x0a % p), ":", m(a.y * 0x0a % p))

#b = ECC._curve.G * 10
#print(m(b.x * 0x0a % p), ":", m(b.y * 0x0a % p))

#c = a + b

#k = 0x7E70D649387CDEE87DBCE85888CEE4D933509BFF02C64F0F8330DE9CF6384ED4

#print(m(c.x * k % p), ":", m(c.y * k % p), ":", m(k))

#print(m(a.x * 0x0a % p), ":", m(a.y * 0x0a % p))
#print(m(b.x), ":", m(b.y))

# is_on_curve(x, y)

#j = a * 0xFFF
#print(m(j.x))
#print(m(j.y))
#print("---")
#print(m(j.x * 0x0a % p))
#print(m(j.y * 0x0a % p))
#print("---")
#f = j * 2
#f = j.copy()
#f.double()
#z = 0x3937221464ADAE328ECA1516B48216897C10DC45BAC95F0E2F103478B3ED5B1D
#print(m(f.x * z % p))
#print(m(f.y * z % p))
#print(m(z))
#print(m(b))

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
