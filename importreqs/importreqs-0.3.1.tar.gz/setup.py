#!/usr/bin/env python
from importreqs import __VERSION__

long_description = ""

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except:
    pass

sdict = {
    'name': 'importreqs',
    'version': __VERSION__,
    'packages': ['importreqs'],
    'zip_safe': False,
    'install_requires': ['pip'],
    'author': 'the AUTHORS of importreqs',
    'long_description': long_description,
    'url': 'https://github.com/gstianfu/importreqs',
    'entry_points': {
        'console_scripts': [
            'importreqs=importreqs.cli:main',
        ]
    },
    'classifiers': [
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python']
}

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if __name__ == '__main__':
    setup(**sdict)
