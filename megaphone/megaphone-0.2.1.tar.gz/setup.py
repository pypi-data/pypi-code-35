#!/usr/bin/env python
from setuptools import setup, find_packages
import megaphone

setup(
    name="megaphone",
    version=megaphone.__version__,
    description="Connect to the megaphone.fm API",
    author="Brian Muller",
    author_email="bmuller@theatlantic.com",
    license="MIT",
    url="http://github.com/theatlantic/megaphone",
    packages=find_packages(),
    install_requires=["requests>~2.19.1", "yarl>~1.2.6"]
)
