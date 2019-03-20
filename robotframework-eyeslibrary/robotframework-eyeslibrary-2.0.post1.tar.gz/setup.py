#!/usr/bin/env python

import sys

# from distutils.core import setup
from setuptools import setup, find_packages
from os import path
import io
from os.path import join, dirname

sys.path.append(join(dirname(__file__), "EyesLibrary"))

execfile("EyesLibrary/version.py")

with io.open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="robotframework-eyeslibrary",
    version=VERSION,
    description="Visual Verification testing library for Robot Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Joel Oliveira, Sofia Nunes",
    author_email="<joel.oliveira@criticalsoftware.com>, <sofia.nunes@criticalsoftware.com>",
    url="https://github.com/joel-oliveira/EyesLibrary",
    license="Apache License 2.0",
    keywords="robotframework testing testautomation eyes-selenium selenium appium visual-verification",
    platforms="any",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Framework :: Robot Framework :: Library",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
    ],
    install_requires=["robotframework >= 3.1.1", "eyes-selenium >= 3.15.2"],
    packages=find_packages(exclude=["tests", "docs"]),
)
