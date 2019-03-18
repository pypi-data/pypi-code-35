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

from sushy.resources import base
from sushy import utils

from rsd_lib import common as rsd_lib_common
from rsd_lib.resources.v2_1.chassis import log_entry
from rsd_lib import utils as rsd_lib_utils


class LogService(base.ResourceBase):
    identity = base.Field('Id', required=True)
    """The log service identity string"""

    description = base.Field('Description')
    """The log service description"""

    name = base.Field('Name')
    """The log service name"""

    status = rsd_lib_common.StatusField('Status')
    """The log service status"""

    service_enabled = base.Field("ServiceEnabled", adapter=bool)
    """This indicates whether this service is enabled"""

    max_number_of_records = base.Field("MaxNumberOfRecords",
                                       adapter=rsd_lib_utils.num_or_none)
    """The maximum number of log entries this service can have"""

    overwrite_policy = base.Field("OverWritePolicy")
    """The overwrite policy for this service that
     takes place when the log is full
     """

    date_time = base.Field("DateTime")
    """The current DateTime (with offset) for the log
       service, used to set or read time
    """

    date_time_local_offset = base.Field("DateTimeLocalOffset")
    """The time offset from UTC that the DateTime
       property is set to in format: +06:00
    """

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a LogService

        :param connector: A Connector instance
        :param identity: The identity of the log service resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(LogService, self).__init__(connector, identity, redfish_version)

    def _get_entry_collection_path(self):
        """Helper function to find the LogEntryCollection path"""
        return utils.get_sub_resource_path_by(self, 'Entries')

    @property
    @utils.cache_it
    def log_entries(self):
        """Property to provide reference to `LogEntryCollection` instance

        It is calculated once when it is queried for the first time. On
        refresh, this property is reset.
        """
        return log_entry.LogEntryCollection(
            self._conn, self._get_entry_collection_path(),
            redfish_version=self.redfish_version)


class LogServicesCollection(base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return LogService

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a LogService Collection

        :param connector: A Connector instance
        :param path: The canonical path to the LogService Collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(LogServicesCollection, self).__init__(connector,
                                                    path,
                                                    redfish_version)
