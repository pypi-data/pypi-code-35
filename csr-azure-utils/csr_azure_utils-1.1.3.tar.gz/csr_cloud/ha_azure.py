import os
import sys
import requests
import urllib
from os.path import expanduser
from token_api import Token_api as token_api
from meta_utils import MetaDataUtils as Metadata
import logging
import ipaddress
from logging.handlers import RotatingFileHandler
import datetime
import json
import shutil

log = logging.getLogger('HA')
log.setLevel(logging.INFO)

home = expanduser("~")
event_dir = "%s/cloud/HA/events" % home


class csr_ha():
    def __init__(self):                                                                 #pragma nocover
        self.cert_file = "/etc/ssl/certs/ca-bundle.trust.crt"
        sys.path.append(home + '/.local/lib/python2.7/site-packages/csr_ha/client_api')
        sys.path.append(home + '.local/lib/python2.7/site-packages/csr_ha/server')

        # Setting event_logger for route events for fail-safe approach
        # Ideally csr_ha is responsible for setting it up using set_event_logger
        self.event_logger = log
        self.event_log_file = ""

        if os.path.exists("/home/guestshell/cloud/HA/csr_ha.log"):
            if os.path.getsize("/home/guestshell/cloud/HA/csr_ha.log") > 15000000:
                shutil.copy('/home/guestshell/cloud/HA/csr_ha.log', '/bootflash/csr_ha.log')
                os.remove('/home/guestshell/cloud/HA/csr_ha.log')


    def create_event_logger(self, node, event_type, directory_name):
        '''
            This function will create the event logger
        '''

        # Create the logger for events
        logger = logging.getLogger("HA.events")

        # Name the log file
        log_file = "node_" + str(node['index']) + "_" + str(
            datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")) + "_" + event_type

        # save the file path so that we can remove the file in-case of unnecessary reverts
        self.event_log_file = os.path.join(directory_name, log_file)

        # Roll over if the number of event files exceeds 513 count
        if len(os.listdir(directory_name)) > 512:
            filetoremove = os.popen("ls -t " + directory_name + "|  tail -1").read().strip()
            log.info('Event files threshold exceeded. Removing event file: "{}"'.format(os.path.join(directory_name, filetoremove).strip()))
            command = "rm {}".format(os.path.join(directory_name, filetoremove))
            os.system(command)

        # Create the file handler
        handler = logging.FileHandler(filename=os.path.join(directory_name, log_file), mode='a')

        log.info("Created event_log file: {} for node {} {} event".format(self.event_log_file, node['index'], event_type))
        # Add Handler
        if not len(logger.handlers):
            logger.addHandler(handler)

        return logger

    def set_event_logger(self, node, event_type, directory_name=event_dir):
        '''
            This function will set the event_logger for ha
        '''

        self.event_logger = self.create_event_logger(node, event_type, directory_name)


    def obtain_token(self, node, event_type):
        # connect to the token manager

        rc = token_api()
        token = ""
        server_status = rc.is_server_up()

        if server_status != 0:
            self.event_logger.info("failed connection to token manager rc=%d" % rc)
            sys.exit()

        if 'appId' in node:
            # appid has been specified. use aad to get a token
            token = rc.get_token_with_params(node['cloud'],
                                             node['tenantId'],
                                             node['appId'],
                                             node['appKey'])
            self.event_logger.info("requesting token using Azure Active Directory")
            if event_type == 'verify':
                self.event_logger.info("token=%s" % token)

            if token is "":
                self.event_logger.info("failed to obtain token using AAD")

        else:
            # no appid specified.  use msi to get token.
            token = rc.get_token()
            self.event_logger.info("Requesting token from default authentication application")
            if event_type == 'verify':
                self.event_logger.info("token=%s" % token)

            if token is "":
                self.event_logger.info("failed to obtain token using default application")

        rc.disconnect()
        if token == '':
            self.event_logger.info("failed to obtain token")
        return token


    def get_route_table(self, node, event_type=None):

        self.event_logger.info("Requesting token for fetching the routes from route table")
        token = self.obtain_token(node, event_type)
        total_nodes = ""

        if token == "":
            self.event_logger.error("Failed to obtain token")
            return None
        else:
            self.event_logger.info("Obtained token successfully")

        # Specify the HTTP GET request to read the route table
        apiversion = "2017-10-01"
        auth_header = "Bearer " + token
        all_headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Accept': 'application/json',
                       'Authorization': auth_header}

        if node['cloud'] == 'azure':
            url = "https://management.azure.com/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/routeTables/%s?api-version=%s" % (
                node['subscriptionId'], node['resourceGroup'], node['routeTableName'], apiversion)
        elif node['cloud'] == 'azusgov':
            url = "https://management.usgovcloudapi.net/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/routeTables/%s?api-version=%s" % (
                node['subscriptionId'], node['resourceGroup'], node['routeTableName'], apiversion)
        elif node['cloud'] == 'azchina':
            url = "https://management.chinacloudapi.cn/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/routeTables/%s?api-version=%s" % (
                node['subscriptionId'], node['resourceGroup'], node['routeTableName'], apiversion)
        else:
            self.event_logger.error("Unknown cloud name %s" % node['cloud'])
            return None

        # Send the HTTP GET request for the route table
        try:
            response = requests.get(url, verify=self.cert_file, headers=all_headers)
        except requests.exceptions.RequestException as e:
            self.event_logger.error("get_route_table: request had error %s" % e)
            return None

        if event_type == 'verify':
            # Write the HTTP GET response to the event file for debugging purposes
            self.event_logger.info("Fetching the route table")
            self.event_logger.info("Route table get response:\n {r}".format(r=response.text))

        if 200 == response.status_code:
            self.event_logger.info("Read route table successfully")
        else:
            self.event_logger.error("Route GET request failed with code %d" % response.status_code)
            self.event_logger.info("Route table get response:\n {r}".format(r=response.text))
            return None

        # Extract the routes section from the table
        route_table = response.json()
        routes = route_table['properties']['routes']

        if routes == '':
            self.event_logger.error("No routes found in table")
            self.event_logger.error("Get route response:\n{r}".format(r=route_table))
            return None

        total_routes = ""
        for i, route in enumerate(route_table["properties"]["routes"]):
            total_routes +="\n{:20s}{}".format(str(route['properties']['addressPrefix']), str(route['properties']['nextHopIpAddress']))
        if event_type == 'verify':
            self.event_logger.info("\nRoutes on route table {}:  {}\n".format(node['routeTableName'], total_routes))
        return route_table


    def set_one_route(self, node, event_type, route_table):
        self.event_logger.info("Requesting token for setting the route")
        token = self.obtain_token(node, event_type)

        if token == "":
            self.event_logger.error("Failed to obtain token")
            return
        else:
            self.event_logger.info("Obtained token successfully")

        if event_type == 'verify':
            self.event_logger.info("Evaluating single route in route table for event type %s" % event_type)

        if route_table == '':
            self.event_logger.info("No route table entries found")
            if event_type == 'verify':
                self.event_logger.info("It is likely permission to access the route table was not granted.")
            return

        send_request = False
        found_route = False

        # Walk through all the routes in the current route table
        for i, route in enumerate(route_table["properties"]["routes"]):
            if route['properties']['nextHopType'] == 'VirtualAppliance':
                # Updating a single route in the table.  Need to find the right one.
                if node['route'] == route['properties']['addressPrefix']:
                    # This is the one
                    found_route = True
                    if event_type == 'verify':
                        # Don't change the route
                        newNextHop = route['properties']['nextHopIpAddress']
                        send_request = True
                    elif event_type == 'peerFail':
                        newNextHop = node['nextHop']
                        send_request = True
                    elif event_type == 'revert':
                        newNextHop = node['nextHop']
                        if 'mode' in node:
                            if node['mode'] == 'primary':
                                if route['properties']['nextHopIpAddress'] != node['nextHop']:
                                    send_request = True
                                    self.event_logger.info("Revert: updating %s with nextHop %s as mode configured for primary" %
                                        (route['properties']['addressPrefix'], node['nextHop']))
                    else:
                        self.event_logger.error("Invalid event type %s in set_route_table" % event_type)
                        return
                    break

        if send_request == False:
            if event_type == 'verify':
                self.event_logger.info("Verify event: No need to update single route in route table")
                return
            if event_type == 'revert':
                # No action taken by this revert event. Delete the event log file
                log.info("Removing the event_log_file: {}".format(self.event_log_file))
                os_command = "rm \"%s\"" % self.event_log_file
                os.system(os_command)
                return

        # Did we find the route?
        if found_route == False:
            self.event_logger.error("Did not find route %s event type %s" % (node['route'], event_type))
            return

            # Specify the HTTP PUT request to write the route table
        # Set the URL
        apiversion = "2017-10-01"
        if node['cloud'] == 'azure':
            url = "https://management.azure.com/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/routeTables/%s/routes/%s?api-version=%s" % (
                node['subscriptionId'], node['resourceGroup'], node['routeTableName'], route['name'], apiversion)
        elif node['cloud'] == 'azusgov':
            url = "https://management.usgovcloudapi.net/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/routeTables/%s/routes/%s?api-version=%s" % (
                node['subscriptionId'], node['resourceGroup'], node['routeTableName'], route['name'], apiversion)
        elif node['cloud'] == 'azchina':
            url = "https://management.chinacloudapi.cn/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/routeTables/%s/routes/%s?api-version=%s" % (
                node['subscriptionId'], node['resourceGroup'], node['routeTableName'], route['name'], apiversion)

        else:
            self.event_logger.error("Unknown cloud name %s" % node['cloud'])
            return
            # Set the headers
        auth_header = "Bearer " + token
        all_headers = {'Content-Type': 'application/json',
                       'Accept': 'application/json',
                       'Authorization': auth_header}

        # Build the payload
        payload = "{\"properties\":{\"addressPrefix\":\"%s\", \"nextHopType\":\"%s\", \"nextHopIpAddress\":\"%s\"}}" % (
            route['properties']['addressPrefix'], route['properties']['nextHopType'], newNextHop)

        if event_type == 'verify':
            self.event_logger.info("Updating single route in route table")
            self.event_logger.info("URL=%s" % url)
            for key in all_headers:
                self.event_logger.info("%s:%s" % (key, all_headers[key]))
            self.event_logger.info("Payload=%s" % payload)

        # Send the PUT request
        try:
            response = requests.put(url, data=payload, verify=self.cert_file, headers=all_headers)
        except requests.exceptions.RequestException as e:
            self.event_logger.error("set_one_route: request had error %s" % e)
            return

        write_rsp_to_file = False
        if 200 == response.status_code:
            self.event_logger.info("HTTP PUT of route table was successful")
            self.event_logger.info("Updated route %s to %s" % (route['name'], newNextHop))
            # Write the HTTP SET response to a file for debugging purposes
            if event_type == 'verify':
                write_rsp_to_file = True

            # Extract the routes section from the table
            put_response = response.json()
            provisionState = put_response['properties']['provisioningState']

            if event_type == 'verify':
                self.event_logger.info("Set route provision state is %s" % provisionState)

            if provisionState == 'Failed':
                self.event_logger.error("Set route provisioning state failed")
                write_rsp_to_file = True
        else:
            self.event_logger.error("Set route failed for route %s code=%d" %
                          (route['name'], response.status_code))
            write_rsp_to_file = True

        if write_rsp_to_file == True:
            self.event_logger.info("Set route response")
            self.event_logger.info(response.text)

        return response.status_code


    def set_all_routes(self, node, event_type, route_table):
        self.event_logger.info("Requesting token for setting all routes in the route table")
        token = self.obtain_token(node, event_type)

        if token == "":
            self.event_logger.error("Failed to obtain token")
            return
        else:
            self.event_logger.info("Obtained token successfully")
        if event_type == 'verify':
            self.event_logger.info("Evaluating all routes in route table for event type %s" % event_type)

        send_request = False

        if route_table == '':
            self.event_logger.info("No route table entries found")
            if event_type == 'verify':
                self.event_logger.info("It is likely permission to access the route table was not granted.")
            return

        # The etag can contain quotation marks which must be escaped
        current_etag = route_table['etag']
        new_etag = ''
        tag_len = len(current_etag)
        for i in range(tag_len):
            if current_etag[i] == '\"':
                new_etag = new_etag + '\\'
            new_etag = new_etag + current_etag[i]

        payload = "{\"location\":\"%s\", \"etag\":\"%s\", \"properties\":{\"routes\":[" % (
            route_table['location'], new_etag)

        # Walk through all the routes in the current route table
        routes = route_table['properties']['routes']
        for i, route in enumerate(routes):
            if route['properties']['nextHopType'] == 'VirtualAppliance':
                if event_type == 'verify':
                    # Don't change the route
                    newNextHop = route['properties']['nextHopIpAddress']
                    send_request = True
                elif event_type == 'peerFail':
                    newNextHop = node['nextHop']
                    send_request = True
                elif event_type == 'revert':
                    newNextHop = node['nextHop']
                    if 'mode' in node:
                        if node['mode'] == 'primary':
                            if route['properties']['nextHopIpAddress'] != node['nextHop']:
                                send_request = True
                                self.event_logger.info("Revert: updating %s with nextHop %s as mode configured for primary" %
                                    (route['properties']['addressPrefix'], node['nextHop']))

                else:
                    self.event_logger.error(" Invalid event type %s in set_route_table" % event_type)
                    return

                payload = payload + "{\"name\":\"%s\", \"id\":\"%s\", \"properties\":{\"addressPrefix\":\"%s\", \"nextHopType\":\"%s\", \"nextHopIpAddress\":\"%s\"}}," % (
                    route['name'], route['id'], route['properties']['addressPrefix'], route['properties']['nextHopType'],
                    newNextHop)

            else:
                # These route types have no explicit next hop IP address
                payload = payload + "{\"name\":\"%s\", \"id\":\"%s\", \"properties\":{\"addressPrefix\":\"%s\", \"nextHopType\":\"%s\"}}," % (
                    route['name'], route['id'], route['properties']['addressPrefix'], route['properties']['nextHopType'])

        payload = payload + ']}}'

        if send_request == False:
            if event_type == 'verify':
                self.event_logger.info("No need to update any routes in route table")
            if event_type == 'revert':
                # No action taken by this revert event. Delete the event log file
                os_command = "rm \"%s\"" % self.event_log_file
                os.system(os_command)
            return

            # Specify the HTTP PUT request to write the route table
        # Set the URL
        apiversion = "2017-10-01"
        if node['cloud'] == 'azure':
            url = "https://management.azure.com/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/routeTables/%s?api-version=%s" % (
                node['subscriptionId'], node['resourceGroup'], route_table['name'], apiversion)
        elif node['cloud'] == 'azusgov':
            url = "https://management.usgovcloudapi.net/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/routeTables/%s?api-version=%s" % (
                node['subscriptionId'], node['resourceGroup'], route_table['name'], apiversion)
        elif node['cloud'] == 'azchina':
            url = "https://management.chinacloudapi.cn/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/routeTables/%s?api-version=%s" % (
                node['subscriptionId'], node['resourceGroup'], route_table['name'], apiversion)
        else:
            self.event_logger.error("Unknown cloud name %s" % node['cloud'])
            return

            # Set the headers
        auth_header = "Bearer " + token
        all_headers = {'Content-Type': 'application/json',
                       'Accept': 'application/json',
                       'Authorization': auth_header}
        if event_type == 'verify':
            self.event_logger.info("URL=%s" % url)
            self.event_logger.info("Headers=%s" % all_headers)
            self.event_logger.info("Payload=%s" % payload)

        # Send the PUT request
        self.event_logger.info("Updating all routes in route table")
        try:
            response = requests.put(url, headers=all_headers, data=payload, verify=self.cert_file)
        except requests.exceptions.RequestException as e:
            self.event_logger.error("set_all_routes: request had error %s" % e)
            return

        write_rsp_to_file = False
        if 200 == response.status_code:
            # Write the HTTP SET response to a file for debugging purposes
            self.event_logger.info("HTTP PUT of route table was successful")
            self.event_logger.info("Updated all routes in table %s to %s" %
                          (node['routeTableName'], newNextHop))
            if event_type == 'verify':
                write_rsp_to_file = True

            # Extract the routes section from the table
            put_response = response.json()
            provisionState = put_response['properties']['provisioningState']

            if event_type == 'verify':
                self.event_logger.info("Set route provision state is %s" % provisionState)

            if provisionState == 'Failed':
                self.event_logger.error("Set route provisioning state failed")
                write_rsp_to_file = True
        else:
            self.event_logger.error("Failed to set all routes in table %s code=%d" %
                          (node['routeTableName'], response.status_code))
            write_rsp_to_file = True

        write_rsp_content = ""
        if write_rsp_to_file == True:
            self.event_logger.info("Set route response:\n%s" % response.txt)

        return response.status_code


    def set_route_table(self, node, event_type, route_table):
        # Are we changing all route entries, or just a specific one?
        if not route_table:
            self.event_logger.error("Route Table not found")
            rsp_code = 404

        if 'route' in node:
            # Updating a specific route in the table
            rsp_code = self.set_one_route(node, event_type, route_table)
            return rsp_code
        else:
            # Updating all routes in the table
            rsp_code = self.set_all_routes(node, event_type, route_table)
            return rsp_code


    def verify_node(self, node, event_type):
        param_str = " "
        self.event_logger.info("Redundancy node configuration: ")
        for key in node:
            param_str = param_str + "{:15s}{} \n".format(key, node[key])
        self.event_logger.info(param_str)

        if event_type == 'verify':
            node_verified = True
            if (not (node.has_key('cloud'))):
                self.event_logger.info("Missing required parameter -p cloud")
                node_verified = False
            if (not (node.has_key('subscriptionId'))):
                self.event_logger.info("Missing required parameter -s subscriptionId")
                node_verified = False
            if (not (node.has_key('resourceGroup'))):
                self.event_logger.info("Missing required parameter -g resourceGroup")
                node_verified = False
            if (not (node.has_key('routeTableName'))):
                self.event_logger.info("Missing required parameter -t routeTableName")
                node_verified = False
            if (not (node.has_key('nextHop'))):
                self.event_logger.info("Missing required parameter -n nextHopIpAddress")
                node_verified = False
            if node.has_key('appId'):
                if (not (node.has_key('tenantId'))):
                    self.event_logger.info("Missing required parameter -d tenantId")
                    node_verified = False
                if (not (node.has_key('appKey'))):
                    self.event_logger.info("Missing required parameter -k applicationKey")
                    node_verified = False

            if node_verified:
                self.event_logger.info("All required parameters have been provided")
                return 'OK'
            else:
                return 'ERR1'
        else:
            if ((node.has_key('index')) and
                    (node.has_key('cloud')) and
                    (node.has_key('routeTableName')) and
                    (node.has_key('subscriptionId')) and
                    (node.has_key('resourceGroup')) and
                    (node.has_key('nextHop'))):

                if node.has_key('appId'):
                    if (not (node.has_key('tenantId'))):
                        return "ERR1"
                    elif (not (node.has_key('appKey'))):
                        return "ERR1"
                return 'OK'
            else:
                self.event_logger.info("verify_node: missing required parameter")
                return "ERR1"

    def check_cloud_command(self, cmd):
        i = 1
        keyword = ""
        if cmd == '-s':
            keyword = "subscriptionId"
        elif cmd == '-r':
            keyword = 'route'
        elif cmd == '-p':
            keyword = "cloud"
        elif cmd == '-n':
            keyword = "nextHop"
        elif cmd == '-g':
            keyword = "resourceGroup"
        elif cmd == '-t':
            keyword = "routeTableName"
        elif cmd == '-a':
            keyword = "appId"
        elif cmd == '-d':
            keyword = "tenantId"
        elif cmd == '-k':
            keyword = "appKey"
        else:
            log.error("Invalid command format %s" % cmd)
            print "Invalid command format %s" % cmd
            return "Error"

        return keyword


    def create_node(self, params):
        # Make any cloud specific changes to the parameters
        node = params

        if params.has_key('appKey'):
            # Check if the key is URL encoded. If so, decode it.
            app_key = params['appKey']
            if len(app_key) > 44 and app_key.count('%') > 0:
                node['appKey'] = urllib.unquote(app_key)

        return node


    def check_clear_param(self, index,old_params):

        keyword = " "
        if old_params[index] == '-r':
            keyword = "route"
        elif old_params[index] == '-s':
            keyword = "subscriptionId"
        elif old_params[index] == '-g':
            keyword = "resourceGroup"
        elif old_params[index] == '-t':
            keyword = "routeTableName"
        elif old_params[index] == '-a':
            keyword = "appId"
        elif old_params[index] == '-n':
            keyword = "nextHop"
        elif old_params[index] == '-d':
            keyword = "tenantId"
        elif old_params[index] == '-k':
            keyword = "appKey"
        else:
            log.info("Invalid parameter format %s" % old_params[index])

        return keyword

    def clear_param_parser(self, optional, required):

        optional.add_argument('-n', help='to clear the nextHopIpAddress', default=None, action="store_true")
        optional.add_argument('-s', help='to clear the subscriptionId', default=None, action="store_true")
        optional.add_argument('-g', help='to clear the resourceGroup', default=None, action="store_true")
        optional.add_argument('-t', help='to clear the routeTableName', default=None, action="store_true")
        optional.add_argument('-a', help='to clear the applicationId', default=None, action="store_true")
        optional.add_argument('-d', help='to clear the tenantId', default=None, action="store_true")
        optional.add_argument('-k', help='to clear the applicationKey', default=None, action="store_true")
        optional.add_argument('-r', help='to clear the route', default=None, action="store_true")



    def create_node_parser(self, optional, required):

        required.add_argument('-p', help='<cloud_provider>   {azure | azusgov | azchina}', choices=['azure', 'azusgov', 'azchina'],
                              default=None, required=True)
        required.add_argument('-n', help='<nextHopIpAddress>', default=None, required=True)
        required.add_argument('-t', help='<routeTableName>', default=None, required=True)
        optional.add_argument('-s', help='<subscriptionId>', default=None)
        optional.add_argument('-g', help='<resourceGroup>', default=None)
        optional.add_argument('-r', help='<route>   e.g. 15.0.0.0/8', default=None)
        optional.add_argument('-a', help='to add the applicationId', default=None)
        optional.add_argument('-d', help='to add the tenantId', default=None)
        optional.add_argument('-k', help='to add the applicationKey', default=None)

    def validate_inputs(self, args):
        response = {}
        resp_msg = '''Please make sure you have MSI (Managed service identity) feature available 
in this region of Azure and it is configured to allow this CSR VM an contributer/network contributor 
access to the route table to be able to change the routes. At last, please do 
'node_event.py -i {} -e verify' to verify node is configured correctly.\n
            '''.format(str(args.i))
        response['code'] = 200
        response['msg'] = ""

        #Returning if Subscription ID is missing
        if not args.s or not args.g:
            response['code'] = 199
            response['msg'] = "Unable to validate nodes. Please verify node configuration."
            if not args.s:
                response['msg'] = response['msg'] + "\n199: subscriptionId is not found in input parameters. Please configure valid subscriptionId using set_params.py client_api"
            if not args.g:
                response['msg'] = response['msg'] + "\n199: resourceGroup is not found in input parameters. Please configure valid resourceGroup using set_params.py client_api"
            return json.dumps(response)

        if (not args.a or not args.s or not args.d or not args.k) and args.p != 'azure':
            log.warning(resp_msg)
            response['code'] = 199
            response['msg'] = resp_msg

        node = self.create_node_from_args(args)

        foundRoute = False
        routetable = self.get_route_table(node)
        if routetable is not None:
            # Walk through all the routes in the current route table
            if args.r:
                for i, route in enumerate(routetable["properties"]["routes"]):
                    if route['properties']['nextHopType'] == 'VirtualAppliance':
                        # Updating a single route in the table.  Need to find the right one.
                        if node['route'] == route['properties']['addressPrefix']:
                                foundRoute = True
                if foundRoute:
                    response['msg'] += "Verified route {} is present in the routetable".format(node['route'])
                else:
                    response['code'] = 199
                    response['msg'] += "Route {} is not found in the routetable".format(node['route'])

            # checking if the node configured is for all routes
            else:
                response['code'] = 200
                response['msg'] += "Verified node configuration can fetch all routes in routetable"

        else:
            response['code'] = 199
            response['msg'] = "Unable to validate nodes, please verify the node configuration"
        return json.dumps(response)

    def set_node_parser(self,  optional, required):

        optional.add_argument('-s', help='to set the subscriptionId', default=None)
        optional.add_argument('-r', help='to set the route', default=None)
        optional.add_argument('-g', help='to set the resourceGroup', default=None)
        optional.add_argument('-t', help='to set the routeTableName', default=None)
        optional.add_argument('-n', help='to set the nextHopIpAddress', default=None)
        optional.add_argument('-a', help='to set the applicationId', default=None)
        optional.add_argument('-d', help='to set the tenantId', default=None)
        optional.add_argument('-k', help='to set the applicationKey', default=None)


    def validate_nexthop(self, nextHop):
        '''
        This method is used to validate if the nextHop is in the right IP format
        :param nextHop:
        :return: Returns 0 or 1 based on the nextHop
        '''
        try:
            ipaddress.ip_address(unicode(nextHop))
            return 0
        except Exception as e:
            return 1

    # def validate_string(self, resourceInput):
    #     '''
    #     Validating the ResourceGroup naming conventions
    #     :param resourceInput:
    #     :return:
    #     '''
    #     if re.match(r"^[\w\._\(\)]+$", resourceInput):
    #         log.info("Validated the input: {}".format(resourceInput))
    #         return resourceInput
    #     else:
    #         raise argparse.ArgumentTypeError("Not in a alphanumeric, underscore, parentheses, hyphen, period (except at end), and Unicode characters format")

    def create_node_from_args(self, args):
        node = {}
        if args.p:
            node['cloud'] = args.p
        if args.s:
            node['subscriptionId'] = args.s
        if args.n:
            node['nextHop'] = args.n
        if args.g:
            node['resourceGroup'] = args.g
        if args.t:
            node['routeTableName'] = args.t
        if args.r:
            node['route'] = args.r
        if args.a:
            node['appId'] = args.a
        if args.d:
            node['tenantId'] = args.d
        if args.k:
            node['appKey'] = args.k

        return node


    def validate_set_param_inputs(self, node, new_params):
        response = {}
        resp_msg = '''Please make sure you have MSI (Managed service identity) feature available 
        in this region of Azure and it is configured to allow this CSR VM an contributer/network contributor 
        access to the route table to be able to change the routes. At last, please do 
        'node_event.py -i {} -e verify' to verify node is configured correctly.\n
                    '''.format(str(node['index']))
        response['code'] = 200
        response['msg'] = ""
        if not node.has_key("resourceGroup") or not node.has_key('subscriptionId'):
            response['code'] = 199
            response['msg'] = "Unable to validate nodes. Please verify node configuration"
            if not node.has_key("resourceGroup"):
                response['msg'] =  response['msg'] + "\n199: resourceGroup not found in input parameters"
            if not node.has_key("subscriptionId"):
                response['msg'] = response['msg'] + "\n199: subscriptionId not found in input parameters"
            return response

        if (not node.has_key('appId') or not node.has_key('subscriptionId') or not node.has_key('tenantId') or not node.has_key('appKey')) and node.has_key('cloud') != 'azure':
            log.warning(resp_msg)
            response['code'] = 199
            response['msg'] = resp_msg

        foundRoute = False
        routetable = self.get_route_table(node)
        if routetable is not None:
            # Walk through all the routes in the current route table
            if node.has_key("route"):
                for i, route in enumerate(routetable["properties"]["routes"]):
                    if route['properties']['nextHopType'] == 'VirtualAppliance':
                        # Updating a single route in the table.  Need to find the right one.
                        if node['route'] == route['properties']['addressPrefix']:
                            foundRoute = True
                if foundRoute:
                    response['msg'] += "Verified route {} is present in the routetable".format(node['route'])
                else:
                    response['code'] = 199
                    response['msg'] += "Route {} is not found in the routetable".format(node['route'])

            # checking if the node configured is for all routes
            else:
                response['code'] = 200
                response['msg'] += "Verified node configuration can fetch all routes in routetable"

        else:
            response['code'] = 199
            response['msg'] = "Unable to validate nodes, please verify the node configuration"
        return response

    # Taking cloud's input if a revert event is needed if none of nodes are configured as Primary
    def do_revert(self):
        return False
