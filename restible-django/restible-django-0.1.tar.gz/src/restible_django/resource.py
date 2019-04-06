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
"""
Base class for django based REST resources
"""
from __future__ import absolute_import, unicode_literals

# 3rd party imports
from django.db.utils import IntegrityError

# local imports
from restible.model import ModelResource


class DjangoResource(ModelResource):
    """ Base class for django based REST resources. """
    def create_item(self, request, params, payload):
        del request, params     # Unused here

        try:
            return self.model.objects.create(**payload)
        except IntegrityError as ex:
            raise ModelResource.AlreadyExists(str(ex))

    def update_item(self, request, params, payload):
        del params      # Unused here
        pk = self.get_pk(request)
        return self.model.objects.filter(pk=pk).update(**payload)

    def delete_item(self, request, params, payload):
        del params, payload      # Unused here
        item = self.item_for_request(request)
        if item:
            item.delete()

    def query_items(self, request, params, payload):
        del request, payload      # Unused here
        return self.model.objects.filter(**params)

    def get_item(self, request, params, payload):
        """ Get requested item. """
        del params, payload      # Unused here
        return self.item_for_request(request)

    def item_for_request(self, request):
        """ Get requested item. """
        pk = self.get_pk(request)
        try:
            return self.dbquery(request, {}).get(pk=pk)
        except self.model.DoesNotExist:
            return None
