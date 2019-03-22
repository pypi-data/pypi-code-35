"""Command-line implementation of flake8 with some tinkering for vyper."""
import sys
from typing import List, Optional

from flake8.main import application, options
from flake8.processor import PyCF_ONLY_AST, FileProcessor
from flake8.options import manager

from vyper.functions.functions import dispatch_table, stmt_dispatch_table
from vyper.utils import (
    base_types,
    valid_global_keywords,
    reserved_words,
    function_whitelist,
    valid_lll_macros,
)
from vyper.parser.pre_parser import pre_parse

__author__ = 'Mike Shultz'
__email__ = 'mike@mikeshultz.com'
__version__ = '0.1.10'

VYPER_BUILTINS = set(dispatch_table.keys())
VYPER_BUILTINS.update(stmt_dispatch_table.keys())
VYPER_BUILTINS.update(base_types)
VYPER_BUILTINS.update(valid_global_keywords)
VYPER_BUILTINS.update(reserved_words)
VYPER_BUILTINS.update(function_whitelist)
VYPER_BUILTINS.update(valid_lll_macros)
# Missing from vyper internals?
# https://github.com/ethereum/vyper/issues/1364
VYPER_BUILTINS.update({'msg'})


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
