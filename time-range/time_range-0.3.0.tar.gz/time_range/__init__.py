# -*- coding: utf-8 -*-

"""Top-level package for Time range."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

__author__ = """Christopher Tunnell"""
__email__ = 'christopher.douglas.tunnell@gmail.com'
__version__ = '0.3.0'

from .time_range import get_working_days, time_distribution
from .time_range import fraction_of_year, time_distribution_raw
from .time_range import form_2555_data
