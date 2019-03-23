from common import inverse

b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
X = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
Y = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
Z = 1

t0 = X**2;    t1 = Y**2 % p;    t2 = Z**2;
t3 = X*Y;    t3 = (t3+t3) % p; Z3 = X*Z;
Z3 = (Z3+Z3) %p; Y3 = b*t2 % p;   Y3 = (Y3-Z3) % p;
X3 = (Y3+Y3) % p; Y3 = (X3+Y3)%p; X3 = (t1-Y3) % p;
Y3 = (t1+Y3) % p; Y3 = X3*Y3 % p; X3 = X3*t3 %p;
t3 = t2+t2; t2 = t2+t3; Z3 = b*Z3;
Z3 = Z3-t2; Z3 = (Z3-t0) % p; t3 = Z3+Z3;
Z3 = Z3+t3; t3 = t0+t0; t0 = t3+t0;
t0 = t0-t2; t0 = t0*Z3; Y3 = Y3+t0;
print "Z3", hex(Z3 % p)
print "Y", hex(Y % p)
print "Z", hex(Z % p)
t0 = Y*Z;    t0 = t0+t0; Z3 = t0*Z3;
print "Z3", hex(Z3 % p)
X3 = X3-Z3; Z3 = t0*t1; Z3 = Z3+Z3;
Z3 = Z3+Z3;

Z3inv = inverse(Z3, p)

print hex((X3*Z3inv) % p)
print hex((Y3*Z3inv) % p)
print hex((Z3*Z3inv) % p)
