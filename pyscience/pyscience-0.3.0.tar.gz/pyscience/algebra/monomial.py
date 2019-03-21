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
from pyscience.math import Fraction, gcd

EXPONENTS = list('⁰¹²³⁴⁵⁶⁷⁸⁹')

def get_exponent(value):
    result = ''
    for x in list(str(value)):
        result += EXPONENTS[int(x)]
    
    return result

def group_variables(expr):
    '''Group variables with the same value.
        >>> group_variables('xxy')
        x²y
        >>> group_variables('xyzzy')
        xy²z²
        >>>
    '''
    assert type(expr) is str
    R = ''
    variables = []
    
    for letra in list(str(expr)):
        if not (letra in variables):
            variables.append(letra)
    
    for letra in variables:
        if expr.count(letra) != 1:            
            R += letra + get_exponent(expr.count(letra))
        else:
            R+=letra
    
    return R

def subtract(expr1, expr2):
    '''Simplify expr1 from expr2, like a division.

       >>> subtract('xx','xy') # xy
       { 'x': 1,
         'y': 1
       }
    '''
    R={}
    c1 = count_variables(expr1)
    c2 = count_variables(expr2)

    for x in c1.keys():
        if x in c2:
            R[x]=c1[x]-c2[x]
            if R[x] < 0:
                R[x] = 0
        else:
            R[x]=c1[x]
    for x in c2.keys():
        if x in R:
            if c2[x]-c1[x] > 0:
                R[x] = c2[x]-c1[x]
        else:
            R[x]=c2[x]

    # Remove zeros
    RC={}
    for x in R.keys():
        if R[x] != 0:
            RC[x]=R[x]
    
    return RC

def subtract_str(expr1, expr2):
    '''Like ``subtract``, but returns a str
    '''
    r = subtract(expr1, expr2)
    r2 = ''
    for x in r.keys():
        r2 += x * r[x]
    
    return r2

def count_variables(expr):
    '''Count variables with the same value.
        >>> count_variables('xxy')
        {
            'x': 2,
            'y': 1
        }
        >>>
    '''
    result = {}
    variables = []
    
    for x in list(expr):
        if not x in variables:
            variables.append(x)
    
    for x in variables:
        result[x] = expr.count(x)
    
    return result

