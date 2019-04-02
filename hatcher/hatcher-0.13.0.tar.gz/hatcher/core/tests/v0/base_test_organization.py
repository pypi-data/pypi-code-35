#  Copyright (c) 2018, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
import json

import responses

from hatcher.testing import unittest
from hatcher.core.brood_url_handler import BroodURLHandler
from hatcher.core.model_registry import ModelRegistry
from hatcher.core.url_templates import URLS_V0
from hatcher.core.tests.common import JsonSchemaTestMixin


class BaseTestOrganization(JsonSchemaTestMixin):

    api_version = 0
    urls = URLS_V0
    brood_responses = None
    organization = None
    repository_type = None
    user_type = None

    def setUp(self):
        self.url_handler = BroodURLHandler.from_auth('http://brood-dev')
        self.model_registry = ModelRegistry(api_version=self.api_version)

    @responses.activate
    def test_get_repository(self):
        # When
        repository = self.organization.repository('free')

        # Then
        self.assertIsInstance(repository, self.repository_type)
        self.assertEqual(repository.organization_name, self.organization.name)
        self.assertEqual(repository.name, 'free')

    @responses.activate
    def test_create_repository(self):
        # Given
        expected = {
            'name': 'dev',
            'description': 'Dev Repository',
        }
        self.brood_responses.test_create_repository()

        # When
        repository = self.organization.create_repository(
            'dev', 'Dev Repository')

        # Then
        self.assertEqual(repository.organization_name, self.organization.name)
        self.assertEqual(repository.name, 'dev')
        self.assertEqual(len(responses.calls), 1)
        call, = responses.calls
        request, response = call
        self.assertJsonValid(request.body, 'create_repository.json')
        self.assertEqual(json.loads(request.body), expected)
        self.assertEqual(
            request.headers.get('Content-Type'), 'application/json')

    @responses.activate
    def test_get_user(self):
        # When
        user = self.organization.user('user@acme.org')

        # Then
        self.assertIsInstance(user, self.user_type)
        self.assertEqual(user.organization_name, self.organization.name)
        self.assertEqual(user.email, 'user@acme.org')

    @responses.activate
    def test_create_user(self):
        # Given
        email = 'user@acme.org'
        expected = {'email': email}
        self.brood_responses.test_create_user()

        # When
        user = self.organization.create_user(email)

        # Then
        self.assertEqual(user.organization_name, self.organization.name)
        self.assertEqual(user.email, email)
        self.assertEqual(len(responses.calls), 1)
        call, = responses.calls
        request, response = call
        self.assertJsonValid(request.body, 'create_organization_user.json')
        self.assertEqual(json.loads(request.body), expected)
        self.assertEqual(
            request.headers.get('Content-Type'), 'application/json')

    @unittest.expectedFailure
    @responses.activate
    def test_delete_organization(self):
        # When
        self.organization.delete()

        # Then
        self.assertEqual(len(responses.calls), 1)

    @unittest.expectedFailure
    @responses.activate
    def test_get_metadata(self):
        # When
        self.organization.metadata()

        # Then
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_list_repositories(self):
        # Given
        expected = ['free', 'commercial', 'testing']
        self.brood_responses.test_list_repositories(expected)

        # When
        repositories = self.organization.list_repositories()

        # Then
        self.assertEqual(repositories, expected)

    @unittest.expectedFailure
    @responses.activate
    def test_list_users(self):
        # Given
        expected = ['user@acme.org', 'admin@acme.org']
        self.brood_responses.test_list_users(expected)

        # When
        users = self.organization.list_users()

        # Then
        self.assertEqual(users, expected)
