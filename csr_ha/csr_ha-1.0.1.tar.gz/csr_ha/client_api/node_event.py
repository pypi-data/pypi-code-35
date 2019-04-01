#!/usr/bin/env python
import sys
import os
from csr_ha.client_api import ha_api
from csr_cloud.csr_cloud import csr_cloud as cloud
import argparse
import json

def validate_params(c, args):

    if args.i != "all":
        try:
            if int(args.i) < 1 or int(args.i) > 1023:
                print "400: Node_index -i expected to be in range <1-1023>/<all> node"
                c.log.error("400: Node_index -i expected to be in range <1-1023>/<all> node")
                sys.exit()
        except (ValueError, TypeError) as e:
            print "400: Node_index -i expected to be in range <1-1023>/<all> node"
            c.log.error("400: Node_index -i expected to be in range <1-1023>/<all> node")
            sys.exit()
    else:
        if args.e == "peerFail":
            print "400: Cannot perform peerFail node_event for all nodes"
            sys.exit()
        #Internally processing all as Nodeindex 0
        args.i = 0
        if args.mi:
            print "400: Unnecessary -mi parameter when using <all> as node_index"


def main(argv):
    c = cloud('HA')

    parser = argparse.ArgumentParser(description="CSR HA Create Node")
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    
    required.add_argument('-i', nargs='?',help='<nodeIndex>', required=True)
    optional.add_argument('-mi', nargs='?',help='<maxIndex>', type=int, default=None, required=False)
    required.add_argument('-e', help='<eventType>  {peerFail | revert | verify}', choices=['peerFail', 'revert', 'verify'], default=None, required=True)

    args = parser.parse_args()

    # Validate the cloud agnostic parameters
    validate_params(c, args)
    sys.argv[0] = os.path.basename(__file__)
    cmd_string = ' '.join(sys.argv)

    req_msg = ha_api.send_command_to_server(c, cmd_string)
    if req_msg == 'OK':
        rsp_msg = json.loads(ha_api.get_response_from_server(c))
        if rsp_msg['code'] == 200 or rsp_msg['code'] == 199:
            c.log.info("Client: node_event: received OK from server")
            if 'msg' in rsp_msg:
                print("{}: {}".format(rsp_msg['code'], rsp_msg['msg']))
            return 0
        else:
            c.log.error("Bad response: %s" % rsp_msg)
            print "400: Unable to process node_event"
            return 7
    else:
        print req_msg

if __name__ == '__main__':
    sys.exit(main(sys.argv))

  


