#!/usr/bin/env python3

from setuptools import setup


with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="ansistrip",
    packages=["ansistrip"],
    version="0.1",
    license="GPL3",
    description="ASCII Screen Splash for SHYCD software.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Carlos A. Planchón",
    author_email="bubbledoloresuruguay2@gmail.com",
    url="https://github.com/carlosplanchon/ansistrip",
    download_url="https://github.com/carlosplanchon/"
        "ansistrip/archive/v0.1.tar.gz",
    keywords=["ascii", "ansi", "strip", "VT100"],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
