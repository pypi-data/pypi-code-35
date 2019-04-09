# -*- coding: utf-8 -*-

"""
Google Play Store Scraper

An async web scraper for the Google Play Android app store.
"""

__version__ = '0.5.6'

import logging

from playmate.api import PlayMate

# Set default logging handler to avoid "No handler found" warnings.
from logging import NullHandler
logging.getLogger(__name__).addHandler(NullHandler())
