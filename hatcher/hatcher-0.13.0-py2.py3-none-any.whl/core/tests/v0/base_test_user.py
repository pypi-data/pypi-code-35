#  Copyright (c) 2018, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
import responses

from hatcher.core.brood_url_handler import BroodURLHandler
from hatcher.core.model_registry import ModelRegistry
from hatcher.core.url_templates import URLS_V0


class BaseTestUser(object):

    api_version = 0
    urls = URLS_V0
    brood_responses = None
    user = None

    def setUp(self):
        self.url_handler = BroodURLHandler.from_auth('http://brood-dev')
        self.model_registry = ModelRegistry(api_version=self.api_version)

    @responses.activate
    def test_delete_user(self):
        # Given
        self.brood_responses.test_delete_user()

        # When
        self.user.delete()

        # Then
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_metadata(self):
        # Given
        expected = {
            "email": "user@acme.org",
            "organization": "enthought",
            "teams": ["read_acme_dev_repository"]
        }
        self.brood_responses.test_get_metadata(expected)

        # When
        metadata = self.user.metadata()

        # Then
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(metadata, expected)
