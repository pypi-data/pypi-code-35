# -*- coding: utf-8 -*-
"""
Mixin classes for Parameters.
"""
#
#   Imports
#
from operator import gt, lt

from .factories import bound_mixin


#
#   Mixins
#

class Minimum(bound_mixin('minimum', gt)):
    """
    Minimum value bound mixin class

    Attributes
    ----------
    minimum
        Minimum allowed value for this parameter.

    Parameters
    ----------
    minimum : optional
        Minimum allowed value for this parameter.

    """
    pass


class Maximum(bound_mixin('maximum', lt)):
    """
    Maximum value bound mixin class

    Attributes
    ----------
    maximum
        Maximum allowed value for this parameter.

    Parameters
    ----------
    maximum : optional
        Maximum allowed value for this parameter.

    """
    pass
