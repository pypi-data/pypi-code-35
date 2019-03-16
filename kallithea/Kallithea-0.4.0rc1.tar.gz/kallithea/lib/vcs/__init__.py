# -*- coding: utf-8 -*-
"""
    vcs
    ~~~

    Various version Control System (vcs) management abstraction layer for
    Python.

    :created_on: Apr 8, 2010
    :copyright: (c) 2010-2011 by Marcin Kuzminski, Lukasz Balcerzak.
"""

VERSION = (0, 5, 0, 'dev')

__version__ = '.'.join((str(each) for each in VERSION[:4]))

__all__ = [
    'get_version', 'get_repo', 'get_backend',
    'VCSError', 'RepositoryError', 'ChangesetError'
]

import sys
from kallithea.lib.vcs.backends import get_repo, get_backend
from kallithea.lib.vcs.exceptions import VCSError, RepositoryError, ChangesetError


def get_version():
    """
    Returns shorter version (digit parts only) as string.
    """
    return '.'.join((str(each) for each in VERSION[:3]))
