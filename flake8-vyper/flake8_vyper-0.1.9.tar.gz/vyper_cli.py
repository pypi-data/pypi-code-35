"""Command-line implementation of flake8 with some tinkering for vyper."""
import sys
from typing import List, Optional

from flake8.main import application, options
from flake8.processor import PyCF_ONLY_AST, FileProcessor
from flake8.options import manager

from vyper.parser.pre_parser import pre_parse

__author__ = 'Mike Shultz'
__email__ = 'mike@mikeshultz.com'
__version__ = '0.1.9'

BIT_LENGTHS = ['256', '128', '64', '32', '16', '8', '4', '2', '1']
TYPES_WITH_LENGTHS = ['bytes', 'uint', 'int']
TYPES_WITHOUT = ['address', 'string', 'decimal', 'wei_value', 'timestamp', 'timedelta']
OTHER_BUILTINS = ['self', 'msg', 'constant', 'modifying', 'private', 'public']
VYPER_BUILTINS = [
    '{}{}'.format(t, l) for l in BIT_LENGTHS for t in TYPES_WITH_LENGTHS
] + TYPES_WITHOUT + OTHER_BUILTINS


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


def patch_app_option_manager(app):
    """ Patch Application an option_manager with a different name (and config) """
    app.option_manager = manager.OptionManager(
        prog="flake8-vyper",
        version=__version__,
    )
    options.register_default_options(app.option_manager)


def add_vyper_builtins_to_argv(argv):
    """ Inject --builtins with the vyper builtins into argv """
    argv = (argv if argv is not None else sys.argv)[:]
    if '--builtins' in argv:
        idx = find('--builtins', argv)
        if idx > -1 and '=' in argv[idx]:
            parts = argv[idx].split('=')
            values = parts[1].split(',')
            argv = '{}={}'.format(parts[0], ','.join(list(values + VYPER_BUILTINS)))
    else:
        argv.append('--builtins=' + ','.join(VYPER_BUILTINS))
    return argv


def or_sys_argv(argv):
    return (argv if argv is not None else sys.argv[1:])


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
    patch_app_option_manager(app)
    app.run(add_vyper_builtins_to_argv(or_sys_argv(argv)))
    app.exit()
