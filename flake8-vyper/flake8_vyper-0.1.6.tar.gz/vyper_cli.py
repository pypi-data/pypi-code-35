"""Command-line implementation of flake8 with some tinkering for vyper."""
import sys
from typing import List, Optional

from flake8.main import application
from flake8.processor import PyCF_ONLY_AST, FileProcessor

from vyper.parser.pre_parser import pre_parse

__author__ = 'Mike Shultz'
__email__ = 'mike@mikeshultz.com'
__version__ = '0.1.6'

VYPER_BUILTINS = [
    'address', 'bytes1', 'bytes128', 'bytes16', 'bytes2', 'bytes256', 'bytes32', 'bytes4',
    'bytes64', 'bytes8', 'constant', 'decimal', 'int1', 'int128', 'int16', 'int2', 'int256',
    'int32', 'int4', 'int64', 'int8', 'modifying', 'msg', 'private', 'public', 'self', 'string',
    'timedelta', 'timestamp', 'uint1', 'uint128', 'uint16', 'uint2', 'uint256', 'uint32', 'uint4',
    'uint64', 'uint8', 'wei_value'
]


def find(val, it):
    """ Find the index of a value in an iterator """
    for i in range(0, len(it)):
        if val == it[i]:
            return i
    return -1


def patch_processor(processor):
    """ Patch FileProcessor to use the Vyper AST pre-processor """

    def build_ast(self):
        """Build an abstract syntax tree from the list of lines."""
        source_code = "".join(self.lines)
        _, reformatted_code = pre_parse(source_code)
        return compile(reformatted_code, "", "exec", PyCF_ONLY_AST)

    processor.build_ast = build_ast


def add_vyper_builtins_to_argv(argv):
    """ Inject --builtins with the vyper builtins into argv """
    argv = (argv if argv is not None else sys.argv)[:]
    if '--builtins' in argv:
        idx = find('--builtins', argv)
        argv[idx+1] = argv[idx+1] + ',' + ','.join(VYPER_BUILTINS)
    else:
        argv.append('--builtins')
        argv.append(','.join(VYPER_BUILTINS))
    return argv


def add_vyper_filename_to_argv(argv):
    """ Inject --builtins with the vyper builtins into argv """
    argv = (argv if argv is not None else sys.argv)[:]
    if '--filename' not in argv:
        argv.append('--filename')
        argv.append('*.vy')
    return argv


def main(argv=None):
    # type: (Optional[List[str]]) -> None
    """Execute the main bit of the application.

    This handles the creation of an instance of :class:`Application`, runs it,
    and then exits the application.

    :param list argv:
        The arguments to be passed to the application for parsing.
    """
    patch_processor(FileProcessor)
    app = application.Application()
    app.run(add_vyper_filename_to_argv(add_vyper_builtins_to_argv(argv)))
    app.exit()
