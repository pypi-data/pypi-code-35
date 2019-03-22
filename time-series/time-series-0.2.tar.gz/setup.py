# -*- coding: utf-8 -*-

from os.path import join, dirname
from setuptools import setup, find_packages


def read(fname):
    with open(join(dirname(__file__), fname)) as f:
        return f.read()


setup(
    # Package
    name="time-series",
    version="0.2",
    packages=find_packages(exclude=("tests")),
    url="https://github.com/ani071/timeseries",
    keywords=["window", "time", "series"],
    # Contact
    author="Andreas Isnes Nilsen",
    author_email="andnil94@gmail.com",
    # Description
    description="Python implementation of a sliding window.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
