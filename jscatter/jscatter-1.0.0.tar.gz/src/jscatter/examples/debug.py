# -*- coding: utf-8 -*-
#  this file is intended to used in the debugger
# write a script that calls your function to debug it

import numpy as np

# some arrays
w = np.r_[-100:100]
q = np.r_[0.001:5:0.01]
x = np.r_[1:10]

import jscatter as js
import numpy as np
t = js.loglist(0.02, 40, 40)
q=np.r_[0.1:2:0.2]
zz1 = js.dynamic.finiteRouse(t, q, 100, [1]*20, ll=11.7/100**0.5, Wl4=9234e-4, tintern=0., Temp=273 + 60)



