#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages
from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pytz']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Sebastian Schaffer",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Jsoner allows you to easily "
                "convert your classes to json and back.",
    long_description_content_type='text/x-rst',
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='jsoner json celery django serialization',
    name='jsoner',
    packages=find_packages(include=['jsoner']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/sschaffer92/jsoner',
    version='0.2.0',
    zip_safe=False,
    python_requires='>=3.4',
    project_urls={
        'Documentation': 'https://jsoner.readthedocs.io/en/latest/',
        'Source': 'https://github.com/sschaffer92/jsoner/',
        'Tracker': 'https://github.com/sschaffer92/jsoner/issues',
    },
)
