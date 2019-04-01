"""
Defines a class and methods for authenticating with a host
"""

import sys
from getpass import getpass

from fabric import Connection
import paramiko

# This is a hash of id(options): connection_object. The options
# between hosts in a given hostgroup are the exact same object
# unless the host defines custom options. So the number of options
# in this list will always be less than or equal to the number of hosts
# that request authentication information.
CONNECTION_DICT = {}

def authenticate(hostname, options):
    """
    Authenticate to the server. Will retry logins three times if password needs to be entered
    """
    kwargs = {
        'key_filename': None
    }

    if options['auth_method'] == 'key':
        kwargs['key_filename'] = options['key']
        if options['password'] is not None:
            kwargs['passphrase'] = options['password']
        else:
            kwargs['passphrase'] = get_password(
                hostname=options['key'],
                prompt='Enter password for keyfile {hostname}: '
            )
    else:
        if options['password'] is not None:
            kwargs['password'] = options['password']
        else:
            options['password'] = get_password(
                hostname="{u}@{h}".format(
                    u=options['username'],
                    h=hostname
                )
            )
            kwargs['password'] = options['password']

    conn = Connection(
        hostname,
        user=options['username'],
        port=options['port'],
        connect_kwargs=kwargs
    )
    handle_connection_errors(conn, options)

    return conn

def get_connection(host):
    """
    Searches existing connection pool for a connection that matches
    the id of the options passed in. If found, it returns a connection
    object to run on, otherwise, creates a new connection, saves it, and
    returns it.
    """
    for options in CONNECTION_DICT:
        if options is id(host.options):
            return CONNECTION_DICT[id(host.options)]

    # Established connection not found, create one
    CONNECTION_DICT[id(host.options)] = authenticate(host.hostname, host.options)
    return CONNECTION_DICT[id(host.options)]

def get_password(hostname='localhost', prompt='Enter password for {hostname}: '):
    """
    Get a password
    """
    return getpass(prompt.format(hostname=hostname))


def handle_connection_errors(connection, options):
    """
    Tries to open the connection, exits cleaner than a traceback if shit hits the fan.
    """
    try:
        connection.open()
        connection.close()
    except paramiko.ssh_exception.SSHException:
        if options['key'] is not None:
            sys.stderr.write("Could not handle {key}. Does it exist? New"\
                    " key formats might also not be supported.".format(key=options['key']))
            exit(1)
