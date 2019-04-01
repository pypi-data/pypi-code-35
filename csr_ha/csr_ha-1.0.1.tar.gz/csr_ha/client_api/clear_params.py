#!/usr/bin/env python
import sys
import os
from csr_ha.client_api import ha_api
from csr_cloud.csr_cloud import csr_cloud as cloud
import argparse
import json

def validate_params(c, args):
    if args.i == 0:
        c.log.error("Client: clear_node: route index of zero is reserved")
        return 2

    try:
        if int (args.i) < 1 or int(args.i) > 1023:
            print "400: Node_index -i expected to be in range <1-1023>"
            sys.exit()
    except (ValueError, TypeError) as e:
        print "400: Node_index -i expected to be in range <1-1023>"
        sys.exit()

def main(argv):
    c = cloud('HA')
    parser = argparse.ArgumentParser(description="CSR HA Clear Node")
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    required.add_argument('-i', nargs='?', help='nodeIndex', required=True)
    optional.add_argument('-m', help='to clear the mode', default=None, action="store_true")

    c.ha.clear_param_parser(optional, required)
    args = parser.parse_args()
    argc = len(argv)

    if (argc != 2) and (argc < 4):
        c.log.error("Client: clear_params: invalid number of arguments %d" % argc)
        print "400: Invalid number of arguments %d" % argc
        parser.print_help()
        parser.exit()

    # Validate the cloud agnostic parameters
    validate_params(c, args)


    sys.argv[0] = os.path.basename(__file__)
    cmd_string = ' '.join(sys.argv)

    req_msg = ha_api.send_command_to_server(c, cmd_string)

    if req_msg == 'OK':
        rsp_msg = json.loads(ha_api.get_response_from_server(c))
        if rsp_msg['code'] == 200 or rsp_msg['code'] == 199:
            c.log.info("Client: clear_params: received OK from server")
            if "msg" in rsp_msg:
                print "{}: {}".format(rsp_msg['code'], rsp_msg['msg'])
            return 0
        else:
            c.log.error("Bad response: %s" % rsp_msg)
            if "msg" in rsp_msg:
                print "{}: {}".format(rsp_msg['code'], rsp_msg['msg'])
            return 3
    else:
        c.log.error("Req_msg: %s" % req_msg)
        print(req_msg)
        return 3

if __name__ == '__main__':
    sys.exit(main(sys.argv))
