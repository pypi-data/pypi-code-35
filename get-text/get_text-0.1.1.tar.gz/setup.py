#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'requests', 'beautifulsoup4', 'Jinja2', 'urllib3',
                'PyYAML']

setup_requirements = []

test_requirements = []

setup(
    author="Melis",
    author_email='melis.zhoroev+python@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Test loader with news sites",
    entry_points={
        'console_scripts': [
            'get_text=get_text.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='get_text',
    name='get_text',
    packages=find_packages(include=['get_text',
                                    'get_text.core',
                                    'get_text.core.config',
                                    'get_text.helper'
                                    ]),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/NMelis/get_text',
    version='0.1.1',
    zip_safe=False,
)
