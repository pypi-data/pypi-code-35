"""
Implements a class to represent a group of hosts
and default authentication for all hosts within
the group. Individual host configuration will
overwrite the group settings. Also provides helper
methods such as loading groups from yaml.
"""

import copy
from shelli import host

def create_host_groups_from_yaml(yaml):
    """Loads groups into list from yaml passed in"""

    groups = {}
    hosts = host.create_hosts_from_yaml(yaml)
    for groupyml in yaml['hostgroups']:
        groupname = list(groupyml.keys())[0]
        groups[groupname] = HostGroup(groupname, groupyml[groupname], hosts)
    return groups

# Valid YAML exerpt
#
# Hostgroups:
#   - DNS:        <------- You are passed this part
#       Hosts:
#         - ns1
#         - ns2
#       Options:
#         auth_method: PSK
#         auth_secret: 'Insecure as fuck'
#
#
# python representation -> [{'DNS': {'Hosts': ['ns1','ns2']}}]

class HostGroup:
    """Class for creating a hostgroup from yaml."""

    def __init__(self, groupname, yaml, all_host_objects):
        self.name = groupname
        # names of all hosts in the group (might not be needed) IMMUTABLE
        self.hostnames = yaml['hosts']
        self.options = host.default_options()

        if 'options' in list(yaml.keys()):
            self.options.update(yaml['options'])

        self.hosts = {}
        for host_object in all_host_objects.values():
            if host_object.hostname in self.hostnames:
                new_host = copy.deepcopy(host_object)

                if new_host.options == host.default_options():
                    new_host.options = self.options
                else:
                    original_options = copy.deepcopy(new_host.options)
                    new_host.options = copy.deepcopy(self.options)
                    new_host.options.update(original_options)

                self.hosts[new_host.hostname] = new_host

    def __str__(self):
        return self.name

    def __repl__(self):
        return str(self)
