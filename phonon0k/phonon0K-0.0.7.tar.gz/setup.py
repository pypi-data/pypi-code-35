#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 16:09:35 2019

@author: Gabriele Coiana
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="phonon0K",
    version="0.0.7",
    author="Gabriele Coiana",
    author_email="gabriele.coiana17@imperial.ac.uk",
    description="Harmonic phonon package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Coiana/phonon0K",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=['bin/phonon0K'],
)
