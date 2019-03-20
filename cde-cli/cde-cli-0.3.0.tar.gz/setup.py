#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()


# TODO
requirements = [
    'GitPython',
    "Click>=6.0",
    "ruamel.yaml",
    "docker",
    "dockerpty",
]
test_requirements = []

setup(
    name='cde-cli',
    version='0.3.0',
    description="cli helper",
    long_description=readme,
    author="Florian Ludwig",
    author_email='f.ludwig@greyrook.com',
    url='https://github.com/FlorianLudwig/cde',
    packages=find_packages(include=['cde']),
    entry_points={
        'console_scripts': [
            'cde=cde.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='cde',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
