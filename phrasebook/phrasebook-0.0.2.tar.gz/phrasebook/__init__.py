#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: phrasebook
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Store phrases (SQL, messages, what-have-you) alongside your modules.
"""
from .phrasebook import Phrasebook
from .sql import SqlPhrasebook
from .version import __version__, __release__
