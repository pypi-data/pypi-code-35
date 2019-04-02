"""
vasprun.xml parser
"""



import os
from . import format_parser


def find_vasprun(filename='INCAR'):
    """
    find vasprun.xml with a filename
    """
    assert isinstance(filename, str), 'filename should be a string'
    vasprun_filename = os.path.join(os.path.dirname(filename), 'vasprun.xml')
    if not os.path.exists(vasprun_filename):
        return None
    return vasprun_filename


def vasprun_parser(vasprun_filename):
    """
    vasprun parser
    """
    return format_parser.read(vasprun_filename, format='vasp-xml', get_dict=True)


def connection_with_other_file(filename):
    sdict = vasprun_parser(find_vasprun(filename))
    return sdict

    # filename = os.path.basename(filename)
    # # import pdb; pdb.set_trace()
    # if filename in ['INCAR']:
    #     return sdict['calc_arrays/parameters']
    # elif filename in ['OUTCAR']:
    #     return sdict
    # elif filename in ['DOSCAR']:
    #     return sdict['calc_arrays/dos']
    # elif filename in ['POSCAR', 'CONTCAR']:
    #     return sdict['positions']
    # elif filename in ['EIGENVAL']:
    #     return sdict['eigenvalues']
    # elif filename in ['POTCAR']:
    #     return sdict['calc_arrays/pseudopotential']
    # else:
    #     raise NotImplementedError(filename, 'not supported')

def test(test_dir=None):
    """
    test vasprun
    """
    test_dir = test_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test')
    assert isinstance(test_dir, str) and os.path.isdir(test_dir), \
        'test_dir: {0}\nYou need to git clone the repo and run the test'.format(test_dir)
    vasprun_filename = find_vasprun(os.path.join(test_dir, 'INCAR'))
    print(vasprun_parser(vasprun_filename))


