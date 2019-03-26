#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")
    ) as fh:
        return fh.read()


setup(
    name="selenium-elements",
    version="0.0.2",
    license="BSD 2-Clause License",
    description="Page object model made easy.",
    long_description=re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub(
        "", read("README.rst")
    ),
    author="Dan Claudiu Pop",
    author_email="danclaudiupop@gmail.com",
    url="https://github.com/danclaudiupop/selenium_elements",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
    ],
    keywords=["selenium", "tests", "page model"],
    python_requires=">=3.7",
    install_requires=["selenium"],
    extras_require={},
)
