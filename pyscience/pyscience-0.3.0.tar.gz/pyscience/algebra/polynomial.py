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
from pyscience.algebra.monomial import count_variables
from pyscience.math.fraction import Fraction

class Polynomial:
    def __init__(self, *args, **kwargs):
        self.monomials = kwargs.get('monomials', [])
        self.numerical_term = kwargs.get('numerical_term', 0)
    
    @property
    def degree(self):
        return max([x.degree for x in self.monomials])
    
    @property
    def list_of_variables(self):
        # TODO: Optimize function.
        ml = [x.list_of_variables for x in self.monomials]
        ml = [''.join(x) for x in ml]
        ml = ''.join(ml)
        ml = count_variables(ml).keys()
        ml = list(ml)
        return ml

    def __add__(self, value):
        if isinstance(value, algebra.Monomial):
            result = Polynomial(numerical_term=self.numerical_term)
            found = False
            for monomial in self.monomials:
                if algebra.monomial.count_variables(monomial.variables) == algebra.monomial.count_variables(value.variables):
                    if not found:
                        if monomial.coefficient + value.coefficient != 0:
                            result.monomials.append(monomial + value)
                        found = True
                else:
                    result.monomials.append(monomial)
            if not found:
                result.monomials.append(value)
            return result
        elif isinstance(value, Polynomial):
            result = algebra.Polynomial()
            
            for monomial in self.monomials:
                result += monomial
            
            for monomial in value.monomials:
                result += monomial
            
            result += self.numerical_term + value.numerical_term
            
            return result
        elif isinstance(value, int):
            self.numerical_term += value
            return self
        elif isinstance(value, algebra.Variable):
            return self + algebra.Monomial(variables=value.name)
        elif isinstance(value, Fraction):
            return Fraction(value.numerator - (value.denominator*self), value.denominator)
        
        raise TypeError(f'Cannot add a Polynomial to {type(value)}')
    
    def __radd__(self, value):
        return self + value

    def __sub__(self, value):
        if isinstance(value, algebra.Monomial):
            result = Polynomial(numerical_term=self.numerical_term)
            found = False
            for monomial in self.monomials:
                if algebra.monomial.count_variables(monomial.variables) == algebra.monomial.count_variables(value.variables):
                    if not found:
                        if monomial.coefficient - value.coefficient != 0:
                            result.monomials.append(monomial - value)
                        found = True
                else:
                    result.monomials.append(monomial)
            if not found:
                result.monomials.append(value)
            return result
        elif isinstance(value, Polynomial):
            result = Polynomial()
            
            for monomial in self.monomials:
                result -= monomial
            
            for monomial in value.monomials:
                result -= monomial
            
            result.numerical_term += self.numerical_term - value.numerical_term
            
            return result
        elif isinstance(value, int):
            self.numerical_term -= value
            return self
        elif isinstance(value, algebra.Variable):
            return self - algebra.Monomial(variables=value.name, coefficient=-1)
        elif isinstance(value, Fraction):
            frac = Fraction(1, value.denominator) * value.numerator + self
            return frac
        
        raise TypeError(f'Cannot subtract a Polynomial to {type(value)}')
    
    def __rsub__(self, value):
        return self.__sub__(value)

    def __truediv__(self, value):
        if isinstance(value, int):
            # TODO: Simplify division
            return Fraction(self, value)
        elif isinstance(value, Fraction):
            return Fraction(self) * value.reverse()
        elif isinstance(value, algebra.Variable):
            raise NotImplementedError
        elif isinstance(value, algebra.Monomial):
            return Fraction(self, value)
        elif isinstance(value, Polynomial):
            raise NotImplementedError
        
        return TypeError(f'Cannot divide a Polynomial by {type(value)}')

    def __mul__(self, value):
        if isinstance(value, (algebra.Monomial, int)):
            result = algebra.Polynomial()
            
            for monomial in self.monomials:
                result += monomial * value
            
            if self.numerical_term:
                result += self.numerical_term * value
            
            return result
        elif isinstance(value, Polynomial):
            result = algebra.Polynomial()
            
            for monomial in self.monomials:
                result += monomial * value
                
            result += self.numerical_term * value
            
            return result
        elif isinstance(value, algebra.Variable):
            result = Polynomial()
            
            for monomial in self.monomials:
                result += monomial * value
                
            if self.numerical_term:
                result += self.numerical_term * value
            
            return result
        elif isinstance(value, Fraction):
            result = Polynomial()
            
            for monomial in self.monomials:
                result += monomial * value
                
            if self.numerical_term:
                result += self.numerical_term * value
            
            return result
        
        raise TypeError(f'Cannot multiply a Polynomial by {type(value)}')
    
    def __rmul__(self, value):
        return self * value

    def __pow__(self, value, mod=None):
        if mod:
            raise NotImplementedError
        
        return Polynomial(monomials=[x ** value for x in self.monomials], numerical_term=self.numerical_term ** value)
        
    def __str__(self):
        result = ''.join(['+'+str(x) if x.coefficient > 0 else str(x) for x in self.monomials])
        result += (str(self.numerical_term) if self.numerical_term < 0 else '+' + str(self.numerical_term)) if self.numerical_term else ''
        return result
        
    def __neg__(self):
        return Polynomial(monomials=[-x for x in self.monomials], numerical_term=-self.numerical_term)
    
    def __pos__(self):
        return self

    def __repr__(self):
        return f'<Polynomial {self}>'
