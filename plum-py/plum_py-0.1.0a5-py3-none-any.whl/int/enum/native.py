# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Native endian integer enumeration types."""

import sys

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
if sys.byteorder == 'little':
    from .little import *
else:
    from .big import *
