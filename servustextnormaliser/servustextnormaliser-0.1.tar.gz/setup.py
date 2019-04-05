#!/usr/bin/env python3

from setuptools import setup


with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="servustextnormaliser",
    packages=["servustextnormaliser"],
    version="0.1",
    license="GPL3",
    description="Python3 module to normalise text.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Carlos A. Planchón",
    author_email="bubbledoloresuruguay2@gmail.com",
    url="https://github.com/carlosplanchon/servustextnormaliser",
    download_url="https://github.com/carlosplanchon/"
        "servustextnormaliser/archive/v0.1.tar.gz",
    keywords=["normalise", "text", "regex"],
    install_requires=[
        "removeurl",
        "removeaccents",
        "servussimplifytext",
        "contractions"
    ],
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
