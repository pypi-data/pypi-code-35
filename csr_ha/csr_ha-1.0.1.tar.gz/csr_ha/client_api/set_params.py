#!/usr/bin/env python
import sys
import os
from csr_ha.client_api import ha_api
from csr_cloud.csr_cloud import csr_cloud as cloud
import argparse
import ipaddress
import json

def validate_params(c, args):

    try:
        if int(args.i) < 1 or int(args.i) > 1023:
            print "400: Node_index -i expected to be in range <1-1023>"
            sys.exit()
    except ValueError as e:
        print "400: Node_index -i expected to be in range <1-1023>"
        sys.exit()

    if args.r:
        try:
            ipaddress.ip_network(unicode(args.r))
            if "/" not in args.r:
                raise ValueError
        except (TypeError, ValueError) as e:
            print ("400: Route(-r) %s is not in correct IPv4/IPv6 network format " % args.r)
            c.log.error(
                "Route (-r) {} is not in the right IPv4/IPv6 network format while setting node: {}".format(args.r,
                                                                                                           args.i))
            sys.exit()

    if args.n:
        nextHopValidation = c.ha.validate_nexthop(args.n)
        if nextHopValidation:
            print ("400: Nexthop(-n) %s is not in right IPv4/IPv6 address format " % args.n)
            c.log.error(
                "Nexthop(-n) {} is not in right IPv4/IPv6 address format while setting node: {}".format(args.n, args.i))
            sys.exit()

def main(argv):
    c = cloud('HA')

    parser = argparse.ArgumentParser(description="CSR HA Set Node")
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-i', nargs='?', help='<nodeIndex>', required=True)
    optional.add_argument('-m', help='<mode> {primary | secondary}', default=None, choices=['primary', 'secondary'])

    c.ha.set_node_parser(optional, required)
    args = parser.parse_args()

    # Validate the cloud agnostic parameters
    validate_params(c, args)

    sys.argv[0] = os.path.basename(__file__)
    cmd_string = ' '.join(sys.argv)

    req_msg = ha_api.send_command_to_server(c, cmd_string)
    if req_msg == 'OK':
        rsp_msg = json.loads(ha_api.get_response_from_server(c))
        if rsp_msg['code'] == 200 or rsp_msg['code'] == 199:
            c.log.info("Client: set_params: received OK from server")
            if 'msg' in rsp_msg:
                print("{}: {}".format(rsp_msg['code'], rsp_msg['msg']))
                print "200: Set_params processed successfully"
            return 0
        else:
            c.log.error("Bad response: %s" % rsp_msg)
            print("400: Unable to set parameters for node: %s" % args.i)
            if 'msg' in rsp_msg:
                print("{}: {}".format(rsp_msg['code'], rsp_msg['msg']))
                print "400: Unable to process set_params"
            return 3
    else:
        print req_msg

if __name__ == '__main__':
    sys.exit(main(sys.argv))
