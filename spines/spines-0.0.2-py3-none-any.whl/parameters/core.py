# -*- coding: utf-8 -*-
"""
Parameter option classes for use in models.
"""
#
#   Imports
#
from .base import Parameter
from . import mixins


#
#   Parameter classes
#

class BoundedParameter(mixins.Minimum, mixins.Maximum, Parameter):
    """
    Bounded parameter (min/max)
    """
    pass
