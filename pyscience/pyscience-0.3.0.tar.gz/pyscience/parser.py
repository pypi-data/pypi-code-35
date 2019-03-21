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
import pyscience

EXPONENTS = {
    '⁰': 0,
    '¹': 1,
    '²': 2,
    '³': 3,
    '⁴': 4,
    '⁵': 5,
    '⁶': 6,
    '⁷': 7,
    '⁸': 8,
    '⁹': 9,
}

def is_digit(value):
    '''Return if ``value`` is number (decimal or whole)'''
    if value.count('.') == 1 and value.replace('.','').isdigit() or value.isdigit():
        return True
    return False

def split_expression(expr):
    last_type = None
    tmp = ''
    result = []
    last = None
    
    for c in list(expr):
        if last_type == 'str' and c != "'":
            tmp += c
            continue
        if c in list('1234567890'):
            typ = 'number'
        elif last_type == 'number' and c == '.':
            typ = 'number'
        elif c in list('+-*/'):
            typ = 'operator'
        elif c == '.' and last_type == 'upper':
            pass
        elif c.isupper():
            if last == '(':
                if tmp != '':
                    result.append(tmp)
                tmp=''
            typ = 'upper'
        elif c.islower():
            if last == '.' or last_type == 'string':
                last_type= 'string'
                typ = 'string'
            elif last_type != 'upper' or last=='(':
                typ = 'none'
            elif last_type == 'upper':
                typ = 'upper'
            
        elif c == '(' and last_type == 'upper':
            pass
        elif c in list('¹²³⁴⁵⁶⁷⁸⁹⁰()'):
            typ = 'none'
        elif c == "'":
            if last_type != 'str':
                typ = 'str'
            else:
                result.append(tmp+c)
                last_type = 'str'
                tmp = ''
                continue
        else:
            typ = 'string'
        
        if typ != last_type or typ == 'none':
            result.append(tmp)
            tmp = ''
            last_type = typ
        tmp += c
        last = c
    
    if tmp:
        result.append(tmp)
    
    return result[1:]

def expand(expr):
    expr = expr.replace(' ', '')
    expr = split_expression(expr)
    
    if pyscience.DEBUG:
        print('split:', expr)
    
    last_type = None
    result = ''
    
    for x in expr:
        if not x:
            continue
        if x.startswith('.'):
            typ = 'none'
        elif x.islower():
            typ = 'variable'
        elif x[0].isupper() and x[-1] == '(':
            typ = 'function'
        elif x in list('+-*/') or x == '**':
            typ = 'operator'
        elif x[0] == x[-1] == "'":
            typ = 'string'
        elif x in list('¹²³⁴⁵⁶⁷⁸⁹⁰'):
            typ = 'exponent'
        elif is_digit(x):
            typ = 'number'
        elif x == ')':
            typ = 'symbol'
        elif x == '(':
            typ = 'start_parenthesis'
        elif x in list(',\''):
            typ = 'none'
        elif '.' in x and x[0].isupper():
            typ = 'attr'
        else:
            raise SyntaxError("'" + x + "'")
        
        if last_type in ('variable', 'exponent', 'symbol') and typ in ('number', 'variable'):
            result += '*'
        elif last_type == 'number' and typ in ('variable', 'attr'):
            result += '*'
        elif last_type in ('variable', 'number', 'symbol') and typ == 'start_parenthesis':
            result += '*'
        elif typ == 'exponent':
            if last_type != 'exponent':
                result += '**'
            result += str(EXPONENTS[x])
            last_type = 'exponent'
            continue
        
        result += x
        last_type = typ
    
    return result
