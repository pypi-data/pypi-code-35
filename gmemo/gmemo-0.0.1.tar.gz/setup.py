# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import os

from setuptools import setup, find_packages

try:
    import pypandoc
    readme = pypandoc.convert('README.md', 'rst', format='markdown_github')
except (IOError, ImportError):
    readme = read_file('README.md')

def _requires_from_file(filename):
    return open(filename).read().splitlines()

# version
here = os.path.dirname(os.path.abspath(__file__))
version = next((line.split('=')[1].strip().replace("'", '')
                for line in open(os.path.join(here, 'gmemo', '__init__.py'))
                if line.startswith('__version__ = ')),
               '0.0.dev0')

setup(
    name='gmemo',
    version=version,
    url='https://gitlab.com/kegeppa',
    author='kegeppa',
    author_email='',
    maintainer='kegeppa',
    maintainer_email='',
    description='Command line application for global memo.',
    long_description=readme,
    packages=find_packages(),
    install_requires=_requires_from_file('requirements.txt'),
    entry_points={
        'console_scripts': [
            'gmemo=gmemo.__main__:main'
        ]
    },
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
