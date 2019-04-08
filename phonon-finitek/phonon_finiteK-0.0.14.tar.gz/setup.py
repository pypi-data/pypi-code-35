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
    name="phonon_finiteK",
    version="0.0.14",
    author="Gabriele Coiana",
    author_email="gabriele.coiana17@imperial.ac.uk",
    description="Finite K phonon package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Coiana/phonon_finiteK",
    packages=['phonon_finiteK'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=['bin/phonon-finiteK'],
)
