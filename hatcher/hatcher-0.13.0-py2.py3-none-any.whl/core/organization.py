#  Copyright (c) 2013-2015, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
import warnings

warnings.warn(
    "hatcher.core.organization has moved to hatcher.core.v0.organization",
    DeprecationWarning)

from .v0.organization import Organization as BaseOrganization
from .model_registry import ModelRegistry


class Organization(BaseOrganization):

    def __init__(self, name, url_handler):
        super(Organization, self).__init__(
            name, url_handler, ModelRegistry(api_version=0))
