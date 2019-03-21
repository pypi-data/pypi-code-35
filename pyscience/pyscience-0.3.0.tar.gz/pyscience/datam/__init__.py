'''
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

# TODO: Data is in a very alpha status

from pprint import pprint

def get_type_of(s):
    if s.isdigit():
        return int
    elif '.' in s and s.replace('.','').isdigit():
        return float
    return str

def boolean(v):
    return len(v) == sum(v)

class Condition():
    def __init__(self, value, match=None):
        self.value = value
        self.match = match
    
    def __call__(self, value):
        bools = [x(value) for x in self.match]
        return boolean(bools)
    
    def __and__(self, cond):
        return Condition(self.value, self.match + [cond])
    
    def __eq__(self, v):
        ''' == '''
        return Condition(self.value, [lambda x: x[self.value] == v])
    
    def __gt__(self, v):
        ''' > '''
        return Condition(self.value, [lambda x: x[self.value] > v])
    
    def __lt__(self, v):
        ''' < '''
        return Condition(self.value, [lambda x: x[self.value] < v])
    
    def __le__(self, v):
        ''' <= '''
        return Condition(self.value, [lambda x: x[self.value] <= v])
    
    def __ne__(self, v):
        ''' != '''
        return Condition(self.value, [lambda x: x[self.value] != v])
    
    def __ge__(self, v):
        ''' >= '''
        return Condition(self.value, [lambda x: x[self.value] >= v])
    
    def __str__(self):
        return f'Condition("{self.value}")'
    
    def __repr__(self):
        return f'<Condition "{self.value}">'

class Data():
    def __init__(self, fn, header=True):
        self.fn = fn
        with open(fn, 'r') as fd:
            self.text_data = fd.read()
        
        self.data = []
        self.data_types = []
        
        nt = 0
        
        for line in self.text_data.splitlines():
            if header:
                self.header = line.split(',')
                for x in self.header:
                    self.data.append([])
                header = False
                nt = len(self.header)
                continue
            
            for number, item in enumerate(line.split(',')):
                item = item.strip()
                
                if len(self.data_types) < nt:
                    self.data_types.append(get_type_of(item))
                
                try:
                    item = self.data_types[number](item)
                except:
                    pass
                
                self.data[number].append(item)
        
    
    def __getitem__(self, key):
        if isinstance(key, str):
            if key in self.header:
                return self.data[self.header.index(key)]
            raise ValueError(f'{key} is not in header')
        elif isinstance(key, int):
            if key > len(self.data[0]):
                raise ValueError('Index is too big')
            
            R = {}
            for n, x in enumerate(self.data):
                R[self.header[n]] = x[key]
            return R
    
    def where(self, condition):
        R = []
        #print('Condition', condition)
        for x in range(len(self.data[0])):
            #print('For', self[x], 'is', condition(self[x]))
            b = self[x]
            if condition(b):
                R.append(b)
        return R

    def __str__(self):
        return f'<Data {self.fn}>'

    def __repr__(self):
        return f'<Data {self.fn}>'


