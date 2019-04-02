#  Copyright (c) 2018, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
import json
from datetime import datetime

import responses

from hatcher.core.url_templates import URLS_V1


class BroodResponses(object):
    """ Mocked brood responses for the brood client tests.

    This class contains methods that will setup the necessary requests
    responses to mock the expected behaviour from brood. Each method
    is named after the related test in the related BaseTestBroodClient
    testcase for V1 entry points.

    """

    def __init__(self, url_handler):
        self.url_handler = url_handler
        self.urls = URLS_V1

    def response(self, path):
        handler = self.url_handler
        return '{scheme}://{host}{path}'.format(
            scheme=handler.scheme, host=handler.host, path=path)

    def repository_list_response(self, indexable=False):
        repositories = {
            'repositories': [
                {
                    'name': 'acme/prod',
                    'access': 'organization_administrator',
                    'description': 'acme repo',
                },
                {
                    'name': 'enthought/free',
                    'access': 'read_repository',
                    'description': 'enthought free repository',
                },
                {
                    'name': 'enthought/commercial',
                    'access': 'read_index',
                    'description': 'enthought commercial repository',
                },
            ]
        }
        responses.add(
            responses.GET,
            self.response(path=self.urls.user.repositories.format()),
            status=200,
            body=json.dumps(repositories),
            content_type='application/json')

        if indexable:
            return ['acme/prod', 'enthought/free', 'enthought/commercial']
        else:
            return ['acme/prod', 'enthought/free']

    def test_create_organization(self):
        responses.add(
            responses.POST,
            self.response(path=self.urls.admin.organizations.format()))

    def test_list_organizations(self, organizations):
        responses.add(
            responses.GET,
            self.response(
                path=self.urls.admin.organizations.format()),
            body=json.dumps({'organizations': organizations}))

    def test_create_api_token(self, name, token):
        expected = {'name': name, 'token': token}
        responses.add(
            responses.POST,
            self.response(path=self.urls.tokens.api.format()),
            status=200,
            body=json.dumps(expected),
            content_type='application/json')

    def test_delete_api_token(self, name):
        # Given
        responses.add(
            responses.DELETE,
            self.response(
                path=self.urls.tokens.api.delete.format(name=name)),
            status=204)

    def test_list_api_tokens(self):
        # Given
        tokens = [
            {
                'name': 'token1',
                'created': datetime(2014, 1, 1, 1, 2, 2, 2).isoformat(),
                'last_used': datetime(2014, 2, 3, 4, 5, 6, 7).isoformat(),
            },
            {
                'name': 'token2',
                'created': datetime(2013, 2, 2, 2, 3, 3, 3).isoformat(),
                'last_used': datetime(2014, 7, 6, 5, 4, 3, 2).isoformat(),
            },
            {
                'name': 'token3',
                'created': datetime(2013, 3, 3, 3, 4, 4, 4).isoformat(),
                'last_used': None,
            },
        ]
        responses.add(
            responses.GET,
            self.response(path=self.urls.tokens.api.format()),
            status=200,
            body=json.dumps({'tokens': tokens}),
            content_type='application/json')
        return tokens

    def test_list_platforms(self, platforms):
        responses.add(
            responses.GET,
            self.response(path=self.urls.metadata.platforms.format()),
            status=200,
            body=json.dumps({'platforms': platforms}),
            content_type='application/json')

    def test_list_python_tags(self, tags):
        responses.add(
            responses.GET,
            self.response(path=self.urls.metadata.python_tags.format()),
            status=200,
            body=json.dumps({'python_tags': tags}),
            content_type='application/json')

    def test_list_all_python_tags(self, tags):
        responses.add(
            responses.GET,
            self.response(path=self.urls.metadata.python_tags.all.format()),
            status=200,
            body=json.dumps({'python_tags': tags}),
            content_type='application/json')

    def test_list_available_repositories(self):
        return self.repository_list_response()

    def test_list_available_repositories_include_indexable(self):
        return self.repository_list_response(True)
