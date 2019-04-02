from collections import OrderedDict
from .utils import Clr, Utils
from .config import Config

oly_banner = """
   ____  __
  / __ \/ /_  __
 / / / / / / / /
/ /_/ / / /_/ /
\____/_/\__, /
       /____/
"""


class Help:
    def __init__(self):
        pass

    HEADER = Clr.OK + oly_banner + Clr.RESET
    COPY = Clr.OK + 'Oly ' + Clr.RESET + 'version ' + Clr.WARNING + Utils.VERSION + Clr.RESET + ' by genzo'
    FOOTER = 'Run ' + Clr.OK + "'oly [COMMAND] --help'" + Clr.RESET + " for more information on a command.\n"
    OPTIONS = {
        '-h, --help': 'Display oly\'s help',
        '-v, --version': 'Display oly\'s version',
    }
    COMMANDS = OrderedDict([
        ('config', 'Client configuration'),
        ('tools', 'Run tools. Run \'oly tools --help\' for more information.'),
        ('service', 'Setup services. '),
        ('package', 'Setup package.'),
        ('console', 'Run a command on a container'),
        ('log', 'Fetch the logs of a container'),
        ('status', 'Tools and services statuses'),
        ('down', 'Bring everything down'),
        ('dump-config', 'Prints out the configuration'),
    ])
    SERVICES_ARGUMENTS = OrderedDict([
        ('add', {
            'args': [],
            'options': {},
            'desc': 'Add %s/s'
        }),
        ('run', {
            'args': [],
            'options': {
                '-a, --all': 'Run all %s/s'
            },
            'desc': 'Run %s'
        }),
        ('stop', {
            'args': [],
            'options': {
                '-a, --all': 'Stop all %s/s'
            },
            'desc': 'Stop %s/s'
        }),
        ('status', {
            'args': [],
            'options': {},
            'desc': '%s'.capitalize() + ' status'
        }),
        ('update', {
            'args': [],
            'options': {},
            'desc': 'Pulls %s last commit from Git'
        }),
        ('remove', {
            'args': [],
            'options': {},
            'desc': 'Remove %s/s'
        }),
        ('ls', {'desc': 'List all available %ss.'})
    ])
    ARGUMENTS = OrderedDict([
        ('run', {
            'args': [],
            'options': {
                '-h, --help': 'Display this help',
                '-a, --all': 'Enable all tools'
            },
            'desc': 'Run tools'
        }),
        ('stop', {
            'args': [],
            'options': {'-h, --help', '--all'},
            'desc': 'Stop tools'
        }),
        ('update', {
            'args': [],
            'options': {},
            'desc': 'Rebuild tools'
        }),
        ('status', {
            'args': [],
            'options': {},
            'desc': 'Tools status'
        }),
        ('ls', {'desc': 'List all available services.'})
    ])

    def get_help(self):
        print(self.HEADER + self.COPY)
        print('')
        Clr('Usage:').warn()
        print("  oly [OPTIONS] COMMAND [ARGUMENTS]")
        print('')
        Clr('Options:').warn()
        for opt, desc in self.OPTIONS.items():
            print(Clr.OK + "  %-25s %s" % (opt + Clr.RESET, desc))
        print('')
        Clr('Commands:').warn()
        for command, desc in self.COMMANDS.items():
            print(Clr.OK + "  %-20s %s" % (command + Clr.RESET, desc))
        print('')
        print(self.FOOTER)

        # config warn
        if not Config().read_config():
            Clr('Oly is not configured, run "oly config" to setup.').error_banner()
            print('')

    def get_args_help(self, arg):
        print('')
        Clr('Usage:').warn()
        print("  oly " + arg + " [ARGUMENTS...]")
        print('')
        Clr('Arguments:').warn()
        for command, desc in self.ARGUMENTS.items():
            if desc:
                print(Clr.OK + "  %-16s %s" % (command + Clr.RESET, desc['desc']))
        print('')

    @staticmethod
    def list_tools():
        data = Config().read_config()
        print('')
        Clr('Available tools:').warn()
        for tool in data['tools']:
            print(Clr.OK + "  %-16s" % (tool + Clr.RESET))
        print('')

    @staticmethod
    def tools_help(args):
        print('')
        Clr('Usage:').warn()
        print("  oly tools " + args[1] + " [OPTIONS]")
        print('')
        Clr('Options:').warn()
        print(Clr.OK + "  %-20s %s" % ('-a, --all' + Clr.RESET, 'Force to ' + str(args[1]) +
                                       ' all tools with no interaction.'))
        print(Clr.OK + "  %-20s %s" % ('--force-recreate' + Clr.RESET, 'Force recreate image'))
        print('')
        Clr('Arguments:').warn()
        for tool in Config().read_config()['tools']:
            print(Clr.OK + "  %-20s %s" % (tool + Clr.RESET, str(args[1]).capitalize() + ' ' + tool))
        print('')

    def services_help(self, mtype):
        print('')
        Clr('Usage:').warn()
        print("  oly %s [ARGUMENT]" % mtype)
        print('')
        Clr('Arguments:').warn()
        for command, desc in self.SERVICES_ARGUMENTS.items():
            print(Clr.OK + "  %-20s %s" % (command + Clr.RESET, desc['desc'] % mtype))
        print('')
