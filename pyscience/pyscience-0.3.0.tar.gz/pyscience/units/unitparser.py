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
from pyscience import get_resource
from pprint import pprint

DEBUG = False

class UnitParser:
    
    def __init__(self, filename=get_resource('units/units.txt')):
        
        with open(filename, 'r') as fd:
            self.fc = fd.read()
    
    def split_line(self, line): # TODO: Optimize?
        if line == '':
            return line, 0
        s = line.split(' ')
        n = 0
        for x in s:
            if x != '':
                break
            n+=1
        return line[n:], n
    
    def parse(self):
        tabindex = 0
        result = {'prefix':[], 'magnitude':[]}
        last_tabindex = 0
        tmp = {}
        
        for line in self.fc.splitlines():
            ln, tabindex = self.split_line(line)
            
            if ln.startswith('#'):
                continue
            if tabindex == 0:
                if ln.startswith('prefix'):
                    typ = 'prefix'
                    tmp['symbol'] = ln.split()[1]
                elif ln.startswith('magnitude'):
                    typ = 'magnitude'
                    tmp['name'] = ln.split()[1]
                    tmp['use_prefixes'] = True
                    tmp['units'] = {}
                    tmp['unit'] = ''
            elif tabindex == 4:
                if typ == 'prefix':
                    name, value = [x.strip() for x in ln.split(' ')]
                    tmp[name] = value
                    
                elif typ == 'magnitude':
                    if ln.startswith('unit '):
                        name, value = ln.split()
                        tmp[name] = value
                    if ln.startswith('use prefixes '):
                        if 'false' in ln:
                            tmp['use_prefixes'] = False
                        else:
                            tmp['use_prefixes'] = True
                    elif ln.startswith('def unit '):
                        terms = [x.strip() for x in ln[8:][len(ln.split()[2])+1:].split(';')]
                        offset = 0
                        factor = 1
                        for term in terms:
                            if term.startswith('offset'):
                                offset = float(term.split()[1])
                            elif term.startswith('factor'):
                                factor = float(eval(term[6:]))
                        
                        tmp['units'][ln.split()[2]] = {'factor': factor, 'offset': offset}
            
            if last_tabindex > tabindex:
                if tmp:
                    result[typ].append(tmp)
                tmp = {}
            
            last_tabindex = tabindex
        
        if DEBUG:
            pprint(result)
        
        return result
