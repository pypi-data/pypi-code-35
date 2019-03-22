#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
from path2vec import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requirements = []
setup_requirements = []

setuptools.setup(
    name="path2vec",
    version=__version__,
    author="Christoph Gote",
    author_email="cgote@ethz.ch",
    license='AGPL-3.0+',
    description="An OpenSource Python package for path embedding based on the path2vec algorithm.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/gotec/path2vec',
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent"
    ],
    test_suite='tests',
    keywords='embedding vector path networks network analysis link prediction clustering ' +
	     'node labeling multi order higher order',
    install_requires=install_requirements,
    setup_requires=setup_requirements
)
