'''
    This file will be used for functionality defining to the HA feature in aws
'''

import logging
import boto3
import datetime
import os
import sys
from logging.handlers import RotatingFileHandler
import argparse
import re
import json
import requests
import time
import shutil
from urllib3.exceptions import NewConnectionError, ConnectTimeoutError, MaxRetryError

DESTINATION_CIDR_BLOCK = "DestinationCidrBlock"
NETWORK_INTERFACE_ID = "NetworkInterfaceId"
ROUTE_TABLE_ID = "routeTableId"
REGION = "region"
ENI_ID = "eniId"
ROUTE = "route"
MODE = "mode"
PRIMARY = "primary"
HA = 'ha'
EVENTS = 'events'
EVENT_LOGS = '/home/guestshell/cloud/HA/events'
REVERT = 'revert'

class HACsr:
    '''
     Functions implemented as api's from csr_ha package
    '''

    def __init__(self):
        self.log = logging.getLogger('ha')

        # Setting event_logger for route events for fail-safe approach
        # Ideally csr_ha is responsible for setting it up using set_event_logger
        self.event_logger = self.log
        self.event_log_file = ""
        try:
            if os.path.exists("/home/guestshell/cloud/HA/csr_ha.log"):
                if os.path.getsize("/home/guestshell/cloud/HA/csr_ha.log") > 15000000:
                    shutil.copy('/home/guestshell/cloud/HA/csr_ha.log', '/bootflash/csr_ha.log')
                    os.remove('/home/guestshell/cloud/HA/csr_ha.log')
        except Exception as e:
            #This is backing up the csr_ha.log file, if file size is above 10 MB. Log the exception and continue so that HACsr object initialization doesn't fail because of this
            self.log.exception("Exception in init is {e}".format(e=e))
        res = ''
        num_retry = 0
        while res == '':
            try:
                num_retry += 1
                res = requests.get("http://169.254.169.254/latest/dynamic/instance-identity/document")
                self.log.info("CSR is in region: %s", res.json()['region'])
                self.region = res.json()['region']
            except Exception as e:
                if num_retry == 5:
                    self.log.warning('Error in fetching region after 5 retries. Exception is %s' % e)
                    self.region = 'us-east-1'
                    self.log.warning("Region is set to us-east-1 by default")
                    pass
                else:
                    self.log.warning('Error in fetching region...Retrying')
                    time.sleep(10)
                    continue

        ec2_client = boto3.client('ec2', region_name=self.region)

        self.log.info("HACsr initialization complete")

    def validate_route_table_string(self, s, pat=re.compile(r"rtb-[a-fA-F0-9]{8,}")):
        self.log.info("Validating if the route table id format matches with AWS")
        if not pat.match(s) or len(pat.match(s).group(0)) != len(s):
            raise argparse.ArgumentTypeError('input %s does not match the route table id pattern "rtb-[a-fA-F0-9]{8,}"' % s)
        return s

    def validate_eni_string(self, s, pat=re.compile(r"eni-[a-fA-F0-9]{8,}")):
        self.log.info("Validating if the ENI ID format matches with aws")
        if not pat.match(s) or len(pat.match(s).group(0)) != len(s):
            raise argparse.ArgumentTypeError('input %s does not match the eni id pattern "eni-[a-fA-F0-9]{8,}"' % s)
        return s

    def validate_inputs(self, args):
        node = {}
        node[REGION] = args.rg
        response, fail_response_code = self.get_response_dict()
        resp_msg = ""

        if args.rg:
            node[REGION] = args.rg
            self.log.info("Validating Region in AWS cloud. This validation is being done using the region {r}".format(r=self.region))
            try:
                ec2_client = boto3.client('ec2', region_name=self.region)
                regions = ec2_client.describe_regions(
                    RegionNames=[
                        node[REGION]
                    ]
                )
                self.log.info("Region found in AWS: %s" % regions)
            except Exception as e:
                self.log.warning("\nWarning: Error in validating region. Exception is {e}".format(e=e))
                resp_msg = resp_msg + "\nWarning: Error in validating region. Exception is {e}".format(e=e)
                response['code'] = fail_response_code

        if args.t or args.r:
            node[ROUTE_TABLE_ID] = args.t
            self.log.info("Reading route table {r} in region {g}".format(r=args.t, g=args.rg))

            rt = self.get_route_table_using_ec2_client(node)
            if rt is None:
                self.log.warning("\nWarning: Route table {r} not found in region {g}".format(r=args.t, g=args.rg))
                resp_msg = resp_msg + "\nWarning: Route table {r} not found in region {g}\n".format(r=args.t, g=args.rg)
                response['code'] = fail_response_code
                if args.r:
                    self.log.warning("\nWarning: Route cannot be validated since Route table does not exist")
                    resp_msg = resp_msg + "\nWarning: Route cannot be validated since Route table does not exist"
            else:
                if args.r:
                    node[ROUTE] = args.r
                    route_found = 0
                    routes = rt['RouteTables'][0]['Routes']
                    for route in routes:
                        if 'DestinationCidrBlock' in route:
                            if route['DestinationCidrBlock'] == node[ROUTE]:
                                route_found = 1
                        if 'DestinationIpv6CidrBlock' in route:
                            if route['DestinationIpv6CidrBlock'] == node[ROUTE]:
                                route_found = 1

                    if route_found == 0:
                        self.log.warning("\nWarning: Route {r} not found in Route Table {t}".format(r=args.r, t=args.t))
                        resp_msg = resp_msg + "\nWarning: Route {r} not found in Route Table {t}".format(r=args.r, t=args.t)
                        response['code'] = fail_response_code
        if args.n:
            node[ENI_ID] = args.n
            eni = self.get_eni_id(node)
            if not eni:
                self.log.warning("\nWarning: ENI ID {e} not found in region {g}".format(e=args.n, g=args.rg))
                resp_msg = resp_msg + "\nWarning: ENI ID {e} not found in region {g}".format(e=args.n, g=args.rg)
                response['code'] = fail_response_code

        if response['code'] == 200:
            resp_msg = resp_msg + "\nAll inputs are valid\n"
        else:
            resp_msg = resp_msg + "\nPlease verify the node configuration"
        response['msg'] = resp_msg
        return json.dumps(response)

    def validate_set_param_inputs(self, node, new_params):
        self.log.info("Validating if set node parameters are valid")
        resp_msg = ""
        response, fail_response_code = self.get_response_dict()
        # for key in new_params:
        self.log.info(new_params)
        if ROUTE_TABLE_ID in new_params.keys() or ROUTE in new_params.keys():
            self.log.info("Validating if Route Table exists")
            rt = self.get_route_table_using_ec2_client(node)
            if not rt:
                if ROUTE_TABLE_ID in new_params.keys():
                    self.log.warning("\nWarning: Route table {r} not found. Please check node configuration again.".format(r=new_params[ROUTE_TABLE_ID]))
                    resp_msg = resp_msg + "\nWarning: Route table {r} not found. Please check node configuration again.".format(r=new_params[ROUTE_TABLE_ID])
                    response['code'] = fail_response_code
                if ROUTE in new_params.keys():
                    self.log.warning("\nWarning: Route cannot be validated since Route table does not exist")
                    resp_msg = resp_msg + "\nWarning: Route cannot be validated since Route table does not exist"
                    response['code'] = fail_response_code
            else:
                if ROUTE in new_params.keys():
                    self.log.info("Validating if route is valid")
                    route_found = 0
                    routes = rt['RouteTables'][0]['Routes']
                    for route in routes:
                        if 'DestinationCidrBlock' in route:
                            if route['DestinationCidrBlock'] == node[ROUTE]:
                                route_found = 1
                        if 'DestinationIpv6CidrBlock' in route:
                            if route['DestinationIpv6CidrBlock'] == node[ROUTE]:
                                route_found = 1

                    if route_found == 0:
                        self.log.warning("\nWarning: Route {r} not found. Please check node configuration again.".format(r=new_params[ROUTE]))
                        resp_msg = resp_msg + "\nWarning: Route {r} not found. Please check node configuration again.".format(r=new_params[ROUTE])
                        response['code'] = fail_response_code

        if ENI_ID in new_params.keys():
            self.log.info("Validating if ENI ID is valid")
            eni = self.get_eni_id(node)
            if not eni:
                self.log.warning("\nWarning: ENI ID {e} not found. Please check node configuration again.".format(e=new_params[ENI_ID]))
                resp_msg = resp_msg + "\nWarning: ENI ID {e} not found. Please check node configuration again.".format(e=new_params[ENI_ID])
                response['code'] = fail_response_code

        if REGION in new_params.keys():
            self.log.info("Validating Region in AWS cloud. This validation is being done using the region {r}".format(r=self.region))
            ec2_client = boto3.client('ec2', region_name=self.region)
            try:
                regions = ec2_client.describe_regions(
                    RegionNames=[
                        node[REGION]
                    ]
                )
            except Exception as e:
                self.log.warning("\nWarning: Region {g} not found. Please check node configuration again.".format(g=new_params[REGION]))
                resp_msg = resp_msg + "\nWarning: Region {g} not found. Please check node configuration again.".format(g=new_params[REGION])
                response['code'] = fail_response_code

        if response['code'] == 200:
            resp_msg = resp_msg + "All inputs are valid"
        else:
            resp_msg = resp_msg + "\nPlease verify the node configuration"

        response['msg'] = resp_msg
        return response

    def create_node(self, params):
        '''
            This node will get the additional params from the metadata server if they are not provided
        '''
        self.log.debug("creating node {p}".format(p=params))

        # At this point we don't need to modify any params but its possible that we add it in the future
        return params

    def create_node_parser(self, optional, required):
        '''
            This function will create a parser for the create_node python file in the csr_ha package
            Also includes the aws specific parameters needed
        '''

        # Required arguments

        required.add_argument('-t', help='<routetable-id> rtb-xxxxxxxx', default=None, required=True, type=self.validate_route_table_string)
        required.add_argument('-rg', help='<region> eg: us-east-1', default=None, required=True)
        required.add_argument('-n', help='<eni-id of peer> eni-xxxxxxxx', default=None, required=True, type=self.validate_eni_string)

        # Optional arguments
        optional.add_argument('-r', help='<destination cidr block> x.x.x.x/x', default=None, required=False)

    def set_node_parser(self, optional, required):
        '''
            This function will create a parser for set_node python file in the csr_ha package
        '''

        # Optional arguments
        self.create_optional_arguments(optional)

    def clear_param_parser(self, optional, required):
        '''
            This function will return a parser for clear_params python file in the csr_ha package
        '''
        # Optional arguments
        curr_action = "store_true"

        # Optional arguments
        optional.add_argument('-t', help='<routetable-id> rtb-xxxxxxxx', default=None, required=False,
                              action=curr_action)
        optional.add_argument('-rg', help='<region> eg: us-east-1', default=None, required=False,
                              action=curr_action)
        optional.add_argument('-n', help='<eni-id> eni-xxxxxxxx', default=None, required=False,
                              action=curr_action)
        optional.add_argument('-r', help='<destination cidr block> x.x.x.x/x', default=None, required=False,
                              action=curr_action)

    def check_clear_param(self, index, old_params):
        '''
            This function will return the keyword for the parameter to be deleted
        '''
        self.log.debug("check_clear_param index: {i}, params: {p}".format(i=index, p=old_params))

        keyword = self.check_param_command(old_params[index])

        return keyword

    def verify_node(self, node, event_type):
        '''
            This function will verify if the required parameters are set for a particular node for that event
        '''
        param_str = " "
        self.event_logger.info("Redundancy node configuration: ")
        for key in node:
            param_str = param_str + "{:15s}{} \n".format(key, node[key])

        self.event_logger.info(param_str)

        event_type = event_type.lower()

        # verify if for that node all parameters have been setup correctly
        if event_type == "verify" or event_type == "peerfail" or event_type == "revert":

            node_verified = True
            if ROUTE_TABLE_ID not in node:
                node_verified = False
                self.event_logger.warning("route table id has not been configured")
            if REGION not in node:
                node_verified = False
                self.event_logger.warning("region has not been configured")
            if ENI_ID not in node:
                node_verified = False
                self.event_logger.warning("eni id has not been configured")
            if ROUTE not in node:
                self.event_logger.warning("Destination cidr block has not been configured, will set all-routes")

            if node_verified is True:
                self.event_logger.info("All required parameters have been configured")
                return 'OK'
            else:
                return 'ERR1'
        else:
            self.event_logger.error("Unknown event type: {e}".format(e=event_type))
            return 'ERR1'

    def get_response_dict(self, event=None):
        # if the request is coming from validate_inputs, the return codes are successful response (200) and warning
        # response (199)
        # if the request is coming from any event for validation, the return codes are successful response (200) and
        # failed response (400) because we want to take an action based on these return codes
        response = {}
        resp_msg = ""
        success_return_code = 200
        response['code'] = success_return_code
        fail_return_code = 199
        if event:
            fail_return_code = 400
        return response, fail_return_code

    def get_eni_id(self, node, event_type=None):
        '''
        This function returns a boto3 eni object
        '''
        eni = None
        try:
            ec2_client = boto3.client('ec2', region_name=node[REGION])
            eni = ec2_client.describe_network_interfaces(
                NetworkInterfaceIds=[
                    node[ENI_ID],
                ]
            )
        except Exception as e:
            self.event_logger.exception("Exception: {ex}".format(ex=e))

        return eni

    def get_route_table_using_ec2_client(self, node):
        '''
        ec2 resource object returns the route table object even if it does not exist, which is why for validation we need to use client object
        '''
        route_table = None
        try:
            ec2_client = boto3.client('ec2', region_name=node[REGION])
            route_table = ec2_client.describe_route_tables(
                RouteTableIds=[
                    node[ROUTE_TABLE_ID],
                ]
            )
        except Exception, e:
            self.event_logger.warning("Exception: {ex}".format(ex=e))

        return route_table

    def get_route_table(self, node, event_type=None):
        '''
            This function returns a route-table boto3 resource object
        '''
        route_table = None

        try:
            if event_type and event_type == 'verify':
                self.event_logger.info("Fetching the route table")
            ec2_resource = self.get_ec2_resource(node[REGION])
            route_table = ec2_resource.RouteTable(node[ROUTE_TABLE_ID])
        except Exception, e:
            self.event_logger.exception("Exception: {ex}".format(ex=e))

        if route_table is None:
            self.event_logger.info("Route table not found: {}".format(ROUTE_TABLE_ID))
            if event_type and event_type == 'verify':
                self.event_logger.info("It is likely permission to access the route table was not granted.")
        else:
            if event_type == 'verify':
                param_str = ""
                self.event_logger.info("VpcId: {r}".format(r=route_table.vpc_id))
                self.event_logger.info("RouteTableId: {r}".format(r=route_table.route_table_id))
                self.event_logger.info("Routes in the route table: ")

                route_list = route_table.routes_attribute
                for route in route_list:
                    if 'DestinationCidrBlock' in route:
                        self.event_logger.info("CIDR: {r}".format(r=route['DestinationCidrBlock']))
                        cidr_block = route['DestinationCidrBlock']
                    if 'DestinationIpv6CidrBlock' in route:
                        self.event_logger.info("v6CIDR: {r}".format(r=route['DestinationIpv6CidrBlock']))
                        cidr_block = route['DestinationIpv6CidrBlock']
                    if 'NetworkInterfaceId' in route:
                        self.event_logger.info("ENI: {r}".format(r=route['NetworkInterfaceId']))
                        next_hop = route['NetworkInterfaceId']
                    elif 'GatewayId' in route:
                        self.event_logger.info("GW: {r}".format(r=route['GatewayId']))
                        next_hop = route['GatewayId']

                    param_str += "{:15s}{} \n".format(cidr_block, next_hop)

                self.event_logger.info(param_str)

        return route_table

    def set_route_table(self, node, event_type, route_table):
        '''
            This function will update the route table for different event types
        '''
        self.event_logger.debug("Setting route table for node: {n} , event_type: {e}".format(
                n=node, e=event_type))
        response_code = 400
        try:

            if route_table is None:
                self.event_logger.error("Route table object is not set, cannot update the table")
                return None

            send_request = False

            # Event type code exists for csr_ha to control the behavior of set_route_table function in the future
            event_type = event_type.lower()
            if event_type == "verify":
                self.event_logger.debug("route_table: {r}".format(r=route_table))
                send_request = True
            elif event_type == "peerfail":
                send_request = True
            elif event_type == "revert":
                if MODE in node:
                    if node[MODE] == PRIMARY:
                        send_request = True
            else:
                self.event_logger.error("Incorrect event type: {e}".format(e=event_type))

                return None

            responses = []

            if send_request is True:
                # Get all the routes from the route table
                routes = route_table.routes_attribute
                next_hop = None
                if routes:
                    if ROUTE in node:
                        # Set one specific route
                        response_code = self.set_one_route(node, route_table, event_type)
                    else:
                        # Set all routes
                        response_code = self.set_all_routes(node, routes, event_type)
            else:
                self.delete_log_file_revert(event_type)

            return response_code

        except Exception, e:
            self.event_logger.exception("Exception: {ex}".format(ex=e))

    def check_cloud_command(self, cmd):
        '''
            This function checks the cloud commands passed through to the cloud specific layer
        '''

        keyword = self.check_param_command(cmd)
        return keyword

    def validate_nexthop(self, nexthop):
        '''
            This function will return True if csr_ha has to validate nexthop ip otherwise return False
        '''

        # For aws, currently next hop is going to be only an ENI-ID, thus we don't have an ip to validate
        return False

    def set_event_logger(self, node, event_type, directory_name=EVENT_LOGS):
        '''
            This function will set the event_logger for ha
        '''

        self.event_logger = self.create_event_logger(node, event_type, directory_name)

    '''
        Functions implemented as helpers to the above api's
    '''

    def get_ec2_resource(self, region):
        '''
            This function returns the boto3 ec2 resource
        '''

        ec2_resource = boto3.resource('ec2', region_name=region)
        return ec2_resource

    def create_optional_arguments(self, optional, store_values=False):
        '''
            This function will return the optional arguments for the parser
        '''

        curr_action = None

        if store_values:
            curr_action = "store_true"

        # Optional arguments
        optional.add_argument('-t', help='<routetable-id> rtb-xxxxxxxx', default=None, required=False,
                              action=curr_action, type=self.validate_route_table_string)
        optional.add_argument('-rg', help='<region> eg: us-east-1', default=None, required=False,
                              action=curr_action)
        optional.add_argument('-n', help='<eni-id> eni-xxxxxxxx', default=None, required=False,
                              action=curr_action, type=self.validate_eni_string)
        optional.add_argument('-r', help='<destination cidr block> x.x.x.x/x', default=None, required=False,
                              action=curr_action)

    def check_param_command(self, cmd):
        '''
            This function is a common function for check_cloud_command and check_clear_param
        '''

        keyword = ""
        if cmd == '-t':
            keyword = ROUTE_TABLE_ID
        elif cmd == '-rg':
            keyword = REGION
        elif cmd == '-n':
            keyword = ENI_ID
        elif cmd == '-r':
            keyword = ROUTE
        else:
            self.log.error("Invalid parameter/command format {c}".format(c=cmd))
            return "Error"

        return keyword

    def set_one_route(self, node, route_table, event_type):
        '''
            This function will set the given route to a given next hop eni
        '''

        # Update the route for the given route cidr only if the eni_id is not our own
        response = []
        sent_request = False
        rsp_code = 400

        routes = route_table.routes_attribute
        for route in routes:
            self.event_logger.info("In set_one_route Route {}".format(route))
            ipv6_route =  False
            if 'DestinationIpv6CidrBlock' in route:
                cidr_block = route['DestinationIpv6CidrBlock']
                ipv6_route = True
            elif 'DestinationCidrBlock' in route:
                cidr_block = route['DestinationCidrBlock']

            if cidr_block == node[ROUTE]:
                if 'NetworkInterfaceId' in route:
                    current_next_hop = route['NetworkInterfaceId']
                    ec2_client = boto3.client('ec2', region_name=node[REGION])
                    if current_next_hop != node[ENI_ID] and event_type != 'verify':
                        self.event_logger.info("Replacing the network interface id {} for route: {}".format(node[ENI_ID], cidr_block))
                        if ipv6_route:
                            resp = ec2_client.replace_route(RouteTableId=node[ROUTE_TABLE_ID], DestinationIpv6CidrBlock=cidr_block, NetworkInterfaceId=node[ENI_ID])
                        else:
                            resp = ec2_client.replace_route(RouteTableId= node[ROUTE_TABLE_ID], DestinationCidrBlock=cidr_block, NetworkInterfaceId=node[ENI_ID])
                        response.append(resp)
                        sent_request = True
                    elif event_type == 'verify':
                        self.event_logger.info("Verifying the network interface id {} for route {}".format(current_next_hop, cidr_block))
                        if ipv6_route:
                            resp = ec2_client.replace_route(RouteTableId=node[ROUTE_TABLE_ID], DestinationIpv6CidrBlock=cidr_block, NetworkInterfaceId=current_next_hop)
                        else:
                            resp = ec2_client.replace_route(RouteTableId= node[ROUTE_TABLE_ID], DestinationCidrBlock=cidr_block, NetworkInterfaceId=current_next_hop)
                        response.append(resp)
                        sent_request = True
                        self.event_logger.info("Response for verify event: {}".format(response))
                    elif event_type == 'peerFail':
                        self.event_logger.info("Route is already updated. No write performed.")
                break

        # Delete log file if it was just a revert event where we did not send a request out
        if not sent_request:
            self.delete_log_file_revert(event_type)

        if event_type == 'verify':
            self.event_logger.info("Set route(s) response")
            self.event_logger.info(response)

        # The response is a list of 1 entry. The entry is a dictionary with 1 key.
        # The value for the 1 key is a dictionary with 4 keys.
        if response:
            rsp_dict = response[0]
            rsp_value = rsp_dict['ResponseMetadata']
            rsp_code = rsp_value['HTTPStatusCode']
            if rsp_code == 200:
                if event_type == 'verify':
                    self.event_logger.info("Verify event completed successfully")
                else:
                    self.event_logger.info("Set route completed successfully")
            else:
                if event_type == 'verify':
                    self.event_logger.info("Verify route failed with error %d" % rsp_code)
                else:
                    self.event_logger.info("Set route failed with error %d" % rsp_code)
                    self.event_logger.info(response)

        return rsp_code

    def set_all_routes(self, node, routes, event_type):
        '''
            In case we don't have a CIDR, then we need to set the entire route table to the given next hop eni
        '''
        return_code = 200
        if event_type == "verify":
            sent_request = True
        else:
            sent_request = False

        # Get a boto3 client
        ec2_client = boto3.client('ec2', region_name=node[REGION])

        # Try to replace all routes irrespective of any errors that you might get.
        # Note: AWS does not allow you to modify the local route to point to an eni-id
        for route in routes:
            response = []
            try:
                # Only update the routes which don't have a gateway id (local or igw)
                if 'GatewayId' in route:
                    self.event_logger.warning("Cannot replace route for gatewayid: {r}".format(r=route['GatewayId']))
                elif 'NetworkInterfaceId' in route:
                    # Check if the network ID in the node is different from the ID in the route
                    if route['NetworkInterfaceId'] != node[ENI_ID]:
                        if event_type == "verify":
                            # Don't change the next hop for the route
                            next_hop = route['NetworkInterfaceId']
                        else:
                            # Replace the next hop interface with the value in the node
                            next_hop = node[ENI_ID]

                        if 'DestinationCidrBlock' in route:
                            self.event_logger.info("Updating {} with nextHop {} for the {} event".format(route['DestinationCidrBlock'], next_hop, event_type))
                            response = ec2_client.replace_route(RouteTableId=node[ROUTE_TABLE_ID], DestinationCidrBlock=route['DestinationCidrBlock'], NetworkInterfaceId=next_hop)
                        elif 'DestinationIpv6CidrBlock' in route:
                            self.event_logger.info("Updating {} with nextHop {} for the {} event".format(route['DestinationIpv6CidrBlock'], next_hop, event_type))
                            response = ec2_client.replace_route(RouteTableId=node[ROUTE_TABLE_ID], DestinationIpv6CidrBlock=route['DestinationIpv6CidrBlock'], NetworkInterfaceId=next_hop)
                        else:
                            self.event_logger.info("Destination CIDR block not found in route")

                        sent_request = True
                        if event_type == "verify":
                            self.event_logger.info("Set route response")
                            self.event_logger.info(response)
                    else:
                        # Network interface in the route is the same as in the node
                        # No need to update route table entry
                        if 'DestinationCidrBlock' in route:
                            self.event_logger.info("Nexthop to {} already set to {}, no update required".format(route['DestinationCidrBlock'], route['NetworkInterfaceId']))
                        elif 'DestinationIpv6CidrBlock' in route:
                            self.event_logger.info("Nexthop to {} already set to {}, no update required".format(route['DestinationIpv6CidrBlock'], route['NetworkInterfaceId']))
                else:
                    self.event_logger.error("Route without gateway or network interface ignored")

                # The response is a dictionary with 1 key.
                # The value for the 1 key is a dictionary with 4 keys.
                if response:
                    rsp_value = response['ResponseMetadata']
                    rsp_code = rsp_value['HTTPStatusCode']
                    if rsp_code == 200:
                        if event_type == 'verify':
                            self.event_logger.info("Route verify completed successfully")
                        else:
                            self.event_logger.info("Set route completed successfully")
                    else:
                        response_code = rsp_code
                        if event_type == 'verify':
                            self.event_logger.info("Verify route failed with error %d" % rsp_code)
                        else:
                            self.event_logger.info("Set route failed with error %d" % rsp_code)
                            self.event_logger.info(response)

            except Exception as e:
                self.event_logger.exception("Could not update the route in the route table: {exp}".format(exp=e))

        # Delete log file if it was just a revert event where we did not send a request out
        if not sent_request:
            self.delete_log_file_revert(event_type)

        return return_code

    def get_cidr_block(self, route):
        '''
            This function will return the cidr block depending on whether the given address is ipv4 or ipv6
        '''

        if route is None:
            return ""

        cidr_block = ""

        if 'DestinationCidrBlock' in route:
            cidr_block = route['DestinationCidrBlock']
        elif 'DestinationIpv6CidrBlock' in route:
            cidr_block = route['DestinationIpv6CidrBlock']

        return cidr_block


    def create_event_logger(self, node, event_type, directory_name):
        '''
            This function will create the event logger
        '''

        # Create the logger for events
        logger = logging.getLogger("ha.events")

        # Name the log file
        log_file = "node_" + str(node['index']) + "_" + str(
            datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")) + "_" + event_type

        # save the file path so that we can remove the file in-case of unnecessary reverts
        self.event_log_file = os.path.join(directory_name, log_file)

        # Roll over if the number of event files exceeds 513 count
        if len(os.listdir(directory_name)) > 512:
            filetoremove = os.popen("ls -t " + directory_name + "|  tail -1").read().strip()
            self.log.info('Event files threshold exceeded. Removing event file: "{}"'.format(
                os.path.join(directory_name, filetoremove).strip()))
            command = "rm {}".format(os.path.join(directory_name, filetoremove))
            os.system(command)

        # Create the file handler
        handler = logging.FileHandler(filename=os.path.join(directory_name, log_file), mode='a')
        # Add Handler
        if not len(logger.handlers):
            logger.addHandler(handler)

        return logger

    def delete_log_file_revert(self, event_type):
        '''
            This function will delete the file if its a revert and we have elected to not send the
            request out to AWS
        '''

        if event_type == REVERT:
            if os.path.exists(self.event_log_file):
                self.event_logger.info("deleting log file for event_type: {e}, file path: {f}".format(e=event_type, f=self.event_log_file))
                os.remove(self.event_log_file)

    # Taking cloud's input if a revert event is needed if none of nodes are configured as Primary
    def do_revert(self):
        return False

