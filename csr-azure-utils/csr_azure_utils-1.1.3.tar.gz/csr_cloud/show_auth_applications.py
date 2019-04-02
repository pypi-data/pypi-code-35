#!/usr/bin/env python

import sys
from csr_cloud.token_api import Token_api as token_api


def main(argv):

    # Establish a connection to the token server
    conn = token_api()

    # Verify server is up
    rc = conn.is_server_up()
    if rc != 0:
        print "failed connection to token manager rc=%d" % rc
        sys.exit()

    # Request server to clear the default AAD application
    result = conn.show_auth_apps()
    if result != 'OK':
        print "Failed to show authentication applications: %s" % result
        sys.exit()

    conn.disconnect()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
