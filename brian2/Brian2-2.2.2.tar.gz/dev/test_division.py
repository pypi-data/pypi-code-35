from brian2 import *
prefs.codegen.string_expression_target = 'cython'
prefs.codegen.target = 'cython'

G = NeuronGroup(10, '''x : 1
                       y : 1''')
G.x = '-1//2'  # this uses numpy by default (prefs.codegen.string_expression_target)
G.run_regularly('y = -1//2')  # this uses the standard codegen target
run(defaultclock.dt)
print(G.x)
print(G.y)
