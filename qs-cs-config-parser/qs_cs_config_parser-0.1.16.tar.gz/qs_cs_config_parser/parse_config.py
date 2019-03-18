import json
import requests
from cloudshell.api.cloudshell_api import CloudShellAPISession, InputNameValue

DCMODEL = 'Dcstaticvm'
ARMMODELS = ['Checkpoint', 'CheckpointMgmt', 'Fortigate']
NIC_ROLES = ['FortiBranch', 'WANCPFW']
SB_SERVER_MODEL = 'Skybox-Server'
VSRX_Model = 'VSRx_NS'
AZURE_COMMANDS_SERVICE_ALIAS = 'Azuresupplementcommands'

class parse_commands():
    '''
    <<__DS__DeviceName__DS__>> - Place holder for a device name
    <<__DG__DeviceName__DG__>> - Place holder for a device name WITHOUT GUID
    <<__D__DeviceName__SN__SubnetName__D__>> - Place holder for a device IP in a specific Subnet
    <<__DX__DeviceName__SN__SubnetName__PB__Ip Idx__DX__>> - place holder for a device specific Public ip, in a specific
                                                            subnet (for cases where we added more than 1 IP per NIC)
    <<__DX__DeviceName__SN__SubnetName__PV__Ip Idx__DX__>> - place holder for a device specific Private ip, in a specific
                                                            subnet (for cases where we added more than 1 IP per NIC)
    <<__SN__SubnetName__SN__>> - Place holder for subnet CIDR
    <<__NA__SubnetName__NA__>> - Place holder for subnet CIDR NA - without the /x part (i.e /28)
    <<__NA__SandboxWide__NA__>> - Place holder for whole sandbox CIDR - without the /x part (i.e /28)
    <<__NX1__SubnetName__NX1__>> - Place holder for subnet CIDR NX - changes x.y.z.w -> x.y.z.(w+1)

    <<__PA__DEVICE_GROUP__PA__>>  - Device Group in Panorama
    <<__PA__SERIAL_NO__PA__>> - serial number of Pan GW on Panorama

    keywords:
    SandboxWide - the address space of the sandbox in it s entirety

    '''

    def __init__(self, session, res_id, logger=None):
        self.session = session
        self.res_id = res_id
        if logger:
            self.logger = logger
        else:
            self.logger = None

    def get_definitions(self, file_name, file_type):
        # try to see if local txt files exists , == production
        PRODUCTION_FILES_BASE_PATH = r'c:\Quali\Policies'
        full_file_path_to_read = (PRODUCTION_FILES_BASE_PATH + '\SkyboxDataFiles\DevicePolicy\{0}.{1}'.format(
                file_name, file_type
            ))
        self.logger.info('first trying to find local file at {}'.format(full_file_path_to_read))
        try:
            file = open(full_file_path_to_read, "r")
            github_raw = file.read()
            file.close()
            self.logger.info('reading policy from file')
        except:
            # if we reach the exception the local files are missing . that means we are in DEV
            self.logger.info('reading policy from file was unsuccessful , trying github')
            GITHUB_URL = r'https://raw.githubusercontent.com/QualiSystemsLab/SkyboxDataFiles/master/DevicePolicy/{0}.{1}'.format(
                file_name, file_type
            )
            github_raw = requests.get(GITHUB_URL).content
        if file_type == 'json':
            policy_object = json.loads(github_raw)
        else:
            policy_object = github_raw
        return policy_object

    def replace_placeholders(self, file_name, file_type, reservation_description):
        services = reservation_description.Services
        subnets = [service for service in services if service.ServiceName == 'Subnet']
        commands = self.get_definitions(file_name, file_type).split('\n')
        parsed_commands = []
        for command in commands:
            idx = 0
            while ('<<__') in command and idx < 10:
                idx = idx + 1
                if ('<<__SN__') in command:
                    # reference to subnet as cidr
                    command = self._parse_subnet_to_cidr(command = command, subnets=subnets)

                if ('<<__NA__') in command:
                    # reference to subnet as NA
                    command = self._parse_subnet_to_cidr_NA(command=command, subnets=subnets)

                if ('<<__NX1__') in command:
                    # reference to subnet as NX
                    command = self._parse_subnet_to_cidr_NX(command=command, subnets=subnets)

                if ('<<__D__') in command:
                    # reference to device with subnet
                    command = self._parse_device_with_subnet(command=command,
                                                              reservation_description=reservation_description,
                                                              subnets=subnets)
                if ('<<__DS__') in command:
                    # reference to device without subnet
                    command = self._parse_device_short(command=command,
                                                       reservation_description=reservation_description)

                if ('<<__DG__') in command:
                    # reference to device without subnet
                    command = self._parse_device_short_without_guid(command=command,
                                                                    reservation_description=reservation_description)

                if ('<<__PA__') in command:
                    # reference to Panorama special commands
                    command = self._panorama_handler(command=command,
                                                     reservation_description=reservation_description,
                                                     res_id=self.res_id,
                                                     session=self.session)
                    # case of PA twice in the same command - need to

                if ('<<__DX__') in command:
                    # reference to device without subnet
                    command = self._parse_device_with_addl_ips(command = command, reservation_description=reservation_description)

            parsed_commands.append(command)

        return parsed_commands

    def _parse_device_with_addl_ips(self, command, reservation_description):
        result_ip = None
        device_reference = command.split('<<__DX__')[1].split('__DX__>>')[0]
        current_device_name = device_reference.split('__SN__')[0]
        current_device_subnet_name = device_reference.split('__SN__')[1].split('__')[0]
        private_or_public = device_reference.split('__')[-2]
        index = device_reference.split('__')[-1]
        services = reservation_description.Services
        subnets = [service for service in services if service.ServiceName == 'Subnet']
        selected_subnet = self._get_subnet(current_device_subnet_name, subnets)
        device_full_name = self._find_gateway_entity(current_device_name, reservation_description)
        resource_details = self.session.GetResourceDetails(device_full_name)
        addl_ips_raw = [attr.Value for attr in resource_details.ResourceAttributes if attr.Name == 'Additional Network Info']
        if addl_ips_raw:
            addl_ips_raw_to_json = addl_ips_raw[0].replace('\\', '')
            addl_ips = json.loads(addl_ips_raw_to_json)
            addl_ips_json = addl_ips[selected_subnet.Alias]
            if private_or_public == 'PV':
                result_ip = addl_ips_json['Private IP'][int(index)]
            if private_or_public == 'PB':
                result_ip = addl_ips_json['Public IP'][int(index)]
            if result_ip:
                name_with_placeholders = '<<__DX__{0}__SN__{1}__{2}__{3}__DX__>>'.format(
                    current_device_name,
                    current_device_subnet_name,
                    private_or_public,
                    index
                )
                command = command.replace(name_with_placeholders, result_ip)
                self.logger.info('changed {0} to {1}'.format(name_with_placeholders, result_ip))
        else:
            self.logger.info('Failed to locate in command {0}'.format(command))
        return command



    def replace_placeholders_additional_nics(self, file_name, file_type, reservation_description):
        services = reservation_description.Services
        subnets = [service for service in services if service.ServiceName == 'Subnet']
        commands = self.get_definitions(file_name, file_type).split('\n')
        parsed_commands = []
        for command in commands:
            if ('<<__SN__') in command:
                # reference to subnet
                command = self._parse_subnet_to_alias(command=command, subnets=subnets)

            if ('<<__DS__') in command:
                # reference to device without subnet
                command = self._parse_device_short(command = command, reservation_description=reservation_description)

            parsed_commands.append(command)

        return parsed_commands

    def replace_place_holders_devices_name(self, file_name, file_type, reservation_description):
        services = reservation_description.Services
        subnets = [service for service in services if service.ServiceName == 'Subnet']
        commands = self.get_definitions(file_name, file_type).split('\n')
        parsed_commands = []
        for command in commands:
            if ('<<__DS__') in command:
                # reference to device without subnet
                command = self._parse_device_short(command = command, reservation_description=reservation_description)

            parsed_commands.append(command)

        return parsed_commands

    def _parse_device_with_subnet(self, command, reservation_description, subnets):
        device_reference = command.split('<<__D__')[1].split('__D__>>')[0]
        current_device_name = device_reference.split('__SN__')[0]
        current_device_subnet_name = device_reference.split('__SN__')[1]

        selected_subnet = self._get_subnet(current_device_subnet_name, subnets)
        subnet_name = '' if selected_subnet is None else selected_subnet.Alias

        device_full_name = self._find_gateway_entity(current_device_name, reservation_description)

        if device_full_name is not None:
            self.logger.info(
                'Located device full name {0} in command {1}'.format(device_full_name, command))

            nic_ip = self._get_nic_connected_to_subnet(
                session=self.session,
                entity_name=device_full_name,
                subnet_name=subnet_name,
                reservation_description=reservation_description,
                subnets=subnets,
                res_id=self.res_id
            )
            device_name_with_placeholders = '<<__D__{0}__SN__{1}__D__>>'.format(current_device_name,
                                                                                current_device_subnet_name)
            command = command.replace(device_name_with_placeholders, nic_ip)
        else:
            self.logger.info('Failed to locate subnet {0} in command {1}'.format(current_device_name, command))

        return command

    def _parse_device_short (self, command, reservation_description):
        current_device_name = command.split('<<__DS__')[1].split('__DS__>>')[0]

        device_full_name = self._find_gateway_entity(current_device_name, reservation_description)

        self.logger.info('B3 Device full Name  is {0}'.format(device_full_name))
        if device_full_name is not None:
            self.logger.info(
                'Located device full name {0} in command {1}'.format(device_full_name, command))

            device_name_with_placeholders = '<<__DS__{0}__DS__>>'.format(current_device_name)
            command = command.replace(device_name_with_placeholders, device_full_name)
        else:
            self.logger.info('Failed to locate subnet {0} in command {1}'.format(current_device_name, command))

        return command

    def _parse_device_short_without_guid(self, command, reservation_description):
        current_device_name = command.split('<<__DG__')[1].split('__DG__>>')[0]

        device_full_name = '-'.join(self._find_gateway_entity(current_device_name, reservation_description).split('-')[:-1])

        self.logger.info('B3 Device full Name  is {0}'.format(device_full_name))
        if device_full_name is not None:
            self.logger.info(
                'Located device full name {0} in command {1}'.format(device_full_name, command))

            device_name_with_placeholders = '<<__DG__{0}__DG__>>'.format(current_device_name)
            command = command.replace(device_name_with_placeholders, device_full_name)
        else:
            self.logger.info('Failed to locate subnet {0} in command {1}'.format(current_device_name, command))

        return command

    def _get_device_group_name(self, session, res_id):
        sbox_last_guid_segment = res_id.split('-')[-1]

        shorthand_sandbox_name = session.GetReservationDetails(res_id).ReservationDescription.Name[:18].replace(' ','').strip()
        # shorthand_blueprint_name = context.reservation.environment_path[:18]

        device_group_name = '{0}-{1}'.format(shorthand_sandbox_name, sbox_last_guid_segment)

        return device_group_name

    def _panorama_handler(self, command, reservation_description, session, res_id ):
        '''
        :param command:
        :param reservation_description:
        :param CloudShellAPISession session:
        :param res_id:
        :return:
        '''
        current_action = command.split('<<__PA__')[1].split('__PA__>>')[0]

        if current_action == 'DEVICE_GROUP':
            device_group_name = self._get_device_group_name(session, res_id)
            converted_action = device_group_name
        elif current_action == 'SERIAL_NO':
            resources = reservation_description.Resources
            PAN_GW_name = [res.Name for res in resources if res.ResourceModelName == 'PAG_NS'][0]
            serial_number = [attr.Value for attr in session.GetResourceDetails(PAN_GW_name).ResourceAttributes if attr.Name == 'Serial Number'][0]
            converted_action = serial_number
        else:
            # dont know what to do here - so exception
            converted_action = None

        if converted_action is not None:
            self.logger.info(
                'Converting action {0} in command {1}'.format(converted_action, command))

            device_name_with_placeholders = '<<__PA__{0}__PA__>>'.format(current_action)
            self.logger.info('with placeholder :{}'.format(device_name_with_placeholders))
            command = command.replace(device_name_with_placeholders, converted_action)
            self.logger.info(
                'Converted action {0} in command {1}'.format(converted_action, command))
        else:
            self.logger.info('Failed to locate action for panorama {0} in command {1}'.format(converted_action, command))

        return command

    def _parse_subnet_to_alias(self, command, subnets):
        current_subnet_name = command.split('<<__SN__')[1].split('__SN__>>')[0]

        # current_subnet = [x for x in subnets if x.Alias.startswith(current_subnet_name)][0]
        current_subnet = self._get_subnet(current_subnet_name, subnets)

        if current_subnet is not None:
            self.logger.info('Located subnet full name {0} in command {1}'.format(current_subnet.Alias, command))
            subnet_name_with_placeholders = '<<__SN__{}__SN__>>'.format(current_subnet_name)
            command = command.replace(subnet_name_with_placeholders, current_subnet.Alias)
        else:
            self.logger.info('Failed to locate subnet {0} in command {1}'.format(current_subnet_name, command))

        return command

    def _parse_subnet_to_cidr(self, command, subnets):
        current_subnet_name = command.split('<<__SN__')[1].split('__SN__>>')[0]

        # current_subnet = [x for x in subnets if x.Alias.startswith(current_subnet_name)][0]
        current_subnet = self._get_subnet(current_subnet_name, subnets)

        if current_subnet is not None:
            self.logger.info('Located subnet full name {0} in command {1}'.format(current_subnet.Alias, command))
            current_subnet_cidr = filter(lambda x: x.Name == 'Allocated CIDR', current_subnet.Attributes)[0].Value
            subnet_name_with_placeholders = '<<__SN__{}__SN__>>'.format(current_subnet_name)
            command = command.replace(subnet_name_with_placeholders, current_subnet_cidr)
        else:
            self.logger.info('Failed to locate subnet {0} in command {1}'.format(current_subnet_name, command))

        return command

    def _parse_subnet_to_cidr_NA(self, command, subnets):
        current_subnet_name = command.split('<<__NA__')[1].split('__NA__>>')[0]

        if current_subnet_name == 'SandboxWide':
            sandbox_wide_subnet_cidr_raw = filter(lambda x: x.Name == 'Allocated CIDR',
                                                  subnets[0].Attributes)[0].Value
            current_subnet_cidr = '.'.join(sandbox_wide_subnet_cidr_raw.split('.')[:-1]) + '.0'
        else:
            current_subnet = self._get_subnet(current_subnet_name, subnets)
            if current_subnet is not None:
                current_subnet_cidr = filter(lambda x: x.Name == 'Allocated CIDR',
                                             current_subnet.Attributes)[0].Value.split('/')[0]
            else:
                self.logger.info('Failed to locate subnet {0} in command {1}'.format(current_subnet_name, command))

        subnet_name_with_placeholders = '<<__NA__{}__NA__>>'.format(current_subnet_name)
        self.logger.info(
            'replacing placeholder {0} with {1}'.format(subnet_name_with_placeholders, current_subnet_cidr))
        command = command.replace(subnet_name_with_placeholders, current_subnet_cidr)

        return command

    def _parse_subnet_to_cidr_NX(self, command, subnets):
        current_subnet_name = command.split('<<__NX1__')[1].split('__NX1__>>')[0]

        # current_subnet = [x for x in subnets if x.Alias.startswith(current_subnet_name)][0]
        current_subnet = self._get_subnet(current_subnet_name, subnets)
        self.logger.info('NX placeholder found for subnet {}'.format(current_subnet_name))
        if current_subnet is not None:
            self.logger.info(
                'Located subnet full name {0} in command {1}'.format(current_subnet.Alias, command))
            current_subnet_cidr_raw = \
            filter(lambda x: x.Name == 'Allocated CIDR', current_subnet.Attributes)[0].Value.split('/')[0]
            octat = str(int(current_subnet_cidr_raw.split('.')[-1]) + 1)
            current_subnet_cidr = '.'.join(current_subnet_cidr_raw.split('.')[:-1]) + '.' + octat
            subnet_name_with_placeholders = '<<__NX1__{}__NX1__>>'.format(current_subnet_name)
            self.logger.info(
                'replacing placeholder {0} with {1}'.format(subnet_name_with_placeholders, current_subnet_cidr))
            command = command.replace(subnet_name_with_placeholders, current_subnet_cidr)
        else:
            self.logger.info('failed to locate subnet {0} in command {1}'.format(current_subnet_name, command))

        return command

    def _get_subnet(self, subnet_partial_name, subnets):
        found_subnet = None

        for subnet_candidate in subnets:
            formatted_alias = '{}'.format('-'.join(subnet_candidate.Alias.split('-')[:-2]).strip())
            if formatted_alias == subnet_partial_name:
                found_subnet = subnet_candidate
        
        return found_subnet

    def _get_nic_connected_to_subnet(self, session, entity_name, subnet_name, reservation_description, subnets, res_id):
        connections = reservation_description.Connectors
        resources = reservation_description.Resources
        services = reservation_description.Services
        subnets = [service for service in services if service.ServiceName == 'Subnet']
        subnet_connections = [c for c in connections if c.Source == subnet_name or c.Target == subnet_name]
        subnet_object = [sub for sub in subnets if sub.Alias == subnet_name][0]
        subnet_id = [attr.Value for attr in subnet_object.Attributes if attr.Name == 'Subnet Id'][0]
        requested_ip = None
        try:
            resource_details = session.GetResourceDetails(entity_name)
            subnet_net_id_adddata = [x for x in resource_details.VmDetails.NetworkData if x.NetworkId == subnet_id][0]
            requested_ip = [x.Value for x in subnet_net_id_adddata.AdditionalData if x.Name == 'ip'][0]
            pass
        except:
            # this is a service then
            try:
                service_nics_data_raw = session.ExecuteCommand(
                reservationId=res_id,
                targetType='Service',
                targetName=AZURE_COMMANDS_SERVICE_ALIAS,
                commandName='print_vm_nic_information',
                commandInputs=[InputNameValue(
                    Name='alias',
                    Value=entity_name
                )],
                printOutput=False
                ).Output
                service_nics_data = json.loads(service_nics_data_raw)
            except:
                pass
            try:
                requested_ip = [x['Private IP'] for x in service_nics_data if x['Subnet Name'] == subnet_id][0]
            except:
                requested_ip = 'Not Found'
        return requested_ip

    def _find_gateway_entity(self, gateway_name, reservation_description):
        '''
        :param CloudShellAPISession session:
        '''
        resources = reservation_description.Resources
        services = reservation_description.Services
        resources_from_apps = [res for res in resources if res.AppDetails]
        gateway = [x.Name for x in resources_from_apps if x.AppDetails.AppName.lower() == gateway_name.lower()]
        if gateway.__len__() > 0:
            return gateway[0]
        else:
            gateway = [x.Alias for x in services if x.Alias.lower() == gateway_name.lower()]
            if gateway.__len__() > 0:
                return gateway[0]
            else:
                gateway = None
                return gateway

