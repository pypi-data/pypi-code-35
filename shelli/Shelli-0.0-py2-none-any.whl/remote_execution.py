from fabric import Connection
from getpass import getpass

# Executor takes a target. The target contains all the information it needs to execute code
class Executor:
    def __init__(self, target):
        self.hosts = target.getAllHosts()
        print(target.commands)
        self.commands = target.commands

    def transport():
        pass

    def execute(self):
        for host in self.hosts:
            password = getpass("Enter password for %s:" % host)
            conn = Connection(
                host.hostname,
                user=host.options['username'],
                port=host.options['port'],
                connect_kwargs={
                    'password': password
                }
            )
            for command in self.commands:
                print(command)
                conn.run(command)

    def cleanup():
        pass