class Monomial:
    
    def __init__(self, *args, **kwargs):
        self.variables = kwargs.get('variables', '')
        self.coefficient = kwargs.get('coefficient', 1)
    
    @property
    def degree(self):
        return sum(count_variables(self.variables).values())
    
    @property
    def list_of_variables(self):
        return list(count_variables(self.variables).keys())
    
    def __mul__(self, value):
        if isinstance(value, int):
            return Monomial(variables=self.variables, coefficient=self.coefficient*value)
        elif isinstance(value, Monomial):
            return Monomial(variables=self.variables+value.variables, coefficient=self.coefficient*value.coefficient)
        elif isinstance(value, algebra.Variable):
            return Monomial(variables=self.variables+value.name, coefficient=self.coefficient)
        elif isinstance(value, algebra.Polynomial):
            return value * self
        elif isinstance(value, Fraction):
            return Fraction(value.numerator * self, value.denominator)
        
        raise TypeError(f'Cannot multiply Monomial by {type(value)}')

    def __rmul__(self, value):
        return self.__mul__(value)

    def __truediv__(self, value):
        if isinstance(value, int):
            if self.coefficient % value == 0:
                return Monomial(coefficient=int(self.coefficient/value), variables=self.variables)
            else:
                return Monomial(coefficient=Fraction(self.coefficient,value), variables=self.variables)
        elif isinstance(value, Fraction):
            return self * value
        elif isinstance(value, algebra.Variable):
            c = count_variables(self.variables)
            
            if len(c) == 1 and list(c.keys())[0] == value.name:
                v = subtract(self.variables, value.name)
                return Monomial(coefficient=self.coefficient, variables=value.name*list(v.values())[0])
            
            return Fraction(self, value)
        elif isinstance(value, Monomial):
            s = subtract(self.variables, value.variables)
            if not s:
                if self.coefficient % value.coefficient == 0:
                    # Si el resto da cero, devuelve un int
                    return self.coefficient // value.coefficient
                else:
                    return Fraction(self.coefficient, value.coefficient)
            elif sum(list(s.values())) == len(s.values()):
                v = ''
                for x in s.keys():
                    v += x*s[x]
                    
                if self.coefficient % value.coefficient == 0:
                    return Monomial(coefficient=self.coefficient//value.coefficient, variables=v)
                else:
                    return Monomial(coefficient=Fraction(self.coefficient, value.coefficient), variables=v)
            else:
                # Hay que devolver una fracción con letras
                m = gcd(self.coefficient, value.coefficient)
                if m != 1:
                    self.coefficient //= m
                    value.coefficient //= m
                
                if value.coefficient == 1 and len(value.variables) == 1:
                    value = algebra.Variable(name=value.variables)
                
                if self.coefficient == 1 and len(self.variables) == 1:
                    return Fraction(algebra.Variable(name=self.variables), value)
                
                return Fraction(self, value)
        
        raise TypeError(f'Cannot divide Monomial by {type(value)}')

    def __rtruediv__(self, value):
        if isinstance(value, int):
            if value % self.coefficient == 0:
                return Monomial(coefficient=value//self.coefficient, variables=self.variables)
            else:
                return Fraction(value, self)
        elif isinstance(value, algebra.Variable):
            return Fraction(value, self)
        
        raise NotImplementedError

    def __add__(self, value):
        if isinstance(value, Monomial) and count_variables(value.variables) == count_variables(self.variables):
            if self.coefficient + value.coefficient == 1 and len(self.variables) == 1:
                return algebra.Variable(name=self.variables)
            return Monomial(coefficient=self.coefficient+value.coefficient,variables=self.variables)
        elif isinstance(value, algebra.Variable):
            if value.name == self.variables:
                return Monomial(coefficient=self.coefficient+1,variables=self.variables)
            else:
                return algebra.Polynomial(monomials=[self, algebra.Monomial(variables=value.name)])
        elif isinstance(value, Fraction):
            value.numerator += self * value.denominator
            return value
        elif isinstance(value, Monomial):
            return algebra.Polynomial(monomials=[algebra.Monomial(coefficient=self.coefficient,variables=self.variables),value])
        elif isinstance(value, int):
            return algebra.Polynomial(monomials=[self,],numerical_term=value)
        
        raise TypeError(f'Cannot add Monomial to {type(value)}')
    
    def __radd__(self, value):
        return self + value

    def __sub__(self, value):
        if isinstance(value, Monomial) and count_variables(value.variables) == count_variables(self.variables):
            return Monomial(coefficient=self.coefficient-value.coefficient, variables=self.variables)
        elif isinstance(value, algebra.Variable):
            if value.name == self.variables:
                return Monomial(coefficient=self.coefficient-1, variables=self.variables)
            elif value.name in self.variables:
                s = subtract_str(self.variables, value.name)
                return Monomial(coefficient=self.coefficient, variables=s)
            else:
                return algebra.Polynomial(monomials=[self, -Monomial(variables=value.name)])
        elif isinstance(value, int):
            return algebra.Polynomial(monomials=[self,],numerical_term=-value)
        elif isinstance(value, Monomial):
            return algebra.Polynomial(monomials=[self,-value])
        elif isinstance(value, algebra.Polynomial):
            return value - self
        elif isinstance(value, Fraction):
            return value - self
        
        raise TypeError(f'Cannot subtract Monomial to {type(value)}')
    
    def __pow__(self, value, mod=None):
        if mod:
            raise NotImplementedError
        
        return Monomial(variables=self.variables*value, coefficient=self.coefficient**value)

    def __rsub__(self, value):
        return  - self + value

    def __neg__(self):
        return Monomial(variables=self.variables, coefficient=-self.coefficient)
    
    def __str__(self):
        if self.coefficient != 1:
            if self.coefficient == -1:
                return '-'+group_variables(self.variables)
            elif self.coefficient == 0:
                return '0'
            else:
                return str(self.coefficient)+group_variables(self.variables)
        else:
            return group_variables(self.variables)
    
    def __repr__(self):
        return f'<Monomial {self}>'
        
