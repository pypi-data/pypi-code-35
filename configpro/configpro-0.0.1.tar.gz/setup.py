#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

name = 'configpro'
description = 'High Performance Distributed Config Manager'
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=name,  # Required
    version='0.0.1',  # Required
    description=description,  # Optional
    long_description=long_description,  # Optional

    # valid values are: text/plain, text/x-rst, and text/markdown
    long_description_content_type='text/markdown',  # Optional (see note above)

    url='https://github.com/zioniony/{}'.format(name),  # Optional

    author='Zion',  # Optional

    # author_email='',  # Optional

    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # These classifiers are *not* checked by 'pip install'. See instead
        # 'python_requires' below.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='{} development'.format(name),  # Optional

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'examples']),  # Required

    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',

    install_requires=['redis', 'watchdog', 'PyYAML'],  # Optional

    extras_require={  # Optional
        'dev': ['jedi'],
        'test': ['coverage'],
    },

    entry_points={  # Optional
        'console_scripts': [
            '{proj}={proj}:main'.format(proj=name),
        ],
    },

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/zioniony/{}/issues'.format(name),
        'Funding': 'https://donate.pypi.org',
        'Source': 'https://github.com/zioniony/{}'.format(name),
    },
)
