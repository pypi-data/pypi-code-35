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
import copy
from pyscience import algebra
from pyscience.math import Fraction

def get_degree(value):
    '''Return de degree of an object, if it has, else 0'''
    if isinstance(value, (algebra.Monomial, algebra.Polynomial)):
        return value.degree
    elif isinstance(value, int):
        return 0
    return 0

def fractions(a, b):
    '''Return ``a`` and ``b`` as Fraction if they aren't'''
    if not isinstance(a, Fraction):
        a = Fraction(a)
    if not isinstance(b, Fraction):
        b = Fraction(b)
    return a, b

class Equation:
    
    def __init__(self, first_member, second_member=0):
        self.first_member = first_member
        self.second_member = second_member
        
    @property
    def degree(self):
        '''Return the degree of the Equation'''
        return max(get_degree(self.first_member), get_degree(self.second_member))
    
    def solve(self):
        '''Return the solution of the Equation'''
        first_member = copy.deepcopy(self.first_member)
        second_member = copy.deepcopy(self.second_member)
        
        if second_member != 0:
            first_member = first_member - second_member
            second_member = 0
        
        if get_degree(first_member) <= 1:
            # First-degree equation
            if isinstance(first_member, algebra.Monomial):
                return 0
            elif isinstance(first_member, int):
                return None
            elif isinstance(first_member, algebra.Polynomial):
                # Check if the number of variables is 1
                if len(first_member.list_of_variables) != 1:
                    raise NotImplementedError('Cannot solve a equation with more than one variable')
                
                if first_member.numerical_term % first_member.monomials[0].coefficient == 0:
                    return -(first_member.numerical_term // first_member.monomials[0].coefficient)
                return -Fraction(first_member.numerical_term, first_member.monomials[0].coefficient)
            elif isinstance(self.first_member, Fraction):
                if isinstance(self.second_member, (int, Fraction)):
                    a, b = fractions(self.first_member, self.second_member)
                    a, b = a.common_denominator(b)
                    return Equation(a.numerator, b.numerator).solve()
                elif isinstance(self.second_member, algebra.Polynomial):
                    a, b = fractions(self.first_member, self.second_member)
                    a, b = a.common_denominator(b)
                    return Equation(a.numerator, -b.numerator).solve()
                
                raise NotImplementedError
        
        raise NotImplementedError('Cannot solve a equation with a degree greater than 1')
    
    def __str__(self):
        return f'Eq({self.first_member} = {self.second_member})\nSolution: {self.solve()}'
    
    def __repr__(self):
        return f'<Equation {self.first_member} = {self.second_member}>'
