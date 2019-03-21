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

from pyscience.units.unitparser import UnitParser

UNITS = UnitParser()
UNITS = UNITS.parse()

class Unit:
    '''TODO: Units is very unstable and may change its API in next releases
    TODO: This module is experimental and may not work well.
    '''
    def __init__(self, type_=None, name=None, value=1, prefix=None, unit=None, offset=0, factor=1):
        self.type_ = type_
        self.name = name
        self.value = value
        self.prefix = prefix
        self.unit = unit
        self.offset = offset
        self.factor = factor
    
    def to(self, unit):
        if not isinstance(unit, Unit):
            raise TypeError('unit must be a Unit class')
        
        if not unit.type_ == self.type_:
            raise TypeError('Cannot convert unit to ' + unit.type_)
        
        if self.name == unit.name:
            return self
        
        for mag in UNITS['magnitude']:
            if self.name in mag['units'] or self.name.endswith(mag['unit']) or self.name == mag['unit']\
                    or self.name.endswith(tuple(mag['units'].keys())):
                
                target_unit = {'factor': unit.factor, 'offset': unit.offset}
                
                if self.name in mag['units']:
                    source_unit = mag['units'][self.name]
                else:
                    source_unit = {'factor': self.factor, 'offset': self.offset}
                #
                result = self.value
                
                if source_unit['offset']:
                    result += source_unit['offset']
                
                result *= source_unit['factor']
                #
                result /= target_unit['factor']
                
                if target_unit['offset']:
                    result -= target_unit['offset']
                
                return Unit(name=unit.name, value=result)
                
        raise BaseException
    
    def __rmul__(self, value):
        return Unit(name=self.name, value=value, factor=self.factor, offset=self.offset, type_=self.type_)
    
    def __str__(self):
        return f'{self.value} {self.name}'
    
    def __repr__(self):
        return f'<Unit {self.value} {self.unit} ({self.type_}) offset {self.offset} factor {self.factor}>'

class Units:
    
    def __init__(self):
        pass
    
    def __getattr__(self, name):
        for mag in UNITS['magnitude']:
            if name in mag['units']:
                return Unit(name=name, unit=name, offset=mag['units'][name]['offset'], factor=mag['units'][name]['factor'], type_=mag['name'])
            elif name == mag['unit']:
                return Unit(name=name, unit=name, type_=mag['name'])
            elif name[1:] in mag['units']:
                for fac in UNITS['prefix']:
                    if fac['symbol'] == name[0]:
                        factor = fac['value']
                factor = float(factor)
                return Unit(name=name, factor=factor, unit=name[1:], type_=mag['name'])
        
        if name.startswith(tuple([x['symbol'] for x in UNITS['prefix']])):
            for mag in UNITS['magnitude']:
                if mag['use_prefixes'] and name.endswith(mag['unit']):
                    for fac in UNITS['prefix']:
                        if name.startswith(fac['symbol']):
                            factor = fac['value']
                    factor = float(eval(factor))
                    return Unit(name=name, factor=factor, unit=name, type_=mag['name'])
        
        raise ValueError(f'Unit "{name}" does not exit') # Or it is not implemented yet

