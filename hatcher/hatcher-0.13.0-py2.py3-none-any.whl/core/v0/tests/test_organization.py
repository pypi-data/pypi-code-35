#  Copyright (c) 2015, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
from hatcher.testing import unittest
from hatcher.core.tests.v0.base_test_organization import BaseTestOrganization
from .organization_responses import BroodResponses
from ..organization import Organization
from ..repository import Repository
from ..user import User


class TestOrganizationV0(BaseTestOrganization, unittest.TestCase):

    def setUp(self):
        super(TestOrganizationV0, self).setUp()
        self.user_type = User
        self.repository_type = Repository
        self.organization = Organization(
            'acme', url_handler=self.url_handler,
            model_registry=self.model_registry)
        self.brood_responses = BroodResponses(self.url_handler)
