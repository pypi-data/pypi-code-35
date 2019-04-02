"""
To be implemented.
"""
from __future__ import absolute_import
from __future__ import print_function
from unittest.mock import patch
from noaa_sdk import noaa
import pytest

try:
    from unittest.mock import MagicMock
except:
    from mock import MagicMock
