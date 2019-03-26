#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# System modules
import os
import runpy
from setuptools import setup, find_packages


def read_file(filename):
    with open(filename) as f:
        return f.read()


package = find_packages(exclude=["tests"])[0]

# run setup
setup(
    name=package,
    description="simple HTTP server for CO2 data logging",
    author="Yann Büchau",
    author_email="nobodyinperson@gmx.de",
    keywords="measurement,logging",
    license="GPLv3",
    version=runpy.run_path(os.path.join(package, "version.py")).get(
        "__version__", "0.0.0"
    ),
    url="https://gitlab.com/tue-umphy/co2mofetten/python3-co2logserver",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    package_data={"co2logserver.templates": ["*.html"]},
    include_package_data=True,
    install_requires=["flask"],
    extras_require={
        "opensensemap": ["sensemapi[cache]>=0.0.11", "pandas"],
        "msgpack": ["msgpack"],
    },
    tests_require=["flask", "sensemapi[cache]>=0.0.11", "msgpack"],
    test_suite="tests",
    packages=find_packages(exclude=["tests"]),
)
