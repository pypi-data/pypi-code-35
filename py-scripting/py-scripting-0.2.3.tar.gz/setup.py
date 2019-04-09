#! /usr/bin/env python
from setuptools import setup, find_packages

import versioneer


def read_requirements():
    import os

    path = os.path.dirname(os.path.abspath(__file__))
    requirements_file = os.path.join(path, "requirements.txt")
    try:
        with open(requirements_file, "r") as req_fp:
            requires = req_fp.read().split()
    except IOError:
        return []
    else:
        return [require.split() for require in requires]


setup(
    name="py-scripting",
    version=versioneer.get_version(),
    description="Python utilities for scripting",
    author="Eric Hutton",
    author_email="huttone@colorado.edu",
    url="http://csdms.colorado.edu",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    install_requires=read_requirements(),
    setup_requires=["setuptools"],
    packages=find_packages(),
    cmdclass=versioneer.get_cmdclass(),
)
