# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import doctest
import os

import pytest

docfiles = []

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for subdir in ['docs', 'plum', 'plum_c']:
    for dirpath, dirnames, filenames in os.walk(os.path.join(root, subdir)):
        docfiles += [
            os.path.relpath(os.path.join(dirpath, name))
            for name in filenames if os.path.splitext(name)[1] in {'.rst', '.py'}]

for path in docfiles:
    print(path)

OPTION_FLAGS = doctest.ELLIPSIS | doctest.IGNORE_EXCEPTION_DETAIL

@pytest.mark.parametrize('docfile', docfiles)
def test_examples(docfile):
    """Test interactive examples in documentation file.

    :param str docfile: path of RST file

    """
    IGNORE = {
        'about.rst',  # contains examples of future functionality
        '.tox',  # do not test examples from 3rd-party packages

    }
    if not any([ignore_path in docfile for ignore_path in IGNORE]):
        failure_count, _test_count = doctest.testfile(docfile, optionflags=OPTION_FLAGS)
        print(docfile, failure_count, _test_count)
        assert failure_count == 0
