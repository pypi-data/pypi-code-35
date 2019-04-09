import argparse


def str2bool(v):
    if v.lower() in {'yes', 'true', 't', 'y', '1'}:
        return True
    elif v.lower() in {'no', 'false', 'f', 'n', '0'}:
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def xml_file_args(v):
    if not v.endswith('.xml'):
        raise AssertionError('Provided invalid XML file name {}, should end with ".xml".'.format(v))
    else:
        return v


def get_args(argv=None):
    parser = argparse.ArgumentParser(description='run one of the SSBJ tools')
    parser.add_argument('ssbj_discipline')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--test',
                       action='store_true',
                       help='perform a test run with a standard input XML file')
    group.add_argument('-i', '--in_file',
                       type=xml_file_args,
                       help='perform a run with a provided input XML file')
    parser.add_argument('-o', '--out_file',
                        type=xml_file_args,
                        default='__run__{}_output.xml',
                        help='path to store the output XML file')
    parser.add_argument('-merge-files', '--merge_files',
                        type=str2bool,
                        default=False,
                        help='setting whether to merge input file into the output file')
    return parser.parse_args(argv)
