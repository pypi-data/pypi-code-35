"""
This module resolve VASP POTCAR related.
"""

import os
import glob
from . import utils
from . import vasprun
MOD_NAME = 'potcar'
POTCAR_STRING   = 'POTCAR'
DEFAULT_PP_TYPE = 'potpaw_PBE'


def get_potcar_content(pp_names=None, pp_type=DEFAULT_PP_TYPE):
    """
    Using VASPPOT_PATH to combine a POTCAR string with pp_names
    """
    assert utils.VASPPOT_PATH is not None, \
        'To use get_potcar, you need set VASPPOT env'
    if isinstance(pp_names, str):
        pp_names = [pp_names]
    assert isinstance(pp_names, (list, tuple)), \
        'You need to give a list or tuple as pp_names'
    assert pp_names, 'pp_names needs content'
    assert pp_type in utils.VALID_PP_TYPES, '{0} should belongs {1}'.format(pp_type, utils.VALID_PP_TYPES)

    output = ''
    for name in pp_names:
        path = os.path.join(utils.VASPPOT_PATH, pp_type, name, POTCAR_STRING+'*')
        candidate = glob.glob(path)
        if not candidate:
            raise ValueError(pp_type+' may not have '+name)
        elif len(candidate) > 1:
            raise Warning(name+' in '+pp_type+' has more than 1 candiate')
        output += utils.get_file_content(candidate[0])
    return output


def get_avail_pot(pp_names=None, pp_type=DEFAULT_PP_TYPE, preview=False):
    """
    list all available pot
    """
    def list_element_pot(element):
        reg_path = os.path.join(utils.VASPPOT_PATH, pp_type, element+'*', POTCAR_STRING+'*')
        return [path.split('/')[-2] for path in glob.glob(reg_path)]
    assert utils.VASPPOT_PATH is not None, \
        'To use get_potcar, you need set VASPPOT env'
    pp_names = pp_names or utils.CHEMICAL_SYMBOLS
    if isinstance(pp_names, str):
        pp_names = [pp_names]
    assert isinstance(pp_names, (list, tuple)), \
        'You need to give a list or tuple as pp_names or leave it blank'
    assert pp_names, 'pp_names needs content'
    assert pp_type in utils.VALID_PP_TYPES, '{0} should belongs {1}'.format(pp_type, utils.VALID_PP_TYPES)
    pp_dict = {}
    for pp_name in pp_names:
        pp_dict[pp_name] = list_element_pot(pp_name)
    if preview:
        import json
        print(pp_dict)
    else:
        return pp_dict


def gen_potcar(pp_names=None, pp_type=DEFAULT_PP_TYPE, dirname='.', preview=False):
    """
    Generate a POTCAR directly
    """
    assert isinstance(dirname, str) and os.path.isdir(dirname), \
        'dirname should exist'
    output = get_potcar_content(pp_names, pp_type)
    if preview:
        print(output)
    else:
        filename = os.path.join(dirname, POTCAR_STRING)
        with open(filename, 'w') as _fd:
            _fd.write(output)


def test(test_dir=None):
    """
    test of potcar
    """
    test_dir = test_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test_dir')
    os.environ['VASPPOT'] = os.path.join(test_dir, 'vasppot_sample')
    utils.reset_vasppot_path()
    print(utils.VASPPOT_PATH)
    gen_potcar(['H', 'He', 'Li'], preview=True)
    gen_potcar(['H', 'He', 'Li'], dirname='/tmp')

def cli_add_parser(subparsers):
    """
    potcar add_parser
    """
    subp = subparsers.add_parser(MOD_NAME, help='POTCAR')
    subp.add_argument('-i', '--input', metavar='PATH', help='Generate POTCAR with POSCAR')
    subp.add_argument('-d', '--dirname', metavar='PATH', default='.', help='directory to generate file')
    subp.add_argument('-p', '--ptype', default=DEFAULT_PP_TYPE, help='potcar type, avail: {0}'.format(utils.VALID_PP_TYPES))
    subp.add_argument('-l', '--list', action='store_true', help='list available potcar')
    subp.add_argument('pp_names', nargs='*')

def cli_args_exec(args):
    """
    potcar args_exec
    """
    if args.DEBUG:
        print(__file__)
    if args.test:
        test(args.test_dir)
    elif args.list:
        get_avail_pot(args.pp_names, args.ptype, True)
    else:
        gen_potcar(args.pp_names, args.ptype, args.dirname, args.preview)