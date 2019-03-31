# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 16:30:21 2013

@author: elbar
"""

from numpy import polyadd, polymul
from scipy import signal

#-------------------------------------------------------------------------------
class TFPoly():
    ''' Transfer function polynomial                      '''

    def __init__(self, num=[1], den=[1]):
        ''' init vars '''
        self.num = num
        self.den = den

    def __str__(self):
        ''' poly string representation '''
        _str = "num = %s, den = %s" % (self.num, self.den)
        return _str

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
class FODTPoly():
    ''' Proccess polynomial                               '''
    ''' Fisrt Order with Delay                            '''
    ''' Proccess : F(s) = K * 1 / (ts + 1)                '''
    ''' num = [K], [den] = [t, 1]                         '''

    def __init__(self, gain=1.0, tau=1.0, dead_time=1.0, pade_order=4):
        ''' init vars '''
        self.gain = gain
        self.tau = tau
        self.dead_time = dead_time
        self.pade_order = pade_order
        self.num = []
        self.den = []
        self._build_poly()

    def _build_poly(self):
        ''' build polynomial '''
        self.num = [self.gain]
        self.den = [self.tau, 1]
        _pade = pade_poly(self.dead_time, self.pade_order)
        self.num = polymul(self.num, _pade.num)
        self.den = polymul(self.den, _pade.den)

    def __str__(self):
        ''' poly string representation '''
        _str = "num = %s, den = %s" % (self.num, self.den)
        return _str

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
class IntgrPoly():
    ''' Proccess polynomial                               '''
    ''' Integrating Proccess                              '''
    ''' Proccess : F(s) = K / s                           '''
    ''' num = [K], [den] = [1, 0]                         '''

    def __init__(self, gain=1.0, dead_time=1.0, pade_order=4):
        ''' init vars '''
        self.gain = gain
        self.dead_time = dead_time
        self.pade_order = pade_order
        self.num = []
        self.den = []
        self._build_poly()

    def _build_poly(self):
        ''' build polynomial '''
        self.num = [self.gain]
        self.den = [1, 0]
        _pade = pade_poly(self.dead_time, self.pade_order)
        self.num = polymul(self.num, _pade.num)
        self.den = polymul(self.den, _pade.den)

    def __str__(self):
        ''' poly string representation '''
        _str = "num = %s, den = %s" % (self.num, self.den)
        return _str

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
class PIDPoly():
    ''' PID polynomial                                                      '''
    ''' PID : PID(s) = Kc * [Ti*Td*s^2  + Ti*s + 1] / [Ti*s]                '''

    def __init__(self, kc=1.0, ti=1.0, td=1.0):
        ''' init vars '''
        self.kc = kc
        if (ti):
            self.ti = ti
        else:
            self.ti = 0.0
        if (td):
            self.td = td
        else:
            self.td = 0.0
        self.num = []
        self.den = []
        self._build_poly()

    def _build_poly(self):
        ''' build polynomial '''
        self.num = [self.ti * self.td, self.ti, 1]
        self.num [:] = [self.kc * x for x in self.num]
        if (self.ti) :
            self.den = [ self.ti, 0]
        else :
            self.den = [1]

    def __str__(self):
        ''' poly string representation '''
        _str = "num = %s, den = %s" % (self.num, self.den)
        return _str

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
class TransferFunction():
    ''' transfer function '''

    def __init__(self, sys):
        ''' init vars '''
        self.num = sys.num
        self.den = sys.den
        self._build_tf()

    def _build_tf(self):
        ''' build default transfer function '''
        self.lti = signal.lti(self.num, self.den)

    def set_lti(self, lti):
        ''' change transfer function directly'''
        self.num = lti.num
        self.den = lti.den
        self._build_tf()

    def bode(self):
        ''' bode return values '''
        return self.lti.bode()

    def step(self):
        ''' step response return values '''
        return self.lti.step()

    def impulse(self):
        ''' impulse response return values '''
        return self.lti.impulse()

    def output(self):
        ''' output response return values '''
        return self.lti.output()

    def nyquist(self):
        ''' nyquist response return values '''
        return self.lti.freqresp()

    def __str__(self):
        ''' transfer function string representation '''
        _str = "num = %s, den = %s" % (self.num, self.den)
        return _str

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def pade_poly(delay, n=1):
    '''
    Create a linear system that approximates a delay.
    Return the lti object of the Pade approximation.

    Parameters
    ----------
    t : time delay in sec
    n : order of approximation

    Returns
    -------
    num, den : array
    Polynomial coefficients of the delay model, in descending powers of s.

    Notes
    -----
    Based on an algorithm in Golub and van Loan, "Matrix Computation" 3rd.
    Ed. pp. 572-574.
    '''

    if delay == 0:
        num = [1,]
        den = [1,]
    else:
        num = [0. for i in range(n+1)]
        num[-1] = 1.
        den = [0. for i in range(n+1)]
        den[-1] = 1.
        c = 1.
        for k in range(1, n+1):
            c = delay * c * (n - k + 1)/(2 * n - k + 1)/k
            num[n - k] = c * (-1)**k
            den[n - k] = c
        num = [coeff/den[0] for coeff in num]
        den = [coeff/den[0] for coeff in den]

    return TFPoly(num, den)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def mul_poly(sys1, sys2):
    ''' multiply sys1 and sys2 LTI objects
        returns sys1 * sys2
    '''
    num1 = sys1.num
    den1 = sys1.den
    num2 = sys2.num
    den2 = sys2.den
    num = polymul(num1, num2)
    den = polymul(den1, den2)
    return TFPoly(num, den)

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def feedback_poly(sys1, sys2, sign=-1):
    ''' Feedback interconnection between sys1 and sys2 LTI objects
        returns sys1 / (1 - sign * sys1 * sys2)
    '''
    num1 = sys1.num
    den1 = sys1.den
    num2 = sys2.num
    den2 = sys2.den
    num = polymul(num1, den2)
    den = polyadd(polymul(den2, den1), -sign * polymul(num2, num1))
    return TFPoly(num, den)

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def closed_loop_poly(sys, pid):
    ''' Closed lopp LTI
        returns sys * pid / (1 + sys * pid)
    '''
    num1 = sys.num
    den1 = sys.den
    num2 = pid.num
    den2 = pid.den
    num = polymul(num1, num2)
    den = polyadd(polymul(den1, den2), polymul(num1, num2))
    return TFPoly(num, den)

#-------------------------------------------------------------------------------