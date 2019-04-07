"""
Setup.py for npm-audit-checker
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name="npm-audit-checker",
    version="0.0.1",
    description="",
    long_description="A CLI to check the output of npm audit and fail based on threshold",
    url="https://github.com/danielwhatmuff/npm-audit-checker",
    author="Daniel Whatmuff",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="npm audit yarn vulnerability severity security checker",
    py_modules=["npm-audit-checker"],
    scripts=["bin/npm-audit-checker"],
)
