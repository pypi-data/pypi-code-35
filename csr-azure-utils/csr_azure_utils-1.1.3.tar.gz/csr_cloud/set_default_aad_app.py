#!/usr/bin/env python

import sys
from csr_cloud.token_api import Token_api as token_api
import argparse


def main(argv):

    parser = argparse.ArgumentParser(description="AAD Application")
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-p', help='<cloud_provider>   {azure | azusgov | azchina}',
                          choices=['azure', 'azusgov', 'azchina'], default=None, required=True)
    required.add_argument('-a', help='to add the applicationId', default=None, required=True)
    required.add_argument('-d', help='to add the tenantId', default=None, required=True)
    required.add_argument('-k', help='to add the applicationKey', default=None, required=True)

    args = parser.parse_args()

    # Establish a connection to the token server
    conn = token_api()

    # Verify server is up
    rc = conn.is_server_up()
    if rc != 0:
        print "failed connection to token manager rc=%d" % rc
        sys.exit()

    # Request server to clear the default AAD application
    result = conn.set_default_aad_app(args.p, args.d, args.a, args.k)
    if result != 'OK':
        print "Failed to set default AAD application: %s" % result
        sys.exit()

    conn.disconnect()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
