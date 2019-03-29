"""A simple package that works in some versions and is broken in others"""

import setuptools


def tweet():
    print("Tweet, tweet!")


def belly_up():
    raise RuntimeError


setuptools.setup(
    name="tox-constraints-canary",
    version="1.0.1",
)

belly_up()
