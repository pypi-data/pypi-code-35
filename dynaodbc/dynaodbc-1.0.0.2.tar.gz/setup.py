from __future__ import print_function
import setuptools

import os
import shutil
import subprocess
import sys

from setuptools import setup, find_packages

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name="dynaodbc",
    version="1.0.0.2",
    author="Dynactionize NV",
    author_email="info-belgium@dynationize.com",
    description="Python ODBC connector for the Dynizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dynactionize/Dyna-ODBC",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pyodbc",
        "dynapython",
    ],
    python_requires="~=3.6",
)