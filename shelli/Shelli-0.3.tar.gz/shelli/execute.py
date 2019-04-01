"""
Class for executing commands. Uses dependency injection
to run commands from a target.
"""

import sys

from shelli import authenticate
from shelli import transport

# Executor takes a target. The target contains all the information it needs to execute code
class Executor:
    """Class to manage executing commands on a host"""

    def __init__(self, target):
        """Nothing."""
        self.hosts = target.get_all_hosts()

        self.longest_host_string = 0
        for host in self.hosts:
            if len(str(self.hosts[host])) > self.longest_host_string:
                self.longest_host_string = len(str(self.hosts[host]))

        self.commands = target.commands
        self.transporters = []
        for transport_string in target.transports:
            self.transporters.append(transport.Transporter(transport_string))

    def execute(self):
        """Actually execute commands from a target onto its hosts"""
  
        # Get all connections. Will probably require authentication.
        # This way makes sure all hosts get authentication information up-front
        # Instead of 5 minutes later, after running a long command
        conns = {}
        for cur_host in self.hosts.values():
            print("Creating connection {name}".format(name=cur_host))
            conns[str(cur_host)] = authenticate.get_connection(cur_host)

        for conn in conns:
            # Transport any necessary files
            self.do_transport(conns[conn])

            # Run commands
            self.run(conn, self.commands, conns[conn])

            # Clean up, ya filthy animal
            self.cleanup(conns[conn])

    def run(self, message, commands, connection):
        """Runs a command on a given connection"""
        for command in commands:
            prompt_header = "[{}]".format(message)
            format_string = "{: <" + str(self.longest_host_string + 2) + "}"
            prompt_header = format_string.format(prompt_header)
            prompt_body = "\tRunning '{}'\n".format(command)
            sys.stderr.write(prompt_header + prompt_body)
            sys.stderr.flush()
            connection.run(command)

    def do_transport(self, connection):
        """Move files to remote"""
        for tranny in self.transporters:
            tranny.send(connection)

    def cleanup(self, connection):
        """Finish up stuff after remote execution"""
        for tranny in self.transporters:
            tranny.cleanup(connection)
