"""Configuration plugin for VSS CLI (vss-cli)."""
import click
import logging
import os
from vss_cli import const
from vss_cli.cli import pass_context
from vss_cli.config import Configuration
from vss_cli.helper import format_output


_LOGGING = logging.getLogger(__name__)


@click.group('config')
@pass_context
def cli(ctx: Configuration):
    """Configure VSS CLI options. If this command is run with no arguments,
    you will be prompted for configuration values such as your VSS username
    and password.  If your config file does not  exist (the default location
    is ~/.vss-cli/config.json, the VSS CLI will create it for you."""
    ctx.auto_output('table')


@cli.command()
@click.option('-r', '--replace', is_flag=True, default=False,
              help='Replace existing configuration')
@pass_context
def mk(ctx: Configuration, replace):
    """Create new configuration or add profile to config file"""
    endpoint = ctx.server or click.prompt(
        'Endpoint',
        default=ctx.server,
        type=click.STRING
    )
    username = ctx.username or click.prompt(
        'Username',
        default=ctx.username,
        type=click.STRING
    )
    password = ctx.password or click.prompt(
        'Password',
        default=ctx.password,
        show_default=False,
        hide_input=True,
        type=click.STRING,
        confirmation_prompt=True
    )
    ctx.configure(
        username=username,
        password=password,
        endpoint=endpoint,
        replace=replace
    )


COLUMNS_DETAILS = [
    ("ENDPOINT", "endpoint"),
    ("USER", "user"),
    ("PASS", "pass"),
    ("TOKEN", "token"),
    ("SOURCE", "source"),
]


@cli.command()
@pass_context
def ls(ctx: Configuration):
    """List existing configuration"""
    from base64 import b64decode
    _profiles = list()
    try:
        profiles = ctx.load_raw_config_file()

        # checking profiles
        for key, profile in profiles.items():
            auth = profile['auth']
            auth_enc = auth.encode()
            user, pwd = b64decode(auth_enc).split(b':')
            masked_pwd = ''.join(['*' for i in range(len(pwd))])
            _profiles.append(
                {'endpoint': key,
                 'user': user.decode(), 'pass': masked_pwd[:8],
                 'token': '{}...{}'.format(profile['token'][:10],
                                           profile['token'][-10:]),
                 'source': 'config file'}
            )
    except FileNotFoundError as ex:
        _LOGGING.warning(f'{str(ex)}. Have you run vss-cli configure mk?')

    # checking env vars
    envs = [e for e in os.environ if 'VSS_' in e]
    if envs:
        user = os.environ.get('VSS_USER', '')
        pwd = os.environ.get('VSS_USER_PASS', '')
        masked_pwd = ''.join(['*' for i in range(len(pwd))])
        tk = os.environ.get('VSS_TOKEN', '')
        endpoint = os.environ.get('VSS_ENDPOINT', const.DEFAULT_SERVER)
        source = 'env'
        _profiles.append({'endpoint': endpoint,
                          'user': user, 'pass': masked_pwd,
                          'token': '{}...{}'.format(tk[:10], tk[-10:]),
                          'source': source})
    click.echo(
        format_output(
            ctx,
            _profiles,
            columns=COLUMNS_DETAILS,
        )
    )
