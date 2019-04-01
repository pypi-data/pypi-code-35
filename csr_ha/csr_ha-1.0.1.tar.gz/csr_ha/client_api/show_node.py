#!/usr/bin/env python
import sys
import os
import ha_api
import argparse
from csr_cloud.csr_cloud import csr_cloud as cloud
import textwrap
import json


def validate_params(c, args):

    if args.i != "all":
        try:
            if int(args.i) < 1 or int(args.i) > 1023:
                print "400: Node_index -i expected to be in range <1-1023>/<all> show all nodes"
                sys.exit()
        except (TypeError, ValueError) as e:
            print "400: Node_index -i expected to be in range <1-1023>/<all> show all nodes"
            sys.exit()


def main(argv):
    c = cloud('HA')
    parser = argparse.ArgumentParser(description="CSR HA Show Node", formatter_class=argparse.RawTextHelpFormatter)
    parser._action_groups.pop()
    required = parser.add_argument_group('optional arguments')

    required.add_argument('-i', default="all",required = True, help=textwrap.dedent('''\
    <1..1023>      nodeIndex
    <all>         show all nodes
    '''))

    args = parser.parse_args()

    # Validate the cloud agnostic parameters
    validate_params(c, args)

    sys.argv[0] = os.path.basename(__file__)
    cmd_string = ' '.join(sys.argv)

    req_msg = ha_api.send_command_to_server(c, cmd_string)
    if req_msg == 'OK':
        rsp_msg = json.loads(ha_api.get_response_from_server(c))
        if rsp_msg['code'] == 200 or rsp_msg['code'] == 199:
            c.log.info("Client: show_node: received OK from server")
            print "{}: Retrieved the node successfully \n{}".format(rsp_msg['code'], rsp_msg['msg'])

        elif  rsp_msg['code'] == 400:
            c.log.info("Client: show_node: No redundancy nodes found")
            print "{}: {}".format(rsp_msg['code'], rsp_msg['msg'])
        else:
            c.log.info("Client: show_node: received ERR from server")
            print "400: Received ERR from server"
    else:
        c.log.error("Req_msg: %s" % req_msg)
        return 3

if __name__ == '__main__':
    sys.exit(main(sys.argv))
