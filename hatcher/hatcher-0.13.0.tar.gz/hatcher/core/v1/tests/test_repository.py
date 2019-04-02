#  Copyright (c) 2015, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
from hatcher.testing import unittest
from hatcher.core.tests.v1.base_test_repository import BaseTestRepository
from hatcher.core.v1.repository import Repository
from .repository_responses import BroodResponses


class TestRepository(BaseTestRepository, unittest.TestCase):

    def setUp(self):
        super(TestRepository, self).setUp()
        self.repository = Repository(
            'enthought', 'free', self.url_handler,
            model_registry=self.model_registry)
        self.brood_responses = BroodResponses(
            self.url_handler, self.repository)
