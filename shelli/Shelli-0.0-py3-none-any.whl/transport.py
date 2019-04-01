"""
Implements a class and some exceptions for transferring files
"""

import os
import re

class TransporterError(Exception):
    """Base Exception class"""

class InvalidTransportFile(TransporterError):
    """No such file to transport error"""

class InvalidTransporter(TransporterError):
    """File is valid, but something else went wrong"""

class Transporter:
    """
    Class to facilitate the copying and deleting of temporary
    remote files such as scripts or configuration files
    """
    def __init__(self, transport_string):
        split = transport_string.split(':')
        self.local_file = split[0]
        self.remote_file = split[1]

        self.local_file = os.path.expanduser(self.local_file)

        if not os.path.exists(self.local_file):
            raise InvalidTransportFile

        if not re.match('^(.+)/([^/]+):(.+)/([^/]+)$', self.local_file + ':' + self.remote_file):
            raise InvalidTransporter

        if len(split) != 2:
            raise InvalidTransporter

    def send(self, connection):
        """Given a connection, send the local file over to the remote"""
        connection.put(self.local_file, remote=self.remote_file)

    def cleanup(self, connection):
        """Given a connection, remove the file that was transported to the remote"""
        connection.run('rm {remote_file}'.format(remote_file=self.remote_file))
