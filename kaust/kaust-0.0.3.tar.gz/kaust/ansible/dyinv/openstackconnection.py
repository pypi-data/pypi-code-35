"""This class connects to an OpenStack cluster to find hosts that have to be patched
and which services on those hosts should be tested after reboot"""

import json
import os
from openstack import connection

class OpenStackConnection:
    """This class is used to access backend OpenStack cluster. It exports a
    to_json method that will use query passed during constructing this
    class to find hosts on which Ansible should apply patching."""

    def __init__(self):
        """Create an OpenStack connection."""
        auth_url = os.getenv('OPENSSTACK_AUTH_URL', 'https://horizon.kaust.edu.sa:15000/v3/')
        self.connection = connection.Connection(auth_url=auth_url,
                                                project_name=os.getenv('OPENSSTACK_PROJECT_NAME', 'admin'),
                                                username=os.getenv('OPENSTACK_USERNAME'),
                                                password=os.getenv('OPENSTACK_PASSWORD'),
                                                user_domain_id=os.getenv('OPENSTACK_USER_DOMAIN_ID', 'default'),
                                                project_domain_id=os.getenv('OPENSTACK_PROJECT_DOMAIN_ID', 'default'))

    def to_json(self):
        """Return this class in its JSON representation."""
        host_names = {
            "_meta": {
                # pylint: disable=no-member
                "hostvars": OpenStackConnection.host_vars(self.connection.compute.servers(all_tenants=True))
            },
            "all": {
                # pylint: disable=no-member
                "hosts": OpenStackConnection.host_list(self.connection.compute.servers(all_tenants=True)),
                "vars": {}
            }
        }
        print(json.dumps(host_names, indent=4, sort_keys=False))

    @staticmethod
    def host_list(servers):
        """Return list of patchable hosts."""
        return [s.name for s in servers if OpenStackConnection.server_is_patchable(s)]

    @staticmethod
    def server_is_patchable(server):
        """Return True if server is patchable."""
        return OpenStackConnection.patching_is_enabled(server.metadata) and \
               'ACTIVE' in server.status and \
               OpenStackConnection.has_public_ip(server.addresses)

    @staticmethod
    def patching_is_enabled(metadata):
        """Return True if PATCHING is YES."""
        return 'PATCHING' not in metadata or metadata['PATCHING'].lower() == 'yes'

    @staticmethod
    def has_public_ip(addresses):
        """Return True is addresses contains an IP starting iwth 10.x."""
        return 'provider1' in addresses and addresses['provider1'][0]['addr'].startswith('10.')

    @staticmethod
    def host_vars(servers):
        """Return vars associated to servers used by Ansible."""
        host_vars = {}
        for srv in servers:
            if OpenStackConnection.server_is_patchable(srv):
                host_vars[srv.name] = {}
                host_vars[srv.name]["ansible_host"] = srv.addresses['provider1'][0]['addr']
                host_vars[srv.name]["service_tag"] = OpenStackConnection.get_service_tag(srv)
        return host_vars

    @staticmethod
    def get_service_tag(server):
        """Return all SERVICETAG associated to server."""
        tags = [""]
        if "SERVICETAG" in server.metadata:
            tags = server.metadata["SERVICETAG"].split(",")
        return tags
