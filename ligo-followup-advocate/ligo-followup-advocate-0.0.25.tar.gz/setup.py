import ast
import sys

import pkg_resources
from setuptools import setup


def get_requirements(filename):
    with open(filename, 'r') as f:
        return [str(r) for r in pkg_resources.parse_requirements(f)]


# Get docstring and version without importing module
with open('ligo/followup_advocate/version.py') as f:
    mod = ast.parse(f.read())
__version__ = mod.body[-1].value.s

setup_requires = ['setuptools >= 30.3.0']
if {'pytest', 'test', 'ptr'}.intersection(sys.argv):
    setup_requires.append('pytest-runner')

setup(install_requires=get_requirements('requirements.txt'),
      setup_requires=setup_requires,
      version=__version__)
