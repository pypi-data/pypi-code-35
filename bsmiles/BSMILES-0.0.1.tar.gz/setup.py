#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 15:04:11 2019

@author: lu
"""

from setuptools import setup,find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="BSMILES",
      version="0.0.1",
      author="lu",
      author_email="lu@gmail.com",
      description="transformation between smiles and bsmiles",
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages(),
      url = "https://github.com/LUJUANJUAN/BSMILES",
      classifiers=[
              "Programming Language :: Python :: 3",
              "License :: OSI Approved :: MIT License",
              "Operating System :: OS Independent",
              ],)