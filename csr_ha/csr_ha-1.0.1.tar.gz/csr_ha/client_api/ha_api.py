#!/usr/bin/env python
import sys
import socket
from csr_ha.server import ha_server
from csr_cloud.csr_cloud import csr_cloud as cloud
import argparse
import time
import json
from os.path import expanduser

sock_file = expanduser("~") +"/cloud/HA/sock_file"

def send_command_to_server(c, command):
    global sock
    Max_Sock_Attempts = 4
    c.log.info("Sending %s" % command)

    # Create a UDS socket and connect the socket to the port where
    # the server is listening
    for attempt in range(Max_Sock_Attempts):
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(sock_file)
            sock.sendall(command)
            sock.shutdown(socket.SHUT_WR)
            return 'OK'
        except Exception as e:
            c.log.exception("API: Socket Exception %s " % e)
            pass
        c.log.error("API: attempt %d Failed.  Retrying" % (attempt+1))
        time.sleep(2)
    else:
        c.log.error("Unable to connect to server")
        return "%s failed" % command


def get_response_from_server(c):
    try:
        sock_buf_size = 255
        response = ""
        while True:
            rsp_msg = sock.recv(sock_buf_size)
            if len(rsp_msg) < sock_buf_size:
               response = response + rsp_msg
               sock.close()
               return response
            response = response + rsp_msg
    except Exception as err:
       c.log.exception("API: Socket Exception %s" % err)
       c.log.error("API: Unable to receive response from HA server")
       # returning the error as a dict (converted to string) to be consistent with response when there is no exception
       # it also makes retrieving the error response easier in create_node.py to display to customers
       error_response = {}
       error_response['code'] = 400
       error_response['msg'] = "API: Socket Exception %s" % err
       response = json.dumps(error_response)
       return response
    
    
def main(argv):
    c = cloud('HA')

    parser = argparse.ArgumentParser(description="CSR HA API Server")
    parser.add_argument('-c', nargs='?',help='{start | stop | ping}', default=None)
    args = parser.parse_args()

    action = args.c
    if action == 'start':
        ha_server.start_server(c)
        return 0
    elif action == 'stop':
        cmd_string = 'stop'
    elif action == 'ping':
        cmd_string = 'ping'

    req_msg = send_command_to_server(c, cmd_string)
    if req_msg == 'OK':
        rsp_msg = get_response_from_server(c)
        if 'OK' == rsp_msg:
            return 0
        else:
            c.log.error("Bad response: %s" % rsp_msg)
            return 4
    else:
        c.log.error("Req_msg: %s" % req_msg)
        print(req_msg)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
  


