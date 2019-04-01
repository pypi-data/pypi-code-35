#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('./src/gosdk/README.md') as readme_file:
    readme = readme_file.read()

history = ""

tests_require = [
    "pytest-flake8 >= 1.0.2",
    "black >= 18.5b1",
    "ipython >= 6.4.0",
    "pytest >= 3.6.0",
    "pytest-cov >= 2.5.1",
    "pytest-mccabe >= 0.1",
    "white >= 0.1.2",
    "pytest-socket >= 0.2.0",
    "pytest-asyncio >= 0.8.0",
    "aioconsole >= 0.1.8",
    "addict >= 2.1.3",
]

setup(
    name="gosdk",
    version='0.8.18',
    author="Ian Maurer",
    author_email='ian@genomoncology.com',

    packages=[
        "gosdk",
    ],
    package_dir={
        '': 'src'
    },

    package_data={
        '': ["*.yaml", "*.bed", "*.txt", "*.tsv", "*.csv"]
    },

    include_package_data=True,

    tests_require=tests_require,

    install_requires=[
        "specd >= 0.8.1",
        "backoff >= 1.5.0",
        "structlog >= 18.1.0",
        "flask == 1.0.2",
    ],

    setup_requires=[
        'pytest-runner',
    ],

    license="Proprietary",
    keywords='Bioinformatics HGVS VCF Clinical Trials Genomics',

    description="gosdk",
    long_description="%s\n\n%s" % (readme, history),

    entry_points={
    },

    classifiers=[
        'License :: Other/Proprietary License',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
)
