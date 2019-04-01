#!/usr/bin/env python
import os
import sys
import socket
from multiprocessing import Process
from node_mgr import NodeTable
from csr_ha.server import event_mgr
from csr_cloud.csr_cloud import csr_cloud as cloud
import argparse
from os.path import expanduser
import json

server_running = False
home = expanduser("~")
sock_file = home + "/cloud/HA/sock_file"
node_file = home + "/cloud/HA/node_file"


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def create_node(c, table, params):
    c.log.info("Processing a create_node command")
    c.log.info("Dict of parameters is %s" % params)
    return table.create_node(params)


def set_params(c, table, params):
    c.log.info("Processing a set_param command")
    c.log.info("Dict of parameters is %s" % params)
    return table.set_params(params)


def clear_params(c, table, params):
    c.log.info("Processing a clear_param command")
    c.log.info("Dict of parameters is %s" % params)
    return table.clear_params(params)


def show_node(c, table, params):
    if params['index'] == 'all':
        total_str = table.show_table()
        c.log.info("See output on server")
        return total_str
    else:
        node_desc = table.show_node(params)
        return node_desc


def delete_node(c, table, params):
    c.log.info("Processing a delete_node command")
    c.log.info("Dict of parameters is %s" % params)
    return table.delete_node(params)


def event_on_one_node(c, event_type, node, params):
    event_mgr.handle_event(node, event_type)


def node_event(c, table, params):
    response = {}
    response['msg'] = ""
    response['code'] = 200
    if params['index'] == 'all':
        index = 0
    else:
        index = int(params['index'])

    # Return if none of the nodes are configured to be primary
    process_event = False
    if params['event'] == "revert":
        for node in table.nodes:
            if node.has_key('mode') :
                if node['mode'] == 'primary':
                    process_event = True

        if not process_event and not c.ha.do_revert():
            c.log.info("No primary nodes configured, revert event aborted")
            response['msg'] = "No primary nodes configured, revert event aborted"
            return json.dumps(response)

    max_node = 0
    if 'range' in params:
        max_node = int(params['range'])
    event_type = params['event']

    for node in table.nodes:
        process_node = False
        node_index = int(node['index'])
        if (((index > 0) and (max_node == 0)) or (index == max_node)):
            # Looking to match a single node
            if node_index == index or index == 0:
                process_node = True
            # Do not process node
            if node.has_key('mode'):
                 if node['mode'] != 'primary' and params['event'] == 'revert' and not c.ha.do_revert():
                    process_node = False

        elif index < max_node:
            # Looking for a range of nodes
            if (index <= node_index) and (node_index <= max_node):
                process_node = True
        else:
            c.log.error("Invalid node range of %d to %d" % (index, max_node))

        if process_node:
            c.log.info("Node event on: {}".format(index))
            event_on_one_node(c, event_type, node, params)
    response['msg'] = "Node_event processed successfully"
    return json.dumps(response)


def server(c):
    # Find out the process ID
    pid = os.getpid()

    # Open up a file to write error and debug messages
    c.log.info("High availability server started with pid=%d" % pid)

    # Create an instance of the node manager
    nodeTable = NodeTable()

    # Create a UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Bind the socket to the port
    sock.bind(sock_file)

    # Listen for incoming connections
    sock.listen(1)

    while server_running:
        try:
            # Wait for a connection
            connection, client_address = sock.accept()

            # Read a command from the client
            line = connection.recv(300)
            c.log.debug("Server got command %s" % line)
            cmd_list = line.rsplit(' ')
            cmd_name = cmd_list[0].rsplit('.', 1)[0]
            ret_msg = ''

            # Call the function that handles this command
            if cmd_name != 'clear_params':
                cmd_dict = {}
                i = 1
                while i < len(cmd_list):
                    if cmd_list[i] == '-i':
                        keyword = "index"
                    elif cmd_list[i] == '-mi':
                        keyword = "range"
                    elif cmd_list[i] == '-m':
                        keyword = "mode"
                    elif cmd_list[i] == '-c':
                        keyword = "command"
                    elif cmd_list[i] == '-e':
                        keyword = "event"
                    elif cmd_list[i] == '':
                        break
                    else:
                        keyword = c.ha.check_cloud_command(cmd_list[i])
                    value = cmd_list[i + 1]
                    i = i + 2
                    if keyword != 'Error':
                        cmd_dict[keyword] = value
                        c.log.info("Added keyword %s with value %s" % (keyword, value))

            if cmd_name == 'create_node':
                ret_msg = create_node(c, nodeTable, cmd_dict)
            elif cmd_name == 'set_params':
                ret_msg = set_params(c, nodeTable, cmd_dict)
            elif cmd_name == 'clear_params':
                ret_msg = clear_params(c, nodeTable, cmd_list)
            elif cmd_name == 'show_node':
                ret_msg = show_node(c, nodeTable, cmd_dict)
            elif cmd_name == 'delete_node':
                ret_msg = delete_node(c, nodeTable, cmd_dict)
            elif cmd_name == 'node_event':
                ret_msg = node_event(c, nodeTable, cmd_dict)
            elif cmd_name == 'stop':
                ret_msg = stop_server()
            elif cmd_name == 'ping':
                ret_msg = 'OK'
            else:
                ret_msg = "Unknown server command %s" % cmd_name
                c.log.error("Unknown server command %s" % cmd_name)

            connection.sendall(ret_msg)
        except socket.error as err:
            c.log.error("Server socket error %d" % err.errno)

        except Exception as e:
            c.log.exception("Server Exception: %s" % e)
            connection.sendall(e.message)

    # Clean up the connection
    c.log.info("Server exiting")
    connection.close()
    return 0


def start_server(c):
    global server_running

    print "Starting the high availability server"
    c.log.info("Starting the high availability server")
    server_running = True

    # Make sure the socket does not already exist
    try:
        os.unlink(sock_file)
    except OSError:
        if os.path.exists(sock_file):
            os_command = "rm %s" % sock_file
            os.system(os_command)

    p = Process(target=server, args=(c,))
    p.start()
    p.join()


def stop_server(c):
    global server_running

    print "Processing a stop_server command"
    c.log.info("Processing a stop_server command")
    server_running = False

    # Make sure the socket does not already exist
    try:
        os.unlink(sock_file)
    except OSError:
        if os.path.exists(sock_file):
            os_command = "rm %s" % sock_file
            os.system(os_command)
    return 'OK'


def main(argv):
    c = cloud('HA')

    parser = argparse.ArgumentParser(description="CSR HA API Server")
    parser.add_argument('start', nargs='?', const=True, help='start server', default=None)
    # parser.add_argument('stop', help='stop server', default=None)
    args = parser.parse_args()

    if args.start is not None:
        start_server(c)

    elif args.stop is not None:
        stop_server(c)
        return 0
    else:
        return 'ERR1'


if __name__ == '__main__':
    sys.exit(main(sys.argv))