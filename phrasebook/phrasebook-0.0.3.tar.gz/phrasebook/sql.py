#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 3/20/19 by Pat Blair
"""
.. currentmodule:: phrasebook.sql
.. moduleauthor:: Pat Blair <pblair@geo-comm.com>

SQL phrases (y'know... like queries and query fragments and such...)
"""
from pathlib import Path
from typing import Iterable
from .phrasebook import Phrasebook


class SqlPhrasebook(Phrasebook):
    """
    A SQL phrasebook is an indexed collection of string templates that is
    particular to SQL phrases.
    """
    def __init__(
            self,
            path: str or Path = None,
            suffixes: Iterable[str] = ('.sql',)
    ):
        """

        :param path: the path to the phrases directory, or a file that has an
            accompanying phrasebook directory
        :param suffixes: the suffixes of phrase files

        .. seealso::

            `Python's String Templates <https://bit.ly/2FdnQ61>`_
        """
        super().__init__(
            path=self._resolve_path(path),
            suffixes=suffixes
        )
