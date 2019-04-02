#  Copyright (c) 2017, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
import responses

from hatcher.testing import unittest
from hatcher.core.v0.organization import Organization
from hatcher.core.tests.base_test_brood_client import BaseTestBroodClient
from .brood_client_responses import BroodResponses


class TestBroodClientV0(BaseTestBroodClient, unittest.TestCase):

    api_version = 0

    def setUp(self):
        super(TestBroodClientV0, self).setUp()
        self.brood_responses = BroodResponses(self.url_handler)
        self.organization = Organization


    @responses.activate
    def test_list_available_repositories(self):
        # Given
        expected = self.brood_responses.test_list_available_repositories()

        # When
        repositories = self.brood.list_available_repositories()

        # Then
        self.assertEqual(repositories, expected)
        self.assertEqual(len(responses.calls), 1)
        request = responses.calls[0].request
        self.assertTrue(request.url.endswith('?include_indexable=False'))

    @responses.activate
    def test_list_available_repositories_include_indexable(self):
        # Given
        expected = self.brood_responses.test_list_available_repositories_include_indexable()  # noqa

        # When
        repositories = self.brood.list_available_repositories(
            include_indexable=True)

        # Then
        self.assertEqual(repositories, expected)
        self.assertEqual(len(responses.calls), 1)
        request = responses.calls[0].request
        self.assertTrue(request.url.endswith('?include_indexable=True'))
