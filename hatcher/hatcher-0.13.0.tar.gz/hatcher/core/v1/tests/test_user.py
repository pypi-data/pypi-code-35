#  Copyright (c) 2018, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
from hatcher.testing import unittest
from hatcher.core.tests.v1.base_test_user import BaseTestUser
from .user_responses import BroodResponses
from ..user import User


class TestUserV1(BaseTestUser, unittest.TestCase):

    def setUp(self):
        super(TestUserV1, self).setUp()
        self.user = User(
            'acme', 'user@acme.org', self.url_handler,
            model_registry=self.model_registry)
        self.brood_responses = BroodResponses(self.url_handler, self.user)
