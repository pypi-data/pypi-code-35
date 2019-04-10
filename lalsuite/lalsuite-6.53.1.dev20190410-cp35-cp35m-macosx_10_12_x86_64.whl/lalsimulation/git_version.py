# -*- coding: utf-8 -*-
# git_version.py - vcs information module
#
# Copyright (C) 2010 Nickolas Fotopoulos
# Copyright (C) 2012-2013 Adam Mercer
# Copyright (C) 2016 Leo Singer
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with with program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307 USA

id = "5991066a048f52017091beefe0d5a9a638b21b4a"
date = "2019-04-10 06:31:45 +0000"
branch = "None"
tag = "None"
if tag == "None":
    tag = None
author = "Carl-Johan Haster <carl-johan.haster@ligo.org>"
builder = "Unknown User <>"
committer = "Carl-Johan Haster <carl-johan.haster@ligo.org>"
status = "CLEAN: All modifications committed"
version = id
verbose_msg = """Branch: None
Tag: None
Id: 5991066a048f52017091beefe0d5a9a638b21b4a

Builder: Unknown User <>
Repository status: CLEAN: All modifications committed"""

import warnings

class VersionMismatchError(ValueError):
    pass

def check_match(foreign_id, onmismatch="raise"):
    """
    If foreign_id != id, perform an action specified by the onmismatch
    kwarg. This can be useful for validating input files.

    onmismatch actions:
      "raise": raise a VersionMismatchError, stating both versions involved
      "warn": emit a warning, stating both versions involved
    """
    if onmismatch not in ("raise", "warn"):
        raise ValueError(onmismatch + " is an unrecognized value of onmismatch")
    if foreign_id == "5991066a048f52017091beefe0d5a9a638b21b4a":
        return
    msg = "Program id (5991066a048f52017091beefe0d5a9a638b21b4a) does not match given id (%s)." % foreign_id
    if onmismatch == "raise":
        raise VersionMismatchError(msg)

    # in the backtrace, show calling code
    warnings.warn(msg, UserWarning)
