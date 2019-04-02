#  Copyright (c) 2013-2015, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
import warnings

warnings.warn(
    "hatcher.core.user has moved to hatcher.core.v0.user",
    DeprecationWarning)

from hatcher.core.v0.user import User


__all__ = ['User']
