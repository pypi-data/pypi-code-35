#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requires = [
    'setuptools'
]


setup_requirements = ['pytest-runner', ]

tests_require = ['pytest',
                'pytest-cov' ]

setup(
    author="Rainer Bruggemann",
    author_email='rainer.bruggemann@pyhasse.org',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    description="pyhasse.core: Basics of partial order aiming at data analysis.",
    install_requires=requires,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='core',
    packages=['pyhasse',
              'pyhasse.core'],
    namespace_packages=['pyhasse'],
    name='pyhasse.core',
    package_dir={'': 'src'},
    setup_requires=setup_requirements,
    test_suite='tests',
    extras_require={
        'testing': tests_require,
    },
    url='https://pyhasse.org',
    download_url='https://bitbucket.org/pyhasse/core/src/default/',
    version='0.1.7',
    zip_safe=False,
)
