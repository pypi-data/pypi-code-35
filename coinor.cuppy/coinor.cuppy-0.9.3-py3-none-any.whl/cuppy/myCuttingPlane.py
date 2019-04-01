'''
Created on Apr 1, 2019

@author: tkral
'''



solve(MILPInstance(module_name = 'coinor.cuppy.examples.MIP6'), whichCuts = [(gomoryCut, {})], display = True, debug_print = True,
      use_cglp = False)
