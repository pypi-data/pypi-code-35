#! /usr/bin/env python

import numpy as np
from __init__ import ADO

n_data = 5000
n_calc = 500
x = np.random.rand(n_data)
y = np.random.rand(n_data+100)
targets = np.random.randint(2, size=n_data)

# ADO calculated without statistics
print(ADO(fx=x, gx=y, target=targets))

# ADO calculated with statistics (i.e. mean and stdev of ADO)
print(ADO(fx=x, gx=y, target=targets, stats=True))

# ADO example where you expect perfect similarity (i.e. compare x with x)
print(ADO(fx=x, gx=x, target=targets, n_data=n_calc))
print(ADO(fx=x, gx=x, target=targets, n_data=n_calc, stats=True, boot_loops=20))