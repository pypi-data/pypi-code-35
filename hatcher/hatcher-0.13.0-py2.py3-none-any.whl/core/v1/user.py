#  Copyright (c) 2013, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
from __future__ import absolute_import

from hatcher.core.url_templates import URLS_V1
from hatcher.core.v0.user import User as UserV0


class User(UserV0):

    def __init__(self, organization_name, email, url_handler, model_registry):
        super(User, self).__init__(
            organization_name, email, url_handler, model_registry)
        self._urls = URLS_V1
