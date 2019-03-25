import sys

from cliff.app import App
from cliff.commandmanager import CommandManager

from .. import __version__


class PescatoreCliApp(App):
    def __init__(self):
        super().__init__(
            description='Pescatore CLI',
            version=__version__,
            command_manager=CommandManager('pescatore_cli.cli'),
            deferred_help=True
        )
    def initialize_app(self, argv):
        self.LOG.debug('initialize_app %s', argv)

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    pescatore_cli_app = PescatoreCliApp()
    return pescatore_cli_app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
