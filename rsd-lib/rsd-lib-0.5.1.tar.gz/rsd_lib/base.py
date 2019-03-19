# Copyright 2019 Intel, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import copy

from sushy.resources import base

from rsd_lib import utils as rsd_lib_utils


class DynamicField(base.Field):
    """Base class for fields consisting of several dynamic attributes."""

    def __init__(self, *args, **kwargs):
        super(DynamicField, self).__init__(*args, **kwargs)
        self._subfields = None

    def _load(self, body, resource, nested_in=None):
        """Load the all attributes.

        :param body: parent JSON body.
        :param resource: parent resource.
        :param nested_in: parent resource name (for error reporting only).
        :returns: a new object with sub-fields attached to it.
        """
        nested_in = (nested_in or []) + self._path
        value = super(DynamicField, self)._load(body, resource)
        if value is None:
            return None

        # We need a new instance, as this method is called a singleton instance
        # that is attached to a class (not instance) of a resource or another
        # CompositeField. We don't want to end up modifying this instance.
        instance = copy.copy(self)
        for name, attr in value.items():
            setattr(
                instance, rsd_lib_utils.camelcase_to_underscore_joined(name),
                attr)

        return instance
