#  Copyright (c) 2018, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
import json
import responses

from hatcher.core.brood_url_handler import BroodURLHandler
from hatcher.core.brood_client import BroodClient
from hatcher.core.tests.common import JsonSchemaTestMixin


class BaseTestBroodClient(JsonSchemaTestMixin):

    api_version = None
    brood_responses = None
    organization = None

    def setUp(self):
        self.url_handler = BroodURLHandler.from_auth('http://brood-dev')
        self.brood = BroodClient(
            url_handler=self.url_handler, api_version=self.api_version)

    @responses.activate
    def test_get_organization(self):
        # When
        organization = self.brood.organization('acme')

        # Then
        self.assertIsInstance(organization, self.organization)
        self.assertEqual(organization.name, 'acme')

    @responses.activate
    def test_create_organization(self):
        # Given
        expected = {
            'name': 'acme',
            'description': 'Acme co.',
        }
        self.brood_responses.test_create_organization()
        # When
        self.brood.create_organization('acme', 'Acme co.')

        # Then
        self.assertEqual(len(responses.calls), 1)
        call, = responses.calls
        request, response = call
        self.assertHatcherUserAgent(request)
        self.assertJsonValid(request.body, 'create_organization.json')
        self.assertEqual(json.loads(request.body), expected)
        self.assertEqual(
            request.headers.get('Content-Type'), 'application/json')

    @responses.activate
    def test_list_organizations(self):
        # Given
        expected = ['enthought', 'acme']
        self.brood_responses.test_list_organizations(expected)

        # When
        organizations = self.brood.list_organizations()

        # Then
        call, = responses.calls
        request, response = call
        self.assertHatcherUserAgent(request)
        self.assertEqual(organizations, list(sorted(expected)))

    @responses.activate
    def test_create_api_token(self):
        # Given
        name = 'mytoken'
        self.brood_responses.test_create_api_token(name, 1234)

        # When
        created_token = self.brood.create_api_token(name)

        # Then
        self.assertEqual(created_token, {'name': name, 'token': 1234})

    @responses.activate
    def test_delete_api_token(self):
        # Given
        name = 'my-token'
        self.brood_responses.test_delete_api_token(name)

        # When
        self.brood.delete_api_token(name)

        # Then
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_list_api_tokens(self):
        # Given
        expected = self.brood_responses.test_list_api_tokens()

        # When
        tokens = self.brood.list_api_tokens()

        # Then
        self.assertEqual(tokens, expected)

    @responses.activate
    def test_list_platforms(self):
        # Given
        expected = [
            'osx-x86',
            'osx-x86_64',
            'rh5-x86',
            'rh5-x86_64',
        ]
        self.brood_responses.test_list_platforms(expected)

        # When
        platforms = self.brood.list_platforms()

        # Then
        self.assertEqual(platforms, expected)

    @responses.activate
    def test_list_python_tags(self):
        # Given
        expected = [
            'cp27',
            'pp27',
            'cp34',
        ]
        self.brood_responses.test_list_python_tags(expected)

        # When
        platforms = self.brood.list_python_tags()

        # Then
        self.assertEqual(set(platforms), set(expected))

    @responses.activate
    def test_list_all_python_tags(self):
        # Given
        expected = [
            'cp27',
            'pp27',
            'cp34',
            'py2',
        ]
        self.brood_responses.test_list_all_python_tags(expected)

        # When
        platforms = self.brood.list_python_tags(list_all=True)

        # Then
        self.assertEqual(set(platforms), set(expected))

    @responses.activate
    def test_list_available_repositories(self):
        # Given
        expected = self.brood_responses.test_list_available_repositories()

        # When
        repositories = self.brood.list_available_repositories()

        # Then
        self.assertEqual(repositories, expected)
        self.assertEqual(len(responses.calls), 1)

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
