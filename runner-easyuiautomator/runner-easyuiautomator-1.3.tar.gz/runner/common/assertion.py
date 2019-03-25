# coding=utf-8
"""
Created on 2016年6月14日

@author: thomas.ning

"""

from .runnerlog import RunnerLog as Logger

class Assertion:
    '''Assertion class provides the assert statement in test case'''

    def __init__(self, order = None):
        self.failureException = AssertionError 
        self.order = order
        
    def assertTrue(self, expr=True, msg=None):
        '''Fail the test unless the expression is true.'''
        if expr != True:
            Logger.check_fail(msg, self.order)
            raise self.failureException, (msg + " deviceOrder=%s"%(self.order if self.order else 0))
    
    def assertFalse(self, expr=False, msg=None):
        '''Fail the test unless the expression is false.'''
        if expr != False:
            Logger.check_fail(msg, self.order)
            raise self.failureException, (msg + " deviceOrder=%s"%(self.order if self.order else 0))
    
    def assertEqual(self, first, second, msg=None):
        '''
        Fail if the two objects are unequal as determined by the == operator. 
        '''
        if not (first == second):
            if msg:
                Logger.check_fail(msg, self.order)
                raise self.failureException, (msg + " deviceOrder=%s"%(self.order if self.order else 0))
            else:
                Logger.check_fail('%s != %s'%(first, second), self.order)
                raise self.failureException, '%s != %s'%(first, second) + " deviceOrder=%s"%(self.order if self.order else 0)
    
    def assertNotEqual(self, first, second, msg=None):
        '''
        Fail if the two objects are equal as determined by the == operator. 
        '''
        if first == second:
            if msg:
                Logger.check_fail(msg, self.order)
                raise self.failureException, (msg + " deviceOrder=%s"%(self.order if self.order else 0))
            else:
                Logger.check_fail('%s != %s'%(first, second), self.order)
                raise self.failureException, '%s != %s'%(first, second) + " deviceOrder=%s"%(self.order if self.order else 0)
                       
    def assertMsg(self, msg):
        Logger.check_fail(msg, self.order)
        raise self.failureException, (msg + " deviceOrder=%d"%(self.order if self.order else 0))
    