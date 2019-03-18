#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for senergy.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 3.1.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
from glob import glob
from os.path import basename, splitext

from setuptools import find_packages
from setuptools import setup

def readme(filename):
    """Read README contents
    """
    with open(filename) as f:
        return f.read()

setup(
    name='senergy',
    #version='0.1.2',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    license='MIT License',
    description='description',
    long_description=readme('README.rst'),
    long_description_content_type="text/markdown",
    author='Sven Eggimann',
    author_email='sven.eggimann@gmail.com',
    url='https://github.com/eggimasv/senergy',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Utilities',
    ],
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    install_requires=[
        #'fiona>=1.7.13',
        #'shapely>=1.6',
        #'geopandas==0.4.0',
        #'rtree>=0.8'
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    entry_points={
        'console_scripts': [
            # eg: 'snkit = snkit.cli:main',
        ]
    },
)