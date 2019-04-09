import io
import os
import re

from setuptools import find_packages
from setuptools import setup


with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name="csj_parser",
    version="0.0.2",
    url="https://github.com/Proteus-tech/csj-parser",
    license='MIT',

    author="HotNow",
    author_email="admin@hot-now.com",

    description="CSJ for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",

    packages=find_packages(exclude=('tests',)),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
