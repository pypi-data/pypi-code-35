from brian2 import *
import os

prefs.codegen.target = 'cython'
prefs.codegen.runtime.cython.delete_source_files = False

@implementation('cython', '''
from myfoo cimport foo
''', sources=['myfoo.pyx'])
@check_units(x=volt, y=volt, result=volt)
def foo(x, y):
    return x + y + 3*volt

G = NeuronGroup(1, '''
                   func = foo(x, y) : volt
                   x : volt
                   y : volt''')
G.x = 1*volt
G.y = 2*volt
mon = StateMonitor(G, 'func', record=True)
net = Network(G, mon)
net.run(defaultclock.dt)
print(mon[0].func)
