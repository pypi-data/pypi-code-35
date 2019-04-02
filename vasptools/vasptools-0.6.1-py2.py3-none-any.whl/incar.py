"""
vasptools incar module
"""



import os
import re
from io import StringIO
from configparser import ConfigParser
from . import vasprun
from .ext_types import ExtDict


MOD_NAME = INCAR_STRING = 'incar'
INCAR_SECTION_STRING = '['+INCAR_STRING+']'



def parse_incar(incar=None, force_basic_parser=False):
    """
    parse incar file to a dict using configparser
    """
    incar = incar or INCAR_STRING
    assert isinstance(incar, str) and os.path.exists(incar),\
        'INCAR file should be given'
    if not force_basic_parser and vasprun.find_vasprun(incar):
        sdict = vasprun.connection_with_other_file(incar)
        return sdict['calc_arrays/parameters']
    buff = INCAR_SECTION_STRING+'\n'
    with open(incar) as _fd:
        buff += _fd.read().lower()
    buff = re.sub(r'\n\s+', '\n', buff)
    conf = ConfigParser(inline_comment_prefixes=('#', ';'))
    conf.read_string(buff)
    return ExtDict(conf.items(INCAR_STRING))


def preview_parse_incar(incar=None):
    """
    preview the dict parsed
    """
    import json_tricks
    print(json_tricks.dumps(parse_incar(incar), indent=4))



def output_incar(incar_dict=None):
    """
    output a incar string using incar_dict
    """
    assert isinstance(incar_dict, dict), 'incar_dict should be a dict'
    incar_dict = {
        INCAR_STRING: incar_dict
        }
    conf = ConfigParser()
    conf.read_dict(incar_dict)
    buff = StringIO()
    conf.write(buff)
    buff = buff.getvalue()
    assert buff.startswith(INCAR_SECTION_STRING), 'output_incar buff error: '+buff
    return buff[len(INCAR_SECTION_STRING):]


def preview_output_incar(incar_dict=None):
    """
    preview INCAR with incar_dict
    """
    print(output_incar(incar_dict))


def gen_incar(incar_dict=None, dirname='.'):
    """
    write a INCAR directly
    """
    filename = os.path.join(dirname, INCAR_STRING)
    with open(filename, 'w') as _fd:
        _fd.write(output_incar(incar_dict))


def test(test_dir=None):
    """
    Test incar
    """
    test_dir = test_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test')
    assert isinstance(test_dir, str) and os.path.isdir(test_dir), \
        'test_dir: {0}\nYou need to git clone the repo and run the test'.format(test_dir)
    incar = os.path.join(test_dir, 'INCAR')
    incar_dict = parse_incar(incar)
    preview_parse_incar(incar)
    print(incar_dict)
    preview_output_incar(incar_dict)
    gen_incar(incar_dict, '/tmp')



def cli_add_parser(subparsers):
    """
    potcar add_parser
    """
    subp = subparsers.add_parser(MOD_NAME, help='INCAR')
    subp.add_argument('filename', metavar='PATH', help='INCAR template')


def cli_args_exec(args):
    """
    potcar args_exec
    """
    if args.DEBUG:
        print(__file__)
    if args.test:
        test(args.test_dir)
    else:
        sdict = parse_incar(args.filename, args.basic_parser)
        for key, val in sdict.items():
            if hasattr(val, tolist):
                val = val.tolist()
            print(key, ':', val)
