#!/usr/bin/python

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="easylogconfig",
    version="0.1.2",
    description="Easy configure logging",
    url="https://github.com/tierpod/easylogconfig",
    author="Pavel Podkorytov",
    author_email="pod.pavel@gmail.com",
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
)
