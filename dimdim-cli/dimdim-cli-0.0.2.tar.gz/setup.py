#!/usr/bin/env python
from setuptools import setup, find_packages

from dimdim_cli import __version__

# Package meta-data.
NAME = 'dimdim-cli'
DESCRIPTION = 'DimDim Backend team CLI.'
URL = 'https://dimdim.com.ua/dimdim-cli/'
EMAIL = 's.berebko@wrenchtech.io'
AUTHOR = 'Serhii Berebko'
REQUIRES_PYTHON = '>=3.5.2'
VERSION = __version__
REQUIRED = [
    'requests>=2.21,<3.0'
]
EXTRAS = {}
with open('README.md') as f:
    long_description = f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    entry_points={
        'console_scripts': ['dimdim_cli=dimdim_cli.increment:main'],
    },
    keywords='dimdim gitlab styleguide',
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='BSD-3-Clause License',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    zip_safe=False
)
