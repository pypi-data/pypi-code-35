"""
Module for working with targets. Provides a class that
initializes a target from yaml, and offers helper methods
for dealing with targets.
"""

from shelli import hostgroup

# Valid yml exerpt
# targets:
#   touch:      <------------- You get this
#     commands:
#       - touch /home/kindlehl/testingcommander
#     groups:
#       - DNS

# Targets are READ ONLY
# Do NOT modify anything in them. This way, you won't need to make copies of everything!!!
class Target:
    """Class to represent a target. Created with a yaml object and a list of hostgroups"""

    def __init__(self, name, all_hostgroups, target_yaml):
        self.name = name
        self.commands = target_yaml['commands']
        self.hostgroup_names = target_yaml['hostgroups']

        if 'transport' in list(target_yaml.keys()):
            self.transports = target_yaml['transport']
        else:
            self.transports = []

        self.hostgroups = {}
        for group in all_hostgroups.values():
            if group.name in self.hostgroup_names:
                self.hostgroups[group.name] = group

    def __str__(self):
        return self.name

    def __repl__(self):
        return str(self)

    def get_all_hosts(self):
        """Returns list of all hosts on target."""

        all_hosts = {}
        for group in self.hostgroups.values():
            for host_key in group.hosts:
                all_hosts[host_key] = group.hosts[host_key]

        return all_hosts

def create_targets_from_yaml(yaml):
    """Creates a list of all targets, given a yaml object"""

    all_hostgroups = hostgroup.create_host_groups_from_yaml(yaml)
    targets = {}

    for target in yaml['targets']:
        target_name = list(target.keys())[0]
        new_target = Target(target_name, all_hostgroups, target[target_name])
        targets[target_name] = new_target

    return targets
