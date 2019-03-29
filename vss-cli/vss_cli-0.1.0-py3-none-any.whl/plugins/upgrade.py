"""Status plugin for VSS CLI (vss-cli)."""
import click
from subprocess import call
import logging

_LOGGING = logging.getLogger(__name__)


@click.group(
    'upgrade',
    invoke_without_command=True,
    short_help='Upgrade VSS CLI and dependencies.')
@click.argument(
    'upstream',
    type=click.Choice(
        ['stable', 'develop', 'branch']
    )
)
@click.option(
    '--git-branch', '-b',
    help='GitLab repository branch',
    required=False
)
def cli(upstream, git_branch):
    """Upgrade existing install of VSS CLI to the latest version
    (experimental). For example, to upgrade to the stable version:

    vss-cli upgrade stable

    To upgrade VSS CLI to the latest develop build:

    vss-cli upgrade develop

    To upgrade to a given official vss-cli GitLab repository:

    vss-cli upgrade --git-branch=issue-145 branch


    """
    lookup = {
        'stable': {
            'pkg': 'vss-cli',
            'args': []
        },
        'develop': {
            'pkg': 'vss-cli',
            'args': [
                '--upgrade',
                '--index-url',
                'https://test.pypi.org/legacy/'
            ]
        },
        'branch': {
            'pkg': f'git+https://gitlab-ee.eis.utoronto.ca'
            f'/vss/vss-cli.git@{git_branch}',
            'args': ['--upgrade']
        }
    }
    try:
        cmd_lookup = lookup[upstream]
        if upstream == 'branch':
            if not git_branch:
                raise click.BadOptionUsage(
                    'branch',
                    'Missing --branch/-b option. '
                    'Try master or develop.'
                )
    except ValueError as ex:
        _LOGGING.error(f'Invalid upstream {upstream}: {ex}')
        raise click.BadArgumentUsage(
            f'Invalid upstream {upstream}'
        )

    try:
        import pip
        cmd_args_str = ' '.join(cmd_lookup['args'])
        cmd_str = f"pip install {cmd_args_str} {cmd_lookup['pkg']}"
        _LOGGING.debug(f'Executing {cmd_str}')
        exit_code = call(
            cmd_str,
            shell=True)
        if exit_code > 0:
            raise click.ClickException(
                'Could not perform upgrade, please try: '
                '\n\tpip install --upgrade vss-cli')
    except ImportError as ex:
        _LOGGING.error(f'Error loading pip: {ex}')
        raise click.UsageError(
            'Pip is required to upgrade VSS CLI'
        )
