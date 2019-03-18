#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = ["pandas"]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest"]

setup(
    author="Henric Sundberg",
    author_email="henric.sundberg@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Neat Panda contains functions written to mimic the R package Tidyr.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="neat_panda",
    name="neat_panda",
    packages=find_packages(include=["neat_panda"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/htp84/neat_panda",
    version="0.1.0",
    zip_safe=False,
)
