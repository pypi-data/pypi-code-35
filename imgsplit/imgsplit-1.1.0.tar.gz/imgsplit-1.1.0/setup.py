#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from os.path import join as pjoin

setup(
    name = 'imgsplit',
    version = '1.1.0',
    author = 'David R. Bild',
    author_email = 'david@davidbild.org',
    keywords = 'image embedded firmware binary',
    url = 'https://github.com/drbild/imgsplit',
    description = 'Split an image file into multiple segments by'
                  ' removing runs of null or zero bytes.',
    classifiers = [
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ],
    scripts = [
        pjoin('bin', 'imgsplit')
    ],
    install_requires = [
        'docopt'
    ]
)
