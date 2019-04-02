#!/usr/bin/env python

import os
import sys
from os.path import expanduser
import socket
#import urllib3.contrib.pyopenssl
import urllib3
import traceback
import logging
from logging.handlers import RotatingFileHandler
import auth_mgr

# Specify files accessed by this script in guestshell
base_dir = expanduser('~') + '/cloud/authMgr/'
debug_file = base_dir + "token_svr.log"
sock_file = base_dir + "sock_file"

if not os.path.exists(base_dir):
    os.makedirs(base_dir)

# Create and configure a logger for the token server
logger = logging.getLogger("Token_svr")
handler = RotatingFileHandler(debug_file, maxBytes=1000000, backupCount=2)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def start_token_svr(): #pragma: no cover
    # Find out the process ID
    pid = os.getpid()

    # Open the debug log file
    logger.info("Token server started, pid=%d", pid)
    # Make sure the socket does not already exist
    try:
        os.unlink(sock_file)
    except OSError:
        if os.path.exists(sock_file):
            raise

    # Create a UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Bind the socket to the port
    sock.bind(sock_file)

    # Use OpenSSL to check certificates for https
    urllib3.contrib.pyopenssl.inject_into_urllib3()

    # Create the MSI based authentication application
    try: 
        auth_mgr.set_default_msi_app(logger)
    except Exception as e:
        logger.error("Server: failed to enable authentication using MSI: %s" % str(e))

    # Get default AAD application if it exists in the app_file
    auth_mgr.read_table_from_file(logger)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        connection, client_address = sock.accept()
        try:
            while True:
                # Read a command from the client
                line = connection.recv(255)
                if line == '':
                    break

                command = line.rsplit(' ')
                if command[0] == "MSI_req":
                    # Ask the authentication manager for a token
                    token = auth_mgr.get_token(logger)

                    # Send the number of bytes in the token
                    token_len = len(token)
                    token_len_as_str = str(token_len) + ' '
                    connection.sendall(token_len_as_str)

                    # Send the token
                    if token != '':
                        connection.sendall(token)
                    else:
                        logger.error("Server: no token returned")

                elif command[0] == "AAD_req":
                    token = ''
                    # Validate the AAD app parameters and get the app
                    aad_app = auth_mgr.verify_aad_app(logger, command[1], command[2], command[3], command[4])
                    if aad_app is not None:
                        # Ask the authentication manager for a token
                        token = auth_mgr.get_token(logger, aad_app)

                    # Send the number of bytes in the token
                    token_len = len(token)
                    token_len_as_str = str(token_len) + ' '
                    connection.sendall(token_len_as_str)

                    # Send the token
                    if token != '':
                        connection.sendall(token)
                    else:
                        logger.error("Server: no token returned by AAD")

                elif command[0] == "Ping":
                    connection.sendall("Ack")
                elif command[0] == 'MSI_app':
                    rc = auth_mgr.set_default_msi_app(logger)
                    connection.sendall(rc)
                elif command[0] == 'Set_app':
                    rc = auth_mgr.set_default_aad_app(logger, command[1], command[2], command[3], command[4])
                    connection.sendall(rc)
                elif command[0] == 'Clear_app':
                    rc = auth_mgr.clear_default_aad_app()
                    connection.sendall(rc)
                elif command[0] == 'Clear_list':
                    rc = auth_mgr.clear_aad_app_list()
                    connection.sendall(rc)
                elif command[0] == 'Show':
                    buf = auth_mgr.show()
                    buf_len_as_str = str(len(buf) - 1) + '#'
                    connection.sendall(buf_len_as_str)
                    connection.sendall(buf)
                elif command[0] == 'Clear_token':
                    rc = auth_mgr.clear_token(logger)
                    connection.sendall(rc)
                elif command[0] == 'Refresh':
                    token = auth_mgr.refresh_token(logger)
                    if token == '':
                        rc = 'ERR: Token not refreshed'
                    else:
                        rc = 'OK'
                    connection.sendall(rc)
                else:
                    logger.error("Token server unrecognized command %s", command)
                    err_msg = "Error: invalid command %s" % command
                    connection.sendall(err_msg)

            # Clean up the connection
            connection.close()

        except Exception as e:
            logger.error("Token server caught exception %s", str(e))
            tb = traceback.format_exc()
            logger.error("%s", tb)
            #connection.sendall(e.message)
            connection.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Incorrect usage of token server script")
        logger.info("Usage: {} start".format(__file__))
        sys.exit(1)
    if sys.argv[1] == 'start':
        start_token_svr()
