'''
Command line interface for the vasptools
'''

import argparse
import argcomplete
from .. import version, __all_modules__
from .vasptools_handlers import vasptools_cli_handle_subcmd
from .check import cli_check_normalize_args
from .complete import (cli_case_insensitive_validator,
                       cli_family_completer, 
                       cli_role_completer, 
                       cli_bsname_completer,
                       cli_fmt_completer, 
                       cli_reffmt_completer)

def run_vasptools_cli():
    ################################################################################################
    # NOTE: I am deliberately not using the 'choices' argument in add_argument. I could use it
    # for formats, etc, however I wouldn't want to use it for basis set names. Therefore, I handle
    # all of that manually so that error output is consistent and clean
    ################################################################################################

    ########################################
    # Main global options
    ########################################
    parser = argparse.ArgumentParser(description='VASPTOOLS')
    parser.add_argument('-d', '--basedir', metavar='PATH', default='.', help='test_dir')
    parser.add_argument('-p', '--preview', action='store_true', help='preview')
    parser.add_argument('--basic_parser', action='store_true', help='use basic parser instead of vasprun parser')
    parser.add_argument('-ppath', '--potpath', metavar='PATH', help='set vasppot_path, you could also set env VASPPOT')
    parser.add_argument('-t', '--test', action='store_true', help='run test')
    parser.add_argument('-td', '--test_dir', metavar='PATH', help='test_dir')
    parser.add_argument('-s', '--shell', action='store_true', help='shell mode, exec shell script')
    parser.add_argument('-D', '--DEBUG', action='store_true', help='debug')
    parser.add_argument('-V', action='version', version='vasptools ' + version())
    # parser.add_argument('-o', '--output', metavar='PATH', help='Output to given file rather than stdout')

    subparsers = parser.add_subparsers(metavar='subcommand', dest='subcmd')
    subparsers.required = True # https://bugs.python.org/issue9253#msg186387

    module_map = {}
    for mod in __all_modules__:
        if hasattr(mod, 'cli_add_parser') and hasattr(mod, 'cli_args_exec'):
            mod_name = mod.MOD_NAME
            mod.cli_add_parser(subparsers)
            module_map.update({mod_name: mod})
    subparsers.add_parser('LISTSUBCOMMAND', help='list all sub commands, just for test')

    """
    ########################################
    # INCAR
    ########################################
    subp = subparsers.add_parser('incar', help='INCAR')
    subp.add_argument('incar', metavar='PATH', help='INCAR template')

    ########################################
    # POTCAR
    ########################################
    subp = subparsers.add_parser('potcar', help='POTCAR')
    subp.add_argument('-i', '--input', metavar='PATH', help='Generate POTCAR with POSCAR')
    subp.add_argument('pp_names', nargs='*')

    ########################################
    # POSCAR
    ########################################
    subp = subparsers.add_parser('poscar', help='POSCAR')
    subp.add_argument('-i', '--input', metavar='PATH', help='parse')
    subp.add_argument('poscar', metavar='PATH')
    
    ########################################
    # KPOINTS
    ########################################
    subp = subparsers.add_parser('kpoints', help='KPOINTS')
    subp.add_argument('-i', '--input', metavar='PATH', help='Generate POTCAR with POSCAR')
    subp.add_argument('-g', '--grid', nargs=3, help='set grid number')
    subp.add_argument('ktype', help='kpoint type, Auto')
    
    ########################################
    # OUTCAR
    ########################################
    # list-ref-formats subcommand
    subp = subparsers.add_parser('outcar', help='OUTCAR')
    subp.add_argument('outcar_path', default='OUTCAR')
    

    
    # list-roles subcommand
    subp = subparsers.add_parser('list-roles', help='Output a list all available roles and descriptions')
    subp.add_argument('-n', '--no-description', action='store_true', help='Print only the role names')

    ########################################
    # Listing of general info and metadata
    ########################################
    # get-data-dir
    subparsers.add_parser('get-data-dir', help='Output the default data directory of this package')

    # list-basis-sets subcommand
    subp = subparsers.add_parser('list-basis-sets', help='Output a list all available basis sets and descriptions')
    subp.add_argument('-n', '--no-description', action='store_true', help='Print only the basis set names')
    subp.add_argument('-f', '--family', help='Limit the basis set list to only the specified family').completer = cli_family_completer
    subp.add_argument('-r', '--role', help='Limit the basis set list to only the specified role').completer = cli_role_completer
    subp.add_argument('-s', '--substr', help='Limit the basis set list to only basis sets whose name contains the specified substring')

    # list-families subcommand
    subparsers.add_parser('list-families', help='Output a list all available basis set families')

    # lookup-by-role
    subp = subparsers.add_parser('lookup-by-role', help='Lookup a companion/auxiliary basis by primary basis and role')
    subp.add_argument('basis', help='Name of the primary basis we want the auxiliary basis for').completer = cli_bsname_completer
    subp.add_argument('role', help='Role of the auxiliary basis to look for').completer = cli_role_completer

    #################################
    # Output of info
    #################################
    # get-basis subcommand
    subp = subparsers.add_parser('get-basis', help='Output a formatted basis set')
    subp.add_argument('basis', help='Name of the basis set to output').completer = cli_bsname_completer
    subp.add_argument('fmt', help='Which format to output the basis set as').completer = cli_fmt_completer
    subp.add_argument('--elements', help='Which elements of the basis set to output. Default is all defined in the given basis')
    subp.add_argument('--version', help='Which version of the basis set to output. Default is the latest version')
    subp.add_argument('--noheader', action='store_true', help='Do not output the header at the top')
    subp.add_argument('--unc-gen', action='store_true', help='Remove general contractions')
    subp.add_argument('--unc-spdf', action='store_true', help='Remove combined sp, spd, ... contractions')
    subp.add_argument('--unc-seg', action='store_true', help='Remove general contractions')
    subp.add_argument('--opt-gen', action='store_true', help='Optimize general contractions')
    subp.add_argument('--make-gen', action='store_true', help='Make the basis set as generally-contracted as possible')

    # get-refs subcommand
    subp = subparsers.add_parser('get-refs', help='Output references for a basis set')
    subp.add_argument('basis', help='Name of the basis set to output the references for').completer = cli_bsname_completer
    subp.add_argument('reffmt', help='Which format to output the references as').completer = cli_reffmt_completer
    subp.add_argument('--elements', help='Which elements to output the references for. Default is all defined in the given basis.')
    subp.add_argument('--version', help='Which version of the basis set to get the references for')

    # get-info subcommand
    subp = subparsers.add_parser('get-info', help='Output general info and metadata for a basis set')
    subp.add_argument('basis', help='Name of the basis set to output the info for').completer = cli_bsname_completer

    # get-notes subcommand
    subp = subparsers.add_parser('get-notes', help='Output the notes for a basis set')
    subp.add_argument('basis', help='Name of the basis set to output the notes for').completer = cli_bsname_completer

    # get-family subcommand
    subp = subparsers.add_parser('get-family', help='Output the family of a basis set')
    subp.add_argument('basis', help='Name of the basis set to output the family for').completer = cli_bsname_completer

    # get-versions subcommand
    subp = subparsers.add_parser('get-versions', help='Output a list all available versions of a basis set')
    subp.add_argument('basis', help='Name of the basis set to list the versions of').completer = cli_bsname_completer
    subp.add_argument('-n', '--no-description', action='store_true', help='Print only the version numbers')

    # get-family-notes subcommand
    subp = subparsers.add_parser('get-family-notes', help='Get the notes of a family of basis sets')
    subp.add_argument('family', type=str.lower, help='The basis set family to the get the notes of').completer = cli_family_completer

    #################################
    # Creating bundles
    #################################
    subp = subparsers.add_parser('create-bundle', help='Create a bundle of basis sets')
    subp.add_argument('fmt', help='Which format to output the basis set as').completer = cli_fmt_completer
    subp.add_argument('reffmt', help='Which format to output the references as').completer = cli_reffmt_completer
    subp.add_argument('bundle_file', help='Bundle/Archive file to create')
    subp.add_argument('--archive-type', help='Override the type of archive to create (zip or tbz)')


    #############################
    # DONE WITH SUBCOMMANDS
    #############################
    """
    # setup autocomplete
    argcomplete.autocomplete(parser, validator=cli_case_insensitive_validator)

    # Now parse and handle the args
    args = parser.parse_args()
    if args.DEBUG:
        print(args)
    if args.subcmd == 'LISTSUBCOMMAND':
        print('\n'.join(list(module_map)))
        exit(0)
    # args = cli_check_normalize_args(args)

    # Actually generate the output
    #  output = vasptools_cli_handle_subcmd(args)
    assert args.subcmd in module_map, '{0} not in module_map: {1}'.format(args.subcmd, list(module_map))
    return module_map[args.subcmd].cli_args_exec(args)
