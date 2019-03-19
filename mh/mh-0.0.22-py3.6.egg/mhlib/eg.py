# eg.py
'''
eg lib code
Example imports or EG_VAR,
import mhlib, print (mhlib.eg.EG_VAR)
import mhlib.eg as eg, print (eg.EG_VAR)
from mhlib import eg, print (eg.EG_VAR)
from mhlib.eg import EG_VAR as eg_var, print (eg_var)
'''

import time
import mhlib.l2


EG_VAR='abcd'

def test():
    ''' returns a test string '''
    return 'ok'

class MhEg (object):
    ''' eg class doc string '''
    def runMh(self):
        ''' doc string for member function '''
        print ('ok run')
        return 10

    def slow(self):
         time.sleep(3)
         return


    def call_external_func(self):
        x = mhlib.l2.L2Mh()




if __name__ == '__main__':
    pass
