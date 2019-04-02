#  Copyright (c) 2018, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
from hatcher.core.url_templates import URLS_V1
from hatcher.core.tests.v0.base_test_user import BaseTestUser as BaseTestUserV0


class BaseTestUser(BaseTestUserV0):

    api_version = 1
    urls = URLS_V1
