#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['alphatwirl', 'Click>=6.0', 'jinja2', 'pandas', 'pyyaml', 'rootpy', 'root_numpy']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="F.A.S.T",
    author_email='fast-hep@cern.ch',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="F.A.S.T. datacard creation package",
    entry_points={
        'console_scripts': [
            'fast_datacard=fast_datacard.cli:main',
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='fast,datacard',
    name='fast-datacard',
    packages=find_packages(include=['fast_datacard']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitlab.cern.ch/fast-hep/public/fast-datacard',
    version='0.1.3',
    zip_safe=False,
)
