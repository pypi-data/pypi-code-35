"""
select atoms needed
"""
from collections import Iterable
from .utils import CHEMICAL_SYMBOLS

def select_region(selections, positions, region):
    """
    selection in region from selections
    """
    if not region:
        return selections
    region = list(region) + [None, None]
    assert all([x is None or isinstance(x, Iterable) and len(x) == 2\
        for x in region]), 'region should be collections of x,y,z region'
        
    output = []
    for sel in selections:
        for regi, reg in enumerate(region[:3]):
            if reg:
                if reg[0] <= positions[sel][regi] <= reg[1]:
                    output.append(sel)
    return output



def select_atoms(symbols, positions, selections, region=None):
    """
    select atoms from selections & region
    """
    if not isinstance(selections, Iterable):
        selections = [selections]
    output = []
    for sel in set(selections):
        if isinstance(sel, int):
            output.append(sel)
        elif isinstance(sel, str) and sel.strip() in CHEMICAL_SYMBOLS:
            output.extend(select_region([x for x in range(len(symbols))\
                if symbols[x] in sel], positions, region))
    return output



def test():
    from ase.build import molecule
    c6h6 = molecule('C6H6')
    test_cases = [
        {
            'selections' : [1, 5, 3, 6],
            'region' : None,
        },
        {
            'selections' : [1, 1, 1, 1],
            'region' : None,
        },
        {
            'selections' : ['C'],
            'region' : None,
        },
        {
            'selections' : ['C'],
            'region' : [None, (0, float('inf')), None],
        },
        {
            'selections' : ['C', 'C', 'H'],
            'region' : [None, (0, float('inf')), None],
        },
        ]
    for i, case in enumerate(test_cases):
        try:
            print(case)
            print(select_atoms(c6h6.get_chemical_symbols(), c6h6.get_positions(),
                         **case))
        except Exception as e:
            print('ERROR case:', i)
            print(e)

if __name__ == '__main__':
    test()
