# Sets default options for a host.
def defaultOptions():
    # These are the only guaranteed options for a host
    return {
        'port': 22,
        'username': 'root',
        # 'auth_method': 'PSK',
        # 'username': 'root',
        # 'auth_secret': '',
    }

# Valid YAML exerpt
# Hosts:
#   - ns1:
#       Auth_method: PSK
#       Auth_user: kindlehl
#       Auth_secret: my password
#     - ns2:

def createHostsFromYaml(yaml):
    hosts = []
    for host_dict in yaml['hosts']:
        hostname = list(host_dict.keys())[0]
        if host_dict[hostname] is None:
            hosts.append(Host(hostname, defaultOptions()))
        else:
            # Put all things like auth_method, auth_user in a variable called options on the host object
            options = defaultOptions().copy()
            options.update(host_dict[hostname])
            hosts.append(Host(hostname, options))
    return hosts

class Host:
    def __init__(self, hostname, yaml=defaultOptions()):
       self.hostname = hostname
       self.options = yaml

    def __str__(self):
        return "%s@%s" % (self.options['username'], self.hostname)

    def __repl__(self):
        return str(self)

    def __getitem__(self, index):
        return self.options[index]

    def __setitem__(self, index, val):
        self.options[index] = val
