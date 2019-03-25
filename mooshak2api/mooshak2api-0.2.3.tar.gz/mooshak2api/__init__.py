"""Mooshak2api - A Python API for interacting with the Mooshak 2 REST API"""

import mooshak2api.contests
import mooshak2api.problems
from .client import login

__version__ = '0.2.3'
__author__ = 'Aaron Walker <aaw13@aber.ac.uk>'
__all__ = [contests, problems, login]

if __name__ == '__main__':
    pass
