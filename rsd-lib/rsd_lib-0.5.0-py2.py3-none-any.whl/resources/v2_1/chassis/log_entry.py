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

from rsd_lib import utils as rsd_lib_utils
from sushy.resources import base
from sushy import utils


class LinksField(base.CompositeField):
    OriginOfCondition = base.Field("OriginOfCondition",
                                   adapter=utils.get_members_identities)
    """The URI of the resource that caused the log entry"""


class LogEntry(base.ResourceBase):
    identity = base.Field('Id', required=True)
    """The log entry identity string"""

    description = base.Field('Description')
    """The log entry description"""

    name = base.Field('Name')
    """The log entry name"""

    severity = base.Field("Severity")
    """The severity of the log entry"""

    created = base.Field("Created")
    """The time the log entry was created"""

    entry_type = base.Field("EntryType")
    """"The type of log entry"""

    oem_record_format = base.Field("OemRecordFormat")
    """The log entry oem record format"""

    entry_code = base.Field("EntryCode")
    """The log entry code"""

    sensor_type = base.Field("SensorType")
    """The log entry sensor type"""

    sensor_number = base.Field("SensorNumber",
                               adapter=rsd_lib_utils.num_or_none)
    """The log entry sensor number"""

    message = base.Field("Message")
    """The log entry message"""

    message_id = base.Field("MessageId")
    """The log entry message id"""

    message_args = base.Field("MessageArgs")
    """The log entry message args"""

    links = LinksField("Links")
    """The log entry links"""

    event_type = base.Field("EventType")
    """The type of an event recorded in this log"""

    event_id = base.Field("EventId")
    """A unique instance identifier of an event"""

    event_timestamp = base.Field("EventTimestamp")
    """Time the event occurred"""


class LogEntryCollection(base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return LogEntry

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a LogEntry Collection

        :param connector: A Connector instance
        :param path: The canonical path to the LogEntry Collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(LogEntryCollection, self).__init__(connector,
                                                 path,
                                                 redfish_version)
