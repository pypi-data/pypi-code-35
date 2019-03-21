'''
pyscience - python science programming
Copyright (c) 2019 Manuel Alcaraz Zambrano

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import math

def lcm(a, b):
    '''Return the lower common denominator of ``a`` and ``b``'''
    n = 1
    while 1:
        if (a*n) % b == 0:
            return a*n
        n += 1

def is_even(n):
    '''Return if ``n`` is a even number'''
    return not n % 2

def is_odd(n):
    '''Return if ``n`` is a odd number'''
    return bool(n % 2)

def Div(n):
    '''Return divisors of ``n``'''
    R = []
    for i in range(1, n+1//2):
        if n%i == 0:
            R.append(i)
    R.append(n)
    
    return R

def _call(value):
    '''Internal function'''
    if isinstance(value, (SQRT, ABS)):
        return value()
    return value

class Expression:
    
    def __init__(self, value):
        self.value = value
        
    def __call__(self):
        value = _call(self.value)
        return self.function(value)
    
    def eval(self):
        return self.function(_call(self.value))
    
    def __str__(self):
        return str(self.__class__.__name__) + '(' + str(self.value) + ')'
    
    def __repr__(self):
        return f'<Expression {self.function}>'
        
class ABS(Expression):
    function = abs

class SQRT(Expression):
    function = math.sqrt

class SIN(Expression):
    function = math.sin

class COS(Expression):
    function = math.cos

class FACTORIAL(Expression):
    function = math.factorial

class ACOS(Expression):
    function = math.acos

class ATAN(Expression):
    function = math.atan
    
MATH_FUNCTIONS = {
    'ABS': ABS,
    'SQRT': SQRT,
    'SIN': SIN,
    'COS': COS,
    'FACTORIAL': FACTORIAL,
    'ACOS': ACOS,
    'ATAN': ATAN
    }

