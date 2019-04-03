import os
import sys
import os.path
from datetime import datetime
import logging
import json
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from google.oauth2 import service_account
from logging.handlers import RotatingFileHandler
import ipaddress
import argparse
import re
import shutil

logger = logging.getLogger('HA')
logger.setLevel(logging.DEBUG)

EVENTS = 'events'
HA = 'HA'
HOME = os.path.expanduser("~")
EVENT_DIR = "%s/cloud/HA/events" % HOME

def validate_hop_priority_param(priority):
    try:
        if int(priority):
            if 0 < int(priority) < 65535:
                logger.info("Hop Priority value %s is valid" % priority)
                return priority
            else:
                logger.error("Hop Priority value %s is not in range 0-65535" % priority)
                raise argparse.ArgumentTypeError("Hop Priority should be between 0-65535")

    except ValueError:
        logger.exception("Hop Priority value %s is not valid integer. Please enter a value between 0-65535" % priority)
        raise argparse.ArgumentTypeError("Hop Priority should be between 0-65536")

def validate_string(s, pat=re.compile(r"[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?")):
    if not pat.match(s):
        raise argparse.ArgumentTypeError('input %s does not match the pattern "[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?"' % s)
    return s

class csr_ha():
    def __init__(self): # pragma: no cover
        if os.path.isfile('/home/guestshell/credentials.json'):
            SERVICE_ACCOUNT_FILE = '/home/guestshell/credentials.json'
            logger.info("Found local service account file")
            self.credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
        else:
            logger.info("Could not find local credentials file. Using ADC to get credentials")
            self.credentials = GoogleCredentials.get_application_default()
        self.service = discovery.build('compute', 'v1', credentials=self.credentials)
        # note: do we need these ?  will we install via --user ?
        sys.path.append(HOME + '/.local/lib/python2.7/site-packages/csr_ha/client_api')
        sys.path.append(HOME + '.local/lib/python2.7/site-packages/csr_ha/server')
        self.route_priority = 65535
        self.route_name = "csr-ha-verify-route"

        self.event_logger = logger
        self.event_log_file = ""

        try:
            if os.path.exists("/home/guestshell/cloud/HA/csr_ha.log"):
                if os.path.getsize("/home/guestshell/cloud/HA/csr_ha.log") > 15000000:
                    shutil.copy('/home/guestshell/cloud/HA/csr_ha.log', '/bootflash/csr_ha.log')
                    os.remove('/home/guestshell/cloud/HA/csr_ha.log')
        except Exception as e:
            logger.exception("Exception in init is {e}".format(e=e))
            pass

    def create_event_logger(self, node, event_type, directory_name):
        '''
            This function will create the event logger
        '''

        # Create the logger for events
        logger = logging.getLogger("HA.events")

        # Name the log file
        log_file = "node_" + str(node['index']) + "_" + str(
            datetime.now().strftime("%Y-%m-%d_%H:%M:%S")) + "_" + event_type

        # save the file path so that we can remove the file in-case of unnecessary reverts
        self.event_log_file = os.path.join(directory_name, log_file)

        # Roll over if the number of event files exceeds 513 count
        if len(os.listdir(directory_name)) > 512:
            filetoremove = os.popen("ls -t " + directory_name + "|  tail -1").read().strip()
            logger.info('Event files threshold exceeded. Removing event file: "{}"'.format(
                os.path.join(directory_name, filetoremove).strip()))
            command = "rm {}".format(os.path.join(directory_name, filetoremove))
            os.system(command)

        # Create the file handler
        handler = logging.FileHandler(filename=os.path.join(directory_name, log_file), mode='a')
        # Add Handler
        if not len(logger.handlers):
            logger.addHandler(handler)

        return logger

    def set_event_logger(self, node, event_type, directory_name=EVENT_DIR):
        '''
            This function will set the event_logger for ha
        '''
        logger.info("Setting event logger")
        self.event_logger = self.create_event_logger(node, event_type, directory_name)

    def create_node(self, params):
        '''
        Currently we are doing validation outside of create_node. So just return the parameters as is.
        '''
        node = params
        return node

    def validate_nexthop(self, nextHop):
        try:
            ipaddress.ip_address(unicode(nextHop))
            return 0
        except Exception as e:
            return 1

    def get_route_by_routename(self, node, route_name, event_type=None):

        try:
            request = self.service.routes().get(project=node['project'], route=route_name)
            response = request.execute()
            self.event_logger.info("Read route successfully")
            if event_type:
                self.event_logger.info("Event type: %s" % event_type)
        except Exception as e:
            self.event_logger.exception("Route GET request failed with error: %s" % e)
            response = str(e)
        self.event_logger.info("Returning response: %s" % response)
        return response

    def get_vpc(self, node):
        vpc = None
        route = self.get_route_by_routename(node, node['routeName'])
        if "HttpError" not in route:
            network = route['network']
            vpc = network.split('/')[-1]
            logger.info("The route %s is in VPC: %s" % (node['routeName'], vpc))
        else:
            logger.error("Received Error for Route. Returning vpc = None")

        return vpc

    def delete_route(self, node, route_name=None):
        if route_name:
            r_name = route_name
        else:
            r_name = node['routeName']

        route = self.get_route_by_routename(node, r_name)
        if "HttpError" in route:
            self.event_logger.error("Route not found. Returning")
            response = route
            return response

        try:
            self.event_logger.info("Deleting Route %s from project %s" % (r_name, node['project']))
            request = self.service.routes().delete(project=node['project'], route=r_name)
            response = request.execute()
            self.event_logger.info("Deleted route %s successfully" % r_name)
        except Exception as e:
            self.event_logger.exception("Error in deleting route is %s " % e)
            response = str(e)

        self.event_logger.info("Route delete completed at %s" % datetime.utcnow())
        return response

    def insert_route(self, node, newNextHop=None, route_priority=None, route_name = None):
        # Insert new route
        if not node['vpc']:
            self.event_logger.error("Node does not have a vpc network defined. Not inserting route and returning")
            return None

        if route_priority:
            prior = route_priority
        else:
            prior = node['hopPriority']

        if route_name:
            r_name = route_name
        else:
            r_name = node['routeName']

        if newNextHop:
            nextHop = newNextHop
        else:
            nextHop = node['nextHopIp']

        route_body = {
            "destRange": node['route'],
            "name": r_name,
            "network": "https://www.googleapis.com/compute/beta/projects/{}/global/networks/{}".format(
                node['project'], node['vpc']),
            "priority": prior,
            "nextHopIp": nextHop
        }
        self.event_logger.info("Inserting route: ")
        for key, value in route_body.items():
            self.event_logger.info("%s : %s" % (key, value))
        try:
            request = self.service.routes().insert(project=node['project'], body=route_body)
            response = request.execute()
        except Exception as e:
            self.event_logger.exception("Route Not inserted. Error is %s" % e)
            response = str(e)

        self.event_logger.info("Route insertion completed at %s" % datetime.utcnow())
        return response

    def set_route_table(self, node, event_type, route_table=None, event_file=None):
        self.event_logger.info("Event %s received from HA server at %s" % (event_type, datetime.utcnow()))

        if event_type.lower() == 'verify':
            self.event_logger.info("Evaluating single route for event type %s" % event_type)
            self.event_logger.info("Get route %s" % node['routeName'])
            # passing both node and node['routeName'] because I want to use the same method for getting my route or
            # peer route in delete
            route = self.get_route_by_routename(node, node['routeName'], event_type)
            self.event_logger.info("Received route %s" % route)

            if "HttpError" in route:
                self.event_logger.info("No route found with name %s. Returning!" % node['routeName'])
                self.event_logger.info("Event %s completed at %s" % (event_type, datetime.utcnow()))
                response = route
                # error responses are already str type. Don't have to type cast
                return response

            newNextHop = route['nextHopIp']
            self.event_logger.info("Next hop IP address is %s" % newNextHop)

            response = self.insert_route(node, newNextHop, self.route_priority, self.route_name)
            if response and "HttpError" not in response:
                self.event_logger.info("Inserted route %s to vpc %s" % (self.route_name, node['vpc']))
            else:
                self.event_logger.error("Something went wrong in inserting route! Returning error log to HA server")
                self.event_logger.info("Event %s completed at %s" % (event_type, datetime.utcnow()))
                # error responses are already str type. Don't have to type cast
                return response

            response = self.delete_route(node, self.route_name)
            if "HttpError" not in response:
                self.event_logger.info("Deleted route %s from vpc %s" % (self.route_name, node['vpc']))
            else:
                self.event_logger.error("Error in deleting route. Returning error log to HA server")
                self.event_logger.info("Event %s completed at %s" % (event_type, datetime.utcnow()))
                # error responses are already str type. Don't have to type cast
                return response

        elif event_type.lower() == 'revert':
            route = self.get_route_by_routename(node, node['routeName'], event_type)
            self.event_logger.info("Received route %s" % route)

            if "HttpError" not in route:
                # Validate that the route fetched matches with the node parameters
                self.event_logger.info("Validating if the route in VPC matches with node configuration")
                validate_response = self.validate_revert_params(node)

                if validate_response['code'] == 200:
                    # The route fetched matches with the route params in node. The route already exists in the VPC so delete the event file
                    if os.path.isfile(self.event_log_file):
                        os_command = "rm \"%s\"" % self.event_log_file
                        os.system(os_command)
                    self.event_logger.info("Route already exists. Nothing to do.")
                    response = route
                else:
                    self.event_logger.info(validate_response['msg'])
                    self.event_logger.info("The route entry in the VPC %s does not match with the node configuration. Please delete the route so that we can insert the route in VPC as defined in node configuration" % node['vpc'])
                    return validate_response['msg']

            else:
                self.event_logger.info("Route not found in vpc %s. Inserting Route" % node['vpc'])
                response = self.insert_route(node)
                if response and "HttpError" not in response:
                    self.event_logger.info("Inserted route %s to vpc %s" % (self.route_name, node['vpc']))
                else:
                    self.event_logger.error("Something went wrong in inserting route! Returning error log to HA server")
                    self.event_logger.info("Event %s completed at %s" % (event_type, datetime.utcnow()))
                    # error responses are already str type. Don't have to type cast
                    return response

        elif event_type.lower() == "peerfail":
            peer_route_name = node['peerRouteName']

            if 'mode' in node and node['mode'] == 'primary':
                # this indicates the peer route is secondary route and we don't have to delete it.
                self.event_logger.info("Peer route %s is not the primary route for destination %s. Nothing to do. Returning." % (node['peerRouteName'], node['route']))
                response = "Peer route %s is not the primary route for destination %s. Nothing to do. Returning." % (node['peerRouteName'], node['route'])
                self.event_logger.info("Event %s completed at %s" % (event_type, datetime.utcnow()))
                # Returning a str, no need to type cast
                return response


            response = self.delete_route(node, peer_route_name)

            if "HttpError" in response:
                self.event_logger.info("No peer route found. Nothing to do.")
                self.event_logger.info("Event %s completed at %s" % (event_type, datetime.utcnow()))
                # error responses are already str type. Don't have to type cast
                return response
            else:
                self.event_logger.info("Deleted peer route. Route %s is now active route for destination %s" % (
                node['routeName'], node['nextHopIp']))

        else:
            self.event_logger.error("Invalid event type %s in set_route_table" % event_type)
            response = "Invalid event type %s in set_route_table" % event_type

        self.event_logger.info("Event %s completed at %s" % (event_type, datetime.utcnow()))
        #converting dict to str before sending back response
        return json.dumps(response)

    def get_route_table(self, node, event_type): # pragma: no cover
        return None

    def verify_node(self, node, event_type):
        required_keys = ['cloud', 'project', 'vpc', 'routeName', 'peerRouteName', 'nextHopIp', 'hopPriority']
        node_verified = True
        for key in required_keys:
            if key in node:
                continue
            else:
                logger.error("Missing required parameter %s" % key)
                node_verified = False

        if node_verified:
            logger.info("All required parameters have been provided")
            return 'OK'
        else:
            return 'ERR1'

    def check_cloud_command(self, cmd):
        keyword = ""
        if cmd == '-g':
            keyword = "project"
        elif cmd == '-v':
            keyword = "vpc"
        elif cmd == '-a':
            keyword = "routeName"
        elif cmd == '-b':
            keyword = "peerRouteName"
        elif cmd == '-o':
            keyword = "hopPriority"
        elif cmd == '-p':
            keyword = "cloud"
        elif cmd == '-n':
            keyword = "nextHopIp"
        elif cmd == '-r':
            keyword = "route"
        else:
            logger.error("Invalid command format %s" % cmd)

        return keyword

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

    def validate_peer_route(self, node):
        # validate the peer route exists in the route table for create_node validation
        peerRoute = self.get_route_by_routename(node, node['peerRouteName'])
        if "HttpError" not in peerRoute:
            # The peer route exists
            logger.info("Peer route %s found in Project %s" % (node['peerRouteName'], node['project']))
            response = True
        else:
            logger.error(
                "The peer route %s does not exist in Project %s" % (node['peerRouteName'], node['project']))
            response = False

        return response

    def validate_vpc(self, node, vpc):
        # Validate VPC
        if 'vpc' in node:
            if node['vpc'] == vpc:
                logger.info("Valid VPC set in HA redundancy node")
                response = True
            else:
                logger.error(
                    "Route %s does not belong to VPC %s" % (
                        node['routeName'], node['vpc']))
                response = False

        else:
            node['vpc'] = vpc
            logger.info("VPC set to %s in HA redundancy node" % vpc)
            response = True

        return response

    def validate_project(self, node, project_id):
        # Validate Project ID
        if node['project'] == project_id:
            logger.info("Valid Project ID set in HA redundancy node")
            response = True
        else:
            logger.error(
                "Route %s does not belong to Project %s" % (
                    node['routeName'], node['project']))
            response = False

        return response

    def validate_nextHopIp(self, node, nexthop):
        # Validate next Hop IP
        if 'nextHopIp' in node:
            if node['nextHopIp'] == nexthop:
                logger.info("Valid next hop ip set in HA redundancy node")
                response = True
            else:
                logger.error(
                    "Next hop IP %s does not match with route %s" % (
                        node['nextHopIp'], node['routeName']))
                response = False

        else:
            node['nextHopIp'] = nexthop
            logger.info("Next Hop IP set to %s in HA redundancy node" % node['nextHopIp'])
            response = True

        return response

    def validate_dest_route(self, node, dest_range):
        # Validate destination route
        if 'route' in node:
            if node['route'] == dest_range:
                logger.info("Valid route set in HA redundancy node")
                response = True
            else:
                logger.error(
                    "Destination Range %s does not match with route %s" % (
                        node['route'], node['routeName']))
                response = False

        else:
            node['route'] = dest_range
            logger.info("Route set to %s in HA redundancy node" % node['route'])
            response = True

        return response

    def validate_route_priority(self, node, priority):
        # Validate Route Priority
        if 'hopPriority' in node:
            logger.info("Route priority is %s" % priority)
            if int(node['hopPriority']) == priority:
                logger.info("Valid Hop Priority set in HA redundancy node")
                response = True
            else:
                logger.error("Hop priority %s does not match with priority for route %s" % (
                    node['hopPriority'], node['routeName']))
                response = False
        else:
            node['hopPriority'] = priority
            logger.info("Hop priority set to %s in HA redundancy node" % node['priority'])
            response = True
        return response

    def check_clear_param(self, index, old_params):

        keyword = " "
        if old_params[index] == '-g':
            keyword = "project"
        if old_params[index] == '-v':
            keyword = "vpc"
        elif old_params[index] == '-a':
            keyword = "routeName"
        elif old_params[index] == '-b':
            keyword = "peerRouteName"
        elif old_params[index] == '-n':
            keyword = "nextHopIp"
        elif old_params[index] == '-o':
            keyword = "hopPriority"
        elif old_params[index] == '-r':
            keyword = "route"
        else:
            logger.error("Invalid parameter format %s" % old_params[index])

        return keyword

    def clear_param_parser(self, optional, required):

        optional.add_argument('-n', help='to clear the nextHopIp', default=None, action="store_true")
        optional.add_argument('-g', help='to clear the project id', default=None, action="store_true")
        optional.add_argument('-v', help='to clear the vpc', default=None, action="store_true")
        optional.add_argument('-a', help='to clear the routeName', default=None, action="store_true")
        optional.add_argument('-b', help='to clear the peerRouteName', default=None, action="store_true")
        optional.add_argument('-o', help='to clear the hopPriority', default=None, action="store_true")
        optional.add_argument('-r', help='to clear the route', default=None, action="store_true")

        return optional, required

    def create_node_parser(self, optional, required):

        required.add_argument('-g', help='Google Cloud Project ID which contains the CSRs', default=None, required=True, type=validate_string)
        required.add_argument('-p', help='Cloud Provider   {gcp}', choices=['gcp'],
                              default=None, required=True)
        required.add_argument('-a', help='The route name for which the current CSR is the next hop', default=None, required=True, type=validate_string)
        required.add_argument('-b', help='The route name for which the BFD peer CSR is the next hop', default=None, required=True, type=validate_string)
        required.add_argument('-n', help='Next Hop IP address for the node. This should be the IP address of the current CSR', default=None, required=True)
        required.add_argument('-o', help='The route priority for the route for which the current CSR is the next hop', default=None, required=True, type=validate_hop_priority_param)
        required.add_argument('-r', help='The destination route CIDR for the route for which the current CSR is the next hop e.g. 15.0.0.0/8', default=None, required=True)
        required.add_argument('-v', help='The VPC network name where the route with the current CSR as the next hop exists', default=None, required=True, type=validate_string)

        return optional, required

    def create_node_from_args(self, args):
        node = {}
        if args.v:
            node['vpc'] = args.v
        if args.a:
            node['routeName'] = args.a
        if args.b:
            node['peerRouteName'] = args.b
        if args.g:
            node['project'] = args.g
        if args.o:
            node['hopPriority'] = args.o
        if args.n:
            node['nextHopIp'] = args.n
        if args.r:
            node['route'] = args.r
        return node

    def validate_revert_params(self, node):
        resp_msg = ""
        response, fail_return_code = self.get_response_dict(event='revert')
        # Check if the route exists
        route = self.get_route_by_routename(node, node['routeName'])
        if "HttpError" in route:
            # route was not found, no other values need validation.
            logger.error("Route %s not found in VPC" % node['routeName'])
            response['code'] = fail_return_code
            resp_msg = resp_msg + "Warning: Route %s not found in this account" % node['routeName']
        else:
            # Validate vpc
            network = route['network']
            vpc = network.split('/')[-1]
            vpc_response = self.validate_vpc(node, vpc)
            if not vpc_response:
                resp_msg = resp_msg + "Warning: Route %s does not belong to VPC %s " \
                                      "operation.\n" % (node['routeName'], node['vpc'])
            # validate project id
            project = route['selfLink']
            project_id = project.split('/')[-4]
            project_response = self.validate_project(node, project_id)
            if not project_response:
                resp_msg = resp_msg + "Warning: Route %s does not belong to Project %s" \
                                      "operation.\n" % (node['routeName'], node['project'])

            # validate nextHopIp
            nextHop = route['nextHopIp']
            nextHopIp_response = self.validate_nextHopIp(node, nextHop)
            if not nextHopIp_response:
                resp_msg = resp_msg + "Warning: Next hop IP %s does not match with route %s" \
                                      "node operation.\n" % (node['nextHopIp'], node['routeName'])
            # validate destRange
            dest_range = route['destRange']
            dest_range_response = self.validate_dest_route(node, dest_range)
            if not dest_range_response:
                resp_msg = resp_msg + "Warning: Destination Range %s does not match with route %s\n" % (node['route'], node['routeName'])

            # validate priority
            priority = route['priority']
            priority_response = self.validate_route_priority(node, priority)
            if not priority_response:
                resp_msg = resp_msg + "Warning: Hop priority %s does not match with priority for route %s in vpc " \
                                      "%s \n" % (node['hopPriority'], node['routeName'], vpc)

            if not vpc_response or not project_response or not nextHopIp_response or not dest_range_response or not priority_response:
                response['code'] = fail_return_code

        response['msg'] = resp_msg
        return response


    def validate_inputs(self, args):
        resp_msg = ""
        logger.info("Validating if node parameters are valid")
        node = self.create_node_from_args(args)
        logger.info("Node:")
        for key,val in node.items():
            logger.info("%s : %s" % (key,val))
        response, fail_return_code = self.get_response_dict()

        #Check if peer route is valid
        peerRoute_response = self.validate_peer_route(node)
        if not peerRoute_response:
            resp_msg = resp_msg + "Warning: Peer route %s not found in Project %s\n" % (node['peerRouteName'], node['project'])
            response['code'] = fail_return_code

        # Check if the route exists
        route = self.get_route_by_routename(node, node['routeName'])
        if "HttpError" in route:
            # route was not found, no other values need validation.
            logger.error("Route %s not found in VPC" % node['routeName'])
            response['code'] = fail_return_code
            resp_msg = resp_msg + "Warning: Route %s not found in this account" % node['routeName']
        else:
            #Validate vpc
            network = route['network']
            vpc = network.split('/')[-1]
            vpc_response = self.validate_vpc(node, vpc)
            if not vpc_response:
                resp_msg = resp_msg + "Warning: Route %s does not belong to VPC %s as provided in create node " \
                                      "operation.\n" % (node['routeName'], node['vpc'])
            #validate project id
            project = route['selfLink']
            project_id = project.split('/')[-4]
            project_response = self.validate_project(node, project_id)
            if not project_response:
                resp_msg = resp_msg + "Warning: Route %s does not belong to Project %s as provided in create node " \
                                  "operation.\n" % (node['routeName'], node['project'])

            #validate nextHopIp
            nextHop = route['nextHopIp']
            nextHopIp_response = self.validate_nextHopIp(node, nextHop)
            if not nextHopIp_response:
                resp_msg = resp_msg + "Warning: Next hop IP %s does not match with route %s as provided in create " \
                                      "node operation.\n" % (node['nextHopIp'], node['routeName'])
            #validate destRange
            dest_range = route['destRange']
            dest_range_response = self.validate_dest_route(node, dest_range)
            if not dest_range_response:
                resp_msg = resp_msg + "Warning: Destination Range %s does not match with route %s as provided in " \
                                      "create node operation.\n" % (node['route'], node['routeName'])

            #validate priority
            priority = route['priority']
            priority_response = self.validate_route_priority(node,priority)
            if not priority_response:
                resp_msg = resp_msg + "Warning: Hop priority %s does not match with priority for route %s in vpc " \
                                      "%s \n" % (node['hopPriority'], node['routeName'], vpc)

            if not vpc_response or not project_response or not nextHopIp_response or not dest_range_response or not priority_response:
                response['code'] = fail_return_code

        if response['code'] == 200:
            resp_msg = resp_msg + "All node inputs are valid"
        else:
            resp_msg = resp_msg + "\nPlease verify the node configuration"

        response['msg'] = resp_msg
        return json.dumps(response)

    def validate_set_param_inputs(self, node, new_params):
        logger.info("Validating if set node parameters are valid")
        resp_msg = ""
        response, fail_return_code = self.get_response_dict()

        if 'peerRouteName' in new_params:
            # Check if peer route is valid
            peerRoute_response = self.validate_peer_route(node)
            if not peerRoute_response:
                resp_msg = resp_msg + "Warning: Peer route %s not found in Project %s\n" % (
                node['peerRouteName'], node['project'])
                response['code'] = fail_return_code

        # Check if the route exists
        route = self.get_route_by_routename(node, node['routeName'])
        if "HttpError" in route:
            # route was not found, no other values need validation.
            logger.error("Route %s not found in VPC" % node['routeName'])
            response['code'] = fail_return_code
            resp_msg = resp_msg + "Warning: Route %s not found in this account." % node['routeName']
        else:

            if 'vpc' in new_params:
                # Validate vpc
                network = route['network']
                vpc = network.split('/')[-1]
                vpc_response = self.validate_vpc(node, vpc)
                if not vpc_response:
                    resp_msg = resp_msg + "Warning: Route %s does not belong to VPC %s" \
                                          "operation.\n" % (node['routeName'], node['vpc'])
                    response['code'] = fail_return_code

            if 'project' in new_params:
                # validate project id
                project = route['selfLink']
                project_id = project.split('/')[-4]
                project_response = self.validate_project(node, project_id)
                if not project_response:
                    resp_msg = resp_msg + "Warning: Route %s does not belong to Project %s" \
                                          "operation.\n" % (node['routeName'], node['project'])
                    response['code'] = fail_return_code

            if 'nextHopIp' in new_params:
                # validate nextHopIp
                nextHop = route['nextHopIp']
                nextHopIp_response = self.validate_nextHopIp(node, nextHop)
                if not nextHopIp_response:
                    resp_msg = resp_msg + "Warning: Next hop IP %s does not match with route %s" \
                                          "node operation.\n" % (node['nextHopIp'], node['routeName'])
                    response['code'] = fail_return_code

            if 'route' in new_params:
                # validate destRange
                dest_range = route['destRange']
                dest_range_response = self.validate_dest_route(node, dest_range)
                if not dest_range_response:
                    resp_msg = resp_msg + "Warning: Destination Range %s does not match with route %s\n" % (node['route'], node['routeName'])
                    response['code'] = fail_return_code

            if 'priority' in new_params:
                # validate priority
                priority = route['priority']
                priority_response = self.validate_route_priority(node, priority)
                if not priority_response:
                    resp_msg = resp_msg + "Warning: Hop priority %s does not match with priority for route %s in vpc " \
                                          "%s \n" % (node['hopPriority'], node['routeName'], vpc)
                    response['code'] = fail_return_code

        if response['code'] == 200:
            resp_msg = resp_msg + "All node inputs are valid"
        else:
            resp_msg = resp_msg + "\nPlease verify the node configuration"

        response['msg'] = resp_msg
        return response

    def set_node_parser(self, optional, required):

        optional.add_argument('-g', help='to set the project id', default=None)
        optional.add_argument('-a', help='to set the routeName', default=None)
        optional.add_argument('-b', help='to set the peerRouteName', default=None)
        optional.add_argument('-o', help='to set the hopPriority', default=None, type=validate_hop_priority_param)
        optional.add_argument('-v', help='to set the vpc', default=None)
        optional.add_argument('-n', help='to set the nextHopIp', default=None)
        optional.add_argument('-r', help='to set the route', default=None)

        return optional, required

    # Taking cloud's input if a revert event is needed if none of nodes are configured as Primary
    def do_revert(self):
        return True