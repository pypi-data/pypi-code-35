#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs

try:
    codecs.lookup("mbcs")
except LookupError:
    ascii = codecs.lookup("ascii")
    codecs.register(lambda name, enc=ascii: {True: enc}.get(name == "mbcs"))

VERSION = "1.2.4"
URL = "https://github.com/rolik2001/python-dexstore"

setup(
    name="dexstore",
    version=VERSION,
    description="Python library for dexstore",
    long_description=open("README.md").read(),
    download_url="{}/tarball/{}".format(URL, VERSION),
    author="Fabian Schuh",
    author_email="Fabian@chainsquad.com",
    maintainer="Fabian Schuh",
    maintainer_email="Fabian@chainsquad.com",
    url=URL,
    keywords=["dexstore", "library", "api", "rpc"],
    packages=["dexstore", "dexstoreapi", "dexstorebase"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
    ],
    install_requires=open("requirements.txt").readlines(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    include_package_data=True,
)
