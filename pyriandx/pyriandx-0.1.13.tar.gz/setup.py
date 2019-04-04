# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from pyriandx import __version__, __author__, __title__, __description__

here = os.path.dirname(__file__)

with open(os.path.join(here, 'requirements.txt')) as f:
    deps = f.readlines()

setup(
    name='pyriandx',
    version=__version__,
    description=__description__,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author=__author__,
    url='https://github.com/umccr/pyriandx',
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={'pyriandx': ['json/*.json']},
    install_requires=deps,
    entry_points = {'console_scripts': ['pyriandx=pyriandx.__main__:main']}
)

