#!/usr/bin/env python
"""Provides the RDSManager class to connect to the existing AWS RDS in use by CFL"""
from time import sleep

from pymysql import connect
from sshtunnel import SSHTunnelForwarder

from ._database import Database

__author__ = 'Will Garside'
__email__ = 'worgarside@gmail.com'
__status__ = 'Production'


class RDSManager(Database):
    """Extension of the Database class specifically for connecting to a MySQL AWS RDS"""

    def setup(self):
        """Setup the SSH Tunnel and Database connection"""

        self.dialect = 'mysql'
        self.driver = 'pymysql'
        self.required_creds = {'db_user', 'db_password'}
        self.db_port = 3306 if not self.db_port else self.db_port

    def _open_ssh_tunnel(self):
        """The RDS requires SSH tunnelling in, so this does that"""

        tunnel_success = False

        while not tunnel_success:
            try:
                self.server = SSHTunnelForwarder(
                    (self.ssh_host, self.ssh_port),
                    ssh_username=self.ssh_username,
                    ssh_pkey=self.pkey_path,
                    remote_bind_address=(self.db_bind_address, self.db_port)
                )
                tunnel_success = True
            except KeyboardInterrupt:
                self.disconnect()
            sleep(5)

        self.server.start()

    def connect_to_db(self):
        """Open the connection to the database"""

        self._open_ssh_tunnel()
        connection_success = False

        while not connection_success:
            try:
                self.conn = connect(
                    user=self.db_user,
                    passwd=self.db_password,
                    host=self.db_host,
                    database=self.db_name,
                    port=self.server.local_bind_port
                )
                connection_success = True
                self.cur = self.conn.cursor()
            except KeyboardInterrupt:
                self.disconnect()
            sleep(5)
