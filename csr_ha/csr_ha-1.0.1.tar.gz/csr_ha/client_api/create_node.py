#!/usr/bin/env python
import os
import sys
from csr_ha.client_api import ha_api
from csr_cloud.csr_cloud import csr_cloud as cloud
import argparse
import ipaddress
import json

def validate_params(c, args):

    if args.i == 0:
        c.log.error("client: create_node: route index of zero is reserved")
        return 2

    try:
        if int (args.i) < 1 or int(args.i) > 1023:
            print "400: Node_index -i expected to be in range <1-1023>"
            c.log.error("400: Node_index -i expected to be in range <1-1023>")
            sys.exit()
    except (ValueError, TypeError) as e:
        c.log.error("400: Node_index -i expected to be in range <1-1023>")
        print "400: Node_index -i expected to be in range <1-1023>"
        sys.exit()

    if args.r:
        try:
            ipaddress.ip_network(unicode(args.r))
            if "/" not in args.r:
                raise ValueError
        except ValueError as e:
            print ("400: Route(-r) {} is not in right IPv4/IPv6 CIDR format ".format(args.r))
            c.log.error(
                "Route (-r) {} is not in the right IPv4/IPv6 CIDR format while creating node: {}".format(args.r,
                                                                                                            args.i))
            sys.exit()

    nextHopValidation = c.ha.validate_nexthop(args.n)

    if nextHopValidation:
        print ("400: Nexthop(-n) {} is not in right IPv4/IPv6 address format ".format(args.n))
        c.log.error(
            "Nexthop(-n) {} is not in right IPv4/IPv6 address format while creating node: {}".format(args.n, args.i))
        sys.exit()

def main(argv):
    c = cloud('HA')

    parser = argparse.ArgumentParser(description="CSR HA Create Node")
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    required.add_argument('-i', nargs='?', help='<nodeIndex>       (1..1023)', required=True)
    optional.add_argument('-m', help='<mode>  {primary | secondary}', choices=['primary', 'secondary'],
                          default=None)

    c.ha.create_node_parser(optional, required)
    args = parser.parse_args()

    # Validate the cloud agnostic parameters
    validate_params(c, args)

    response = c.ha.validate_inputs(args)
    rsp_msg = json.loads(response)
    if rsp_msg['code'] == 200:
        c.log.info("Client: create_node : All node parameters are valid")
    elif rsp_msg['code'] == 199:
        c.log.info("Client: create_node : Node parameters validation completed with warnings")

    if 'msg' in rsp_msg:
        print ("{}: {}".format(rsp_msg['code'], rsp_msg['msg']))

    sys.argv[0] = os.path.basename(__file__)
    cmd_string = ' '.join(sys.argv)
    c.log.info("Cmd_string: %s" % cmd_string)
    req_msg = ha_api.send_command_to_server(c, cmd_string)
    if req_msg == 'OK':
        rsp_msg = json.loads(ha_api.get_response_from_server(c))
        if rsp_msg['code'] == 200 or rsp_msg['code'] == 199:
            c.log.info("Client: create_node : received OK from server")
            if 'msg' in rsp_msg:
                 print("{}: {}".format(rsp_msg['code'], rsp_msg['msg']))

            return 0
        else:
            c.log.error("Bad response: %s" % rsp_msg)
            print("400: Unable to create node: %s" %args.i)
            return 3
    else:
        c.log.error("Req_msg: %s" % req_msg)
        print(req_msg)
        return 3

if __name__ == '__main__':
    sys.exit(main(sys.argv))