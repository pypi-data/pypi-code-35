# pkgdata.py
# Copyright (c) 2013-2019 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0111

# Standard library imports
import os


###
# Global variables
###
VERSION_INFO = (1, 0, 8, "final", 0)
SUPPORTED_INTERPS = ["2.7", "3.5", "3.6", "3.7"]
COPYRIGHT_START = 2013
PKG_DESC = (
    "This module can be used to handle comma-separated values (CSV) files and do"
    "lightweight processing of their data with support for row and column"
    "filtering. In addition to basic read, write and data replacement, files"
    "can be concatenated, merged, and sorted"
)
PKG_LONG_DESC = (
    "This module can be used to handle comma-separated values (CSV) files and do "
    + "lightweight processing of their data with support for row and column "
    + "filtering. In addition to basic read, write and data replacement, files "
    + "can be concatenated, merged, and sorted"
    + os.linesep
    + os.linesep
    + "Examples"
    + os.linesep
    + "--------"
    + os.linesep
    + os.linesep
    + "Read/write"
    + os.linesep
    + "^^^^^^^^^^"
    + os.linesep
    + os.linesep
    + ".. literalinclude:: ./support/pcsv_example_1.py"
    + os.linesep
    + "    :language: python"
    + os.linesep
    + "    :tab-width: 4"
    + os.linesep
    + "    :lines: 1,6-"
    + os.linesep
    + os.linesep
    + "Replace data"
    + os.linesep
    + "^^^^^^^^^^^^"
    + os.linesep
    + os.linesep
    + ".. literalinclude:: ./support/pcsv_example_2.py"
    + os.linesep
    + "    :language: python"
    + os.linesep
    + "    :tab-width: 4"
    + os.linesep
    + "    :lines: 1,6-"
    + os.linesep
    + os.linesep
    + "Concatenate two files"
    + os.linesep
    + "^^^^^^^^^^^^^^^^^^^^^"
    + os.linesep
    + os.linesep
    + ".. literalinclude:: ./support/pcsv_example_3.py"
    + os.linesep
    + "    :language: python"
    + os.linesep
    + "    :tab-width: 4"
    + os.linesep
    + "    :lines: 1,6-"
    + os.linesep
    + os.linesep
    + "Merge two files"
    + os.linesep
    + "^^^^^^^^^^^^^^^"
    + os.linesep
    + os.linesep
    + ".. literalinclude:: ./support/pcsv_example_4.py"
    + os.linesep
    + "    :language: python"
    + os.linesep
    + "    :tab-width: 4"
    + os.linesep
    + "    :lines: 1,6-"
    + os.linesep
    + os.linesep
    + "Sort a file"
    + os.linesep
    + "^^^^^^^^^^^"
    + os.linesep
    + os.linesep
    + ".. literalinclude:: ./support/pcsv_example_5.py"
    + os.linesep
    + "    :language: python"
    + os.linesep
    + "    :tab-width: 4"
    + os.linesep
    + "    :lines: 1,6-"
    + os.linesep
)
PKG_PIPELINE_ID = 7
PKG_SUBMODULES = [
    "concatenate",
    "csv_file",
    "dsort",
    "merge",
    "ptypes",
    "replace",
    "write",
]


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
