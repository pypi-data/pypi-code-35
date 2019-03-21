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

from pyscience.math import lcm

from math import gcd # greater common denominator

def simplify(frac):
    '''Simplify a Fraction'''
    m = gcd(frac.numerator, frac.denominator)
    if m != 1:
        frac.numerator //= m
        frac.denominator //= m
    
    if frac.numerator % frac.denominator == 0:
        return int(frac.numerator / frac.denominator)
    
    return frac


class Fraction():
    
    def __init__(self, numerator, denominator=1):
        '''Fraction class.
        Create a Fraction with ``numerator`` and ``denominator``.
        You can operate with it as a normal number. Examples:
        
        >>> a = Fraction(2, 3)
        >>> b = Fraction(3, 4)
        >>> a + b
        F(17,12)
        >>> a * b
        F(1,2)
        >>> b + Fraction(1, 2)
        F(5,4)
        '''
        self.numerator = numerator
        self.denominator = denominator
        
    def __add__(self, value):
        if isinstance(value, int):
            return Fraction(self.numerator+self.denominator*value, self.denominator).simplify()
        elif isinstance(value, Fraction):
            a, b = self.common_denominator(value)
            return Fraction(a.numerator+b.numerator, a.denominator).simplify()
        
        return NotImplemented
    
    def __sub__(self, value):
        if isinstance(value, int):
            return Fraction(self.numerator-self.denominator*value, self.denominator).simplify()
        elif isinstance(value, Fraction):
            a, b = self.common_denominator(value)
            return Fraction(a.numerator-b.numerator, a.denominator).simplify()
        
        return NotImplemented
    
    def __rsub__(self, value):
        return self.__sub__(value)
    
    def __mul__(self, value):
        if isinstance(value, int):
            return Fraction(self.numerator*value, self.denominator).simplify()
        elif isinstance(value, Fraction):
            return Fraction(self.numerator*value.numerator, self.denominator*value.denominator).simplify()
        
        return NotImplemented
    
    def __rmul__(self, value):
        return self * value
    
    def __truediv__(self, value):
        if isinstance(value, int):
            return (self * Fraction(1,value)).simplify()
        elif isinstance(value, Fraction):
            return simplify(self * value.reverse())
        
        return NotImplemented
    
    def __pow__(self, value, mod=None):
        if mod:
            raise NotImplementedError
        
        if isinstance(value, int):
            return Fraction(self.numerator**value, self.denominator**value).simplify()
        
        return NotImplemented
    
    def with_denominator(self, value):
        if self.denominator == value:
            return self
        return Fraction(value//self.denominator*self.numerator, value)
    
    def common_denominator(self, value):
        ''' Return two fractions, with equal denominator, ``self`` and ``value``'''
        if self.denominator == value.denominator:
            return self, value
        
        cd = lcm(self.denominator, value.denominator)
        #print('cd:',cd)
        
        #print('Common denominator:', cd)
        #print('Common denominator / self.denominator', cd // self.denominator)
        #print('* self.numerator =', (cd//self.denominator)*self.numerator)
        #print()
        #print('Common denominator:', cd)
        #print('Common denominator / value.denominator', cd // value.denominator)
        #print(f'* {value.numerator} =', (cd//value.denominator)*value.numerator)
        
        return Fraction((cd//self.denominator)*self.numerator, cd), Fraction((cd//value.denominator)*value.numerator, cd)
    
    def simplify(self):
        '''Simplify fraction'''
        if self.denominator == 1:
            return self.numerator
        
        if not (isinstance(self.numerator, int) and isinstance(self.denominator, int)):
            # Try to simplify dividing
            return self.numerator / self.denominator
        
        m = gcd(self.numerator, self.denominator)
        if m != 1:
            self.numerator //= m
            self.denominator //= m
        
        if self.numerator % self.denominator == 0:
            return int(self.numerator / self.denominator)
        
        return self
    
    def reverse(self):
        return Fraction(self.denominator, self.numerator)
    
    @property
    def degree(self):
        return 1
    
    def __neg__(self):
        return Fraction(-self.numerator, self.denominator).simplify()
    
    def __pos__(self):
        return self
    
    def __str__(self):
        return f'F({self.numerator}/{self.denominator})'
    
    def __repr__(self):
        return f'<Fraction {self.numerator}/{self.denominator} ({type(self.numerator)}, {type(self.denominator)})>'
