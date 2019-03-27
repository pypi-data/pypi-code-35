#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'sqlalchemy', 'tabulate', 'python-dateutil', 'configparser', 'pylatex', 'num2words']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Luca Parolari",
    author_email='luca.parolari23@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="WPC is a light-weight, highly configurable and easy to use library with a minimal CLI, with the "
                "objective of manage your work (hours and costs) and emit invoices.",
    entry_points={
        'console_scripts': [
            'wpc=wpc.shell_cli:shell.cli_commands',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='wpc',
    name='wpc',
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/lparolari/wpc',
    version='0.2.1',
    zip_safe=False,
)
