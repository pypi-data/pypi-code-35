import cProfile, decimal

def test1():
    d = decimal.Decimal('0.1')
    for i in range(1000000):
        d += d

def test2():
    d = 0.1
    for i in range(1000000):
        d += d

cProfile.run('test1()')
cProfile.run('test2()')

