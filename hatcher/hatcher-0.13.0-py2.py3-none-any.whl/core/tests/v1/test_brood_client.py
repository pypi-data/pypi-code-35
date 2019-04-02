#  Copyright (c) 2017, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
from hatcher.testing import unittest
from hatcher.core.v0.organization import Organization
from hatcher.core.tests.base_test_brood_client import BaseTestBroodClient
from .brood_client_responses import BroodResponses


class TestBroodClientV1(BaseTestBroodClient, unittest.TestCase):

    api_version = 1

    def setUp(self):
        super(TestBroodClientV1, self).setUp()
        self.brood_responses = BroodResponses(self.url_handler)
        self.organization = Organization
