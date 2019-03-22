# pkgdata.py
# Copyright (c) 2013-2019 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0111

# Standard library imports
import os


###
# Global variables
###
VERSION_INFO = (1, 1, 3, "final", 0)
SUPPORTED_INTERPS = ["2.7", "3.5", "3.6", "3.7"]
COPYRIGHT_START = 2013
PKG_DESC = "Automatically generate exceptions documentation in reStructuredText"
COV_EXCLUDE_FILES = ["{PKG_NAME}/pit.py"]
PKG_LONG_DESC = (
    "This package provides a light framework that can be used to automatically "
    + "generate exceptions documentation marked up in "
    + "`reStructuredText <http://docutils.sourceforge.net/rst.html>`_."
    + os.linesep
    + os.linesep
    + "The exdoc module details how to register exceptions, how to "
    + "traced them and how to generate their documentation"
    + os.linesep
)
PKG_PIPELINE_ID = 5

###
# Functions
###
def _make_version(major, minor, micro, level, serial):
    """Generate version string from tuple (almost entirely from coveragepy)."""
    level_dict = {"alpha": "a", "beta": "b", "candidate": "rc", "final": ""}
    if level not in level_dict:
        raise RuntimeError("Invalid release level")
    version = "{0:d}.{1:d}".format(major, minor)
    if micro:
        version += ".{0:d}".format(micro)
    if level != "final":
        version += "{0}{1:d}".format(level_dict[level], serial)
    return version


__version__ = _make_version(*VERSION_INFO)
