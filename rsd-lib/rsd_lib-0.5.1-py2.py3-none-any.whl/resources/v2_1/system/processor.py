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

from rsd_lib import common as rsd_lib_common
from rsd_lib import utils as rsd_lib_utils


class ProcessorIdField(base.CompositeField):

    effective_family = base.Field('EffectiveFamily')
    """The processor effective family"""

    effective_model = base.Field('EffectiveModel')
    """The processor effective model"""

    identification_registers = base.Field('IdentificationRegisters')
    """The processor identification registers"""

    microcode_info = base.Field('MicrocodeInfo')
    """The processor microcode info"""

    step = base.Field('Step')
    """The processor stepping"""

    vendor_id = base.Field('VendorId')
    """The processor vendor id"""


class IntelRackScaleField(base.CompositeField):

    brand = base.Field("Brand")
    """This property shall represent the brand of processor"""

    capabilities = base.Field("Capabilities")
    """This property shall represent array of processor capabilities
       (like reported in /proc/cpuinfo flags)
    """


class OemField(base.CompositeField):

    intel_rackscale = IntelRackScaleField("Intel_RackScale")
    """Intel Rack Scale Design extensions ("Intel_RackScale" object)"""


class Processor(base.ResourceBase):

    identity = base.Field('Id', required=True)
    """The processor identity string"""

    name = base.Field('Name')
    """The processor name string"""

    description = base.Field('Description')
    """The processor description string"""

    socket = base.Field('Socket')
    """The socket or location of the processor"""

    processor_type = base.Field('ProcessorType')
    """The type of processor"""

    processor_architecture = base.Field('ProcessorArchitecture')
    """The architecture of the processor"""

    instruction_set = base.Field('InstructionSet')
    """The instruction set of the processor"""

    manufacturer = base.Field('Manufacturer')
    """The processor manufacturer"""

    model = base.Field('Model')
    """The product model number of this device"""

    max_speed_mhz = base.Field(
        'MaxSpeedMHz', adapter=rsd_lib_utils.num_or_none)
    """The maximum clock speed of the processor in MHz."""

    processor_id = ProcessorIdField('ProcessorId')
    """The processor id"""

    status = rsd_lib_common.StatusField('Status')
    """The processor status"""

    total_cores = base.Field(
        'TotalCores', adapter=rsd_lib_utils.num_or_none)
    """The total number of cores contained in this processor"""

    total_threads = base.Field(
        'TotalThreads', adapter=rsd_lib_utils.num_or_none)
    """The total number of execution threads supported by this processor"""

    oem = OemField("Oem")
    """Oem extension object"""

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a Processor

        :param connector: A Connector instance
        :param identity: The identity of the processor
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(Processor, self).__init__(connector, identity, redfish_version)


class ProcessorCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return Processor

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a ProcessorCollection

        :param connector: A Connector instance
        :param path: The canonical path to the Processor collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(ProcessorCollection, self).__init__(connector, path,
                                                  redfish_version)
