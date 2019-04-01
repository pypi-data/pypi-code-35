"""
Class for hosts and their authentication paramters.  Also provides
helper functions for loading host objects from yaml.
"""

import copy

# Sets default options for a host.
def default_options():
    """Returns default authentication settings."""

    options = {
        'auth_method': 'password',
        'username': 'root',
        'port': 22,
        'key': None,
        'password': None
    }

    return copy.deepcopy(options)

# Valid YAML exerpt
# hosts:
#   - ns1:
#       auth_method: PSK
#       username: kindlehl
#       auth_secret: my password
#   - ns2:

def create_hosts_from_yaml(yaml):
    """Creates a list of host objects from yaml config."""

    hosts = {}
    for host_object in yaml['hosts']:
        if isinstance(host_object, str):
            hostname = host_object
            host_object = {hostname: None}
        else:
            hostname = list(host_object.keys())[0]

        if host_object[hostname] is None:
            hosts[hostname] = Host(hostname, default_options())
        else:
            # Put all things like auth_method, auth_user in
            # a variable called options on the host object
            options = default_options()
            options.update(host_object[hostname])
            hosts[hostname] = Host(hostname, options)
    return hosts

class Host:
    """
    Class to describe a hostname and the authentication options
    used to login to the machine. It has sane default authentication
    options such as root user and password auth.
    """

    def __init__(self, hostname, yaml=default_options()):
        self.hostname = hostname
        self.options = yaml

    def __str__(self):
        return "%s@%s" % (self.options['username'], self.hostname)

    def __hash__(self):
        return str(self)

    def __cmp__(self, rhs):
        return str(self) == str(rhs)

    def __repl__(self):
        return str(self)

    def __getitem__(self, index):
        return self.options[index]

    def __setitem__(self, index, val):
        self.options[index] = val
