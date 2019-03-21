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
'''
Created by Manuel Alcaraz on 22 May, 2018
'''

from pyscience import algebra
from pyscience.math import Fraction

class Variable:
    
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name', 'x')
    
    def __mul__(self, value):
        if isinstance(value, algebra.Monomial):
            return algebra.Monomial(variables=value.variables + self.name, coefficient=value.coefficient)
        elif isinstance(value, int):
            return algebra.Monomial(variables=self.name, coefficient=value)
        elif isinstance(value, Variable):
            return algebra.Monomial(variables=self.name + value.name)
        elif isinstance(value, Fraction):
            return algebra.Monomial(variables=self.name, coefficient=value)
        elif isinstance(value, algebra.Polynomial):
            return value * self
        
        raise TypeError(f'Cannot multiply Variable by {type(value)}')

    def __add__(self, value):
        if isinstance(value, algebra.Monomial):
            if value.variables == self.name:
                return algebra.Monomial(coefficient=1+value.coefficient, variables=self.name)
            else:
                return algebra.Polynomial(monomials=[algebra.Monomial(variables=self.name), value])
        elif isinstance(value, Variable):
            if value.name == self.name:
                return algebra.Monomial(coefficient=2, variables=self.name)
            else:
                return algebra.Polynomial(monomials=[algebra.Monomial(variables=self.name), algebra.Monomial(variables=value.name)])
        elif isinstance(value, int):
            return algebra.Polynomial(monomials=[algebra.Monomial(variables=self.name)], numerical_term=value)
        elif isinstance(value, Fraction):
            return Fraction(value.numerator + self*value.denominator, value.denominator)
        
        raise TypeError(f'Cannot add Variable to {type(value)}')
    
    def __radd__(self, value):
        return self.__add__(value)

    def __sub__(self, value):
        if isinstance(value, algebra.Monomial) and value.variables == self.name:
            return algebra.Monomial(coefficient=1-value.coefficient, variables=self.name)
        elif isinstance(value, Variable) and value.name == self.name:
            return 0
        elif isinstance(value, int):
            return algebra.Polynomial(monomials=[algebra.Monomial(variables=self.name),], numerical_term=-value)
        elif isinstance(value, Fraction):
            return Fraction(value.numerator - self*value.denominator, value.denominator)
        
        raise ValueError(f'Cannot subtract Variable to {type(value)}')
    
    def __rsub__(self, value):
        return (-self) + value
    
    def __truediv__(self, value):
        if isinstance(value, (int, Variable)):
            return Fraction(self, value)
        
        raise ValueError(f'Cannot divide a Variable by {type(value)}')
    
    def __rtruediv__(self, value):
        if isinstance(value, (int, value)):
            return Fraction(value, self)
        
        raise ValueError(f'Cannot divide a {type(value)} by a Variable')

    def __pow__(self, value, mod=None):
        if mod:
            raise NotImplementedError
        
        return algebra.Monomial(variables=self.name*value)
    
    def __rmul__(self, value):
        return self.__mul__(value)

    def __neg__(self):
        return algebra.Monomial(variables=self.name, coefficient=-1)
    
    def __pos__(self):
        return self
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f'<Variable {self.name}>'
