#!/usr/bin/env python

import os
import sys
from csr_ha.client_api import ha_api
from csr_cloud.csr_cloud import csr_cloud as cloud
import argparse
import json

def validate_params(c, args):
    try:
        if int (args.i) < 1 or int(args.i) > 1023:
            print "400: Node_index -i expected to be in range <1-1023>"
            sys.exit()
    except (ValueError, TypeError) as e:
        print "400: Node_index -i expected to be in range <1-1023>"
        sys.exit()


def main(argv):
    c = cloud('HA')

    parser = argparse.ArgumentParser(description="CSR HA Delete Node")
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-i', nargs='?',help='<nodeIndex>', required=True)

    args = parser.parse_args()

    # Validate the cloud agnostic parameters
    validate_params(c, args)

    sys.argv[0] = os.path.basename(__file__)
    cmd_string = ' '.join(sys.argv)

    req_msg = ha_api.send_command_to_server(c, cmd_string)
    if req_msg == 'OK':

        rsp_msg = json.loads(ha_api.get_response_from_server(c))
        if rsp_msg['code'] == 200 or rsp_msg['code'] == 199:
            c.log.info("Client: delete_node: received OK from server")
            print "{}: {}".format(rsp_msg['code'], rsp_msg['msg'])
            return 0
        else:
            c.log.error("Bad response: %s" % rsp_msg)
            print "{}: {}".format(rsp_msg['code'], rsp_msg['msg'])
            return 4

    else:
        c.log.error("Req_msg: %s" % req_msg)
        print(req_msg)
        return 4

if __name__ == '__main__':
    sys.exit(main(sys.argv))

  


