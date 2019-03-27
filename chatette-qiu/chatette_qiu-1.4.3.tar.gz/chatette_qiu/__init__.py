#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module `chatette_qiu`
A generator of example sentences based on templates.
"""

# Retrieve the version number using setuptools
import pkg_resources
try:
    __version__ = pkg_resources.require("chatette_qiu")[0].version
except pkg_resources.DistributionNotFound:
    __version__ = "<couldn't retrieve version number>"  # TODO: find another way
