"""This is the main entry to beat's cmdlines scripts.
"""

import logging
import pkg_resources
import click
from click_plugins import with_plugins
from ..click_helper import AliasedGroup
from ..decorators import verbosity_option
from ..config import Configuration

# defines our own logging level for extra information to be printed
logging.EXTRA = 15
logging.addLevelName(logging.EXTRA, "EXTRA")

def _extra(self, message, *args, **kws):
    if self.isEnabledFor(logging.EXTRA):
        self._log(logging.EXTRA, message, args, **kws)

logging.Logger.extra = _extra

@with_plugins(pkg_resources.iter_entry_points('beat.cli'))
@click.group(cls=AliasedGroup)
@click.option('-T', '--test-mode', help='Assume test mode and doesn\'t setup '
              'the logging module', default=False, is_flag=True)
@click.option('-p', '--prefix',
              help='Overrides the prefix of your local data. '
              'If not set use the value from your RC file',
              type=click.STRING)
@click.option('-c', '--cache',
              help='Overrides the cache prefix. If not set, use the value '
              'from your RC file', type=click.STRING)
@click.option('-t', '--token', help='Overrides the user token for server '
              'operations. If not set, use the value from your RC file.',
              type=click.STRING)
@click.option('-u', '--user', help='Overrides the user name on the remote '
              'platform. If not set, use the value from your RC file.',
              type=click.STRING)
@click.option('-m', '--platform', help='The URL of the BEAT platform to '
              'access.', type=click.STRING)
@click.option('-e', '--editor',
              help='Overrides the user editor to edit local files. If not '
              'set, use the value from your environment. There are no '
              'defaults for this option.', type=click.STRING)
@click.version_option()
@verbosity_option()
@click.pass_context
def main(ctx, test_mode, prefix, cache, user, token, platform, editor):
    """The main command line interface for beat cmdline. Look below for available
    commands."""

    ctx.meta['--prefix'] = prefix
    ctx.meta['--cache'] = cache
    ctx.meta['--user'] = user
    ctx.meta['--token'] = token
    ctx.meta['--platform'] = platform
    ctx.meta['--editor'] = editor

    # Check that we are in a BEAT working folder
    config = Configuration(ctx.meta)

    # Sets up the central logger
    if not test_mode:
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG) #lets everything pass by default

        # Console logging
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO) # default level

        format_str = "%(message)s"
        if 'verbosity' in ctx.meta and ctx.meta['verbosity'] > 2:
            format_str = "[%(asctime)s - %(name)s] %(levelname)s: %(message)s"

        formatter = logging.Formatter(format_str, datefmt="%d/%b/%Y %H:%M:%S")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Execute the command
    ctx.meta['config'] = config
