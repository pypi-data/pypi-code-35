# -*- coding: utf-8 -*-
# Copyright 2018-2019 Mateusz Klos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# 3rd party imports
import pytest

# Project imports
from restible import RestResource
from restible_django import DjangoEndpoint


class ReadOnlyResource(RestResource):
    name = 'read_only'

    def __init__(self):
        super(ReadOnlyResource, self).__init__()
        self.options = True

    def rest_query(self, request, params, payload):
        return 200, [
            {'id': 123, 'name': 'test_resource'},
            {'id': 321, 'name': 'resource_test'},
        ]

    def rest_get(self, request, params, payload):
        return {
            'id': request.rest_keys['test_pk'],
            'name': 'test_resource'
        }


@pytest.mark.django
def test_aliased_as_endpoint_call_operator(rf):
    endpoint = DjangoEndpoint(res_cls=ReadOnlyResource)
    request = rf.get('/test')

    response = endpoint.dispatch(request)

    assert response.status_code == 200
