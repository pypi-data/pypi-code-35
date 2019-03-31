import sys


class CLI:
    commands = {}

    def add_command(self, command, *routes):
        for route in routes:
            self.commands[route] = command

    def command(self, *routes):
        def decorator(func):
            self.add_command(func, *routes)
        return decorator

    def __call__(self):
        argv = sys.argv[1:]
        if len(argv)>0:
            command_name = argv.pop(0)
            Command = self.commands.get(command_name)
            if Command:
                command = Command()
                args = command.parser.parse_args(argv)
                kwargs = dict((arg, getattr(args, arg)) for arg in vars(args))
                command.run(**kwargs)
            else:
                print('[kriek] Command "%s" does not exists.'%command_name)
        else:
            print('doc')
        
