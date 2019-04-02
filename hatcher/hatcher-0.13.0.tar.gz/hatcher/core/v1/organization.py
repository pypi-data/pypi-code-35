#  Copyright (c) 2013, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
from __future__ import absolute_import

from hatcher.core.url_templates import URLS_V1
from hatcher.core.v0.organization import Organization as OrganizationV0


class Organization(OrganizationV0):
    """A representation of an organization in a Brood server.

       The object will use the V1 entrypoints.

    """

    def __init__(self, name, url_handler, model_registry):
        super(Organization, self).__init__(name, url_handler, model_registry)
        self._urls = URLS_V1  # Make sure that we use the V1 entry points
