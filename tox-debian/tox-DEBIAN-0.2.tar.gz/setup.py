# Copyright (c) 2015 BalaBit
# All Rights Reserved.

from setuptools import setup

setup(
    name='tox-DEBIAN',
    description='debian package installer tox plugin',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license="MIT license",
    version='0.2',
    packages=['tox_DEBIAN'],
    entry_points={'tox': ['DEBIAN = tox_DEBIAN']},
    install_requires=['tox>=3.0, <3.9'],
    python_requires='~=3.5',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: tox',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Testing',
    ],
)
