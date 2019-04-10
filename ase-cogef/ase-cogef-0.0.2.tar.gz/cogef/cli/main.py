# Copyright (C) 2016-2019
# See accompanying license files for details.

import sys
import os
from os.path import abspath, dirname, join, isdir

from ase.utils import import_module, search_current_git_hash
from ase.cli.main import main as ase_main


def print_cogef_info():
    versions = []
    for name in ['cogef']:
        try:
            module = import_module(name)
        except ImportError:
            versions.append((name, 'no'))
        else:
            # Search for git hash
            githash = search_current_git_hash(module)
            if githash is None:
                githash = ''
            else:
                githash = '-{:.10}'.format(githash)
            versions.append((name + '-' + module.__version__ + githash,
                             module.__file__.rsplit(os.sep, 1)[0] + os.sep))

    for a, b in versions:
        print('{:25}{}'.format(a, b))


def main():
    assert (len(sys.argv) == 2 and sys.argv[1] == 'test'), \
        'Command "cogef test" only available.'
    directory = join(dirname(dirname(abspath(__file__))), 'test')
    assert isdir(directory), 'Cannot find test folder: ' + directory
    sys.argv.append(directory)
    print_cogef_info()
    ase_main()
