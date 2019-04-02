# -*- coding: utf-8 -*-
"""
Setup file for the spines package.
"""
#
#   Imports
#
from setuptools import setup, find_packages

import versioneer


#
#   Helpers
#

def read(file):
    with open(file, encoding='utf-8') as fin:
        return fin.read()


#
#   Setup
#

setup(
    name='spines',
    description='Skeletons for parameterized models.',
    packages=find_packages(include=['spines', 'spines.*']),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',

    author='Douglas Daly',
    author_email='me@douglasdaly.com',
    url='https://www.github.com/douglasdaly/spines',
    project_urls={
        'Source Code': 'https://www.github.com/douglasdaly/spines',
        'Documentation': 'https://spines.readthedocs.io/',
    },

    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    tests_require=[
        'pytest',
    ],
    include_package_data=True,

    license='MIT',
    keywords="spines parameterized models",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
    ],
)
