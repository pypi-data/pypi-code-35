"""
This is the template of submodule for developers.
If you want to add a submodule, please copy this to your module,
rename vars and write your parts.

IMPORTANT PARTS (used by cli)
    * MOD_NAME
    * test
    * cli_add_parser
    * cli_args_exec
"""

import os
import glob
from . import format_parser
from . import vasprun

MOD_NAME = 'outcar'
OUTCAR_STRING = 'OUTCAR'
DEFAULT_PP_TYPE = 'potpaw_PBE'

def parse_outcar(filename=OUTCAR_STRING, dirname=None):
    dirname = dirname or '.'
    assert isinstance(filename, str), 'filename should be a string, default OUTCAR'
    filepath = os.path.join(dirname, filename)
    assert os.path.isfile(filepath), '{0} does not exists'.format(filepath)
    return format_parser.read(filepath, format='vasp-out', get_dict=True)



def test(test_dir=None):
    """
    test of outcar
    """
    test_dir = test_dir or os.path.join(\
        os.path.dirname(os.path.abspath(__file__)), '..', 'test_dir')
    test_outcar = os.path.join(test_dir, 'OUTCAR')
    print(parse_outcar(test_outcar))

def cli_add_parser(subparsers):
    """
    outcar add_parser
    """
    subp = subparsers.add_parser(MOD_NAME, help=OUTCAR_STRING)
    subp.add_argument('-d', '--dirname', metavar='PATH', help='dirname')
    subp.add_argument('-t', '--calc_type', help='type of calcualtion result')
    subp.add_argument('filename', metavar='PATH', help='OUTCAR path')

def cli_args_exec(args):
    """
    outcar args_exec
    """
    if args.DEBUG:
        print(__file__)
    if args.test:
        test(args.test_dir)
    else:
        if not args.basic_parser and vasprun.find_vasprun(args.filename):
            sdict = vasprun.connection_with_other_file(args.filename)
        else:
            sdict = parse_outcar(args.filename, args.basedir or args.dirname)
        try:
            if args.calc_type:
                print(sdict[args.calc_type])
            else:
                print(sdict)
        except Exception:
            print('only {0} are calculated'.format(sdict.get_all_keys()))
