#  Copyright (c) 2018, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
import json
import responses

from hatcher.core.url_templates import URLS_V1


class BroodResponses(object):
    """ Mocked brood responses for the repository tests.

    This class contains methods that will setup the necessary requests
    responses to mock the expected behaviour from brood. Each method
    is named after the related test in the related BaseTestOrganization
    testcase for V1 entry points.

    """
    def __init__(self, url_handler):
        self.url_handler = url_handler
        self.urls = URLS_V1

    def response(self, path):
        handler = self.url_handler
        return '{scheme}://{host}{path}'.format(
            scheme=handler.scheme, host=handler.host, path=path)

    def test_create_repository(self):
        responses.add(
            responses.POST,
            self.response(
                path=self.urls.admin.organizations.repositories.format(
                    organization_name='acme')))

    def test_create_user(self):
        responses.add(
            responses.POST,
            self.response(
                path=self.urls.admin.organizations.users.format(
                    organization_name='acme')),
            status=201)

    def test_list_repositories(self, expected):
        responses.add(
            responses.GET,
            self.response(
                path=self.urls.admin.organizations.repositories.format(
                    organization_name='acme')),
            body=json.dumps({'repositories': expected}),
            content_type='application/json')

    def test_list_users(self, expected):
        responses.add(
            responses.GET,
            self.response(
                path=self.urls.admin.organizations.users.format(
                    organization_name='acme')),
            body=json.dumps({'users': expected})
        )
