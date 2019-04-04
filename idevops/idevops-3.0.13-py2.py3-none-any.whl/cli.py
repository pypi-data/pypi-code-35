from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError
from idevops import VERSION
from idevops import aws as iaws
from idevops.aliased_group import AliasedGroup
from idevops.iserver import gen_iserver_config
from idevops.shell_wrapper import play_wrap
from idevops.utils import *
from subprocess import call
from yaml.constructor import ConstructorError
from yaml.parser import ParserError
import six

if six.PY2:
    import __builtin__ as builtins
else:
    import builtins


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(VERSION)
    ctx.exit()


CONTEXT_SETTINGS_SHORT_H = dict(help_option_names=['-h', '--help'])
CONTEXT_SETTINGS_WRAPPER = dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
)


# main cmd
@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS_SHORT_H)
@click.option('--name', '-n', envvar='INET', help='Set network name, read `INET` from environment if not specified',
              default='example', prompt=False, show_default='example')
@click.option('--version', '-v', is_flag=True, callback=print_version, expose_value=False,
              is_eager=True, help='Show version')
@click.option('--fast', '-f', is_flag=True, help='Only deal with regions in config')
@click.pass_context
def cli(ctx, name, fast):
    ctx.obj['name'] = name
    ctx.obj['fast'] = fast

#
# static
#

# configure
# @cli.command(short_help="A wrapper around `ansible`", context_settings=CONTEXT_SETTINGS_WRAPPER)
# @click.pass_context
# def configure(ctx):
#    """Configure aws options
#
#    See `aws configure help`
#    """
#    call(['aws', 'configure'] + ctx.args)


# configtest
@cli.command()
@click.option('--list', '-l', is_flag=True, help='List valid node(s).')
@click.pass_context
def configtest(ctx, list):
    """Parse config and test syntax"""
    config_all = get_config_by_name(ctx.obj['name'], check_valid=False, allow_none=True)
    config_valid = get_config_by_name(ctx.obj['name'], allow_none=True)
    config_missing_key = [e for e in config_all if e not in config_valid]
    names = [item['name'] for item in config_valid]
    repeat = builtins.list(set([item for item in names if names.count(item) > 1]))
    config_aws_config_err, config_valid = check_config_aws_valid(config_valid)

    if config_missing_key or repeat:
        if repeat:
            click.secho('Multiple ' + ','.join(repeat) + ' found', fg='red')
        for e in config_missing_key:
            click.secho(show_missing_key_in_config(e), fg='red')
    elif config_aws_config_err:
        for e in config_aws_config_err:
            click.secho(e['msg'], fg='red')
    else:
        click.secho('OK !', fg='green')

    if list and config_valid:
        print_table(config_valid)


#
# aws
#

# create
@cli.command()
@click.option('--overwrite', is_flag=True, help='Overwrite local key pair if exists.')
# @click.argument('branch', default='master')
@click.pass_context
def create(ctx, overwrite):
    """Create network"""
    click.echo('Creating network: {0} ...'.format(ctx.obj['name'], ), err=True)
    iaws.create(ctx.obj['name'], is_overwrite=overwrite, fast=ctx.obj['fast'])
    click.echo(click.style('Done', fg='green') + ' ... Cheers.', err=True)


# delete
@cli.command()
@click.confirmation_option(prompt='Are you sure want to delete the network ?')
@click.argument('nodes', required=False, nargs=-1)
@click.pass_context
def delete(ctx, nodes):
    """Delete network"""
    click.echo('Deleting {0} in {1} ...'.format(nodes or 'ALL NODES', ctx.obj['name']), err=True)
    iaws.delete(ctx.obj['name'], nodes, fast=ctx.obj['fast'])
    click.echo(click.style('Done', fg='green') + ' ... Bye.', err=True)


# sync
@cli.command(help='Sync network info from aws to local')
@click.option('--prune', is_flag=True, help='Prune local config if necessary.')
@click.pass_context
def sync(ctx, prune):
    click.echo('Syncing from aws ...', err=True)
    iaws.sync(ctx.obj['name'], prune_local=prune)
    click.secho('Done.', err=True, fg='green')


# scale
@cli.command()
@click.option('--confirmed', is_flag=True, help='Scale network without confirming.')
@click.pass_context
def scale(ctx, confirmed):
    """Scale network according to local config"""
    click.echo('Scaling {0} ...'.format(ctx.obj['name'], ), err=True)
    iaws.scale(ctx.obj['name'], confirmed=confirmed)
    click.echo(click.style('Done', fg='green') + ' ... Have fun !', err=True)


# ls
@cli.command()
@click.pass_context
def ls(ctx):
    """List nodes in network (list)"""
    iaws.list_print(ctx.obj['name'])


# aws subgroup
@cli.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS_SHORT_H, help="Operate aws ec2")
@click.pass_context
def ec2(ctx):
    """Operate ec2 using aws api"""
    pass

# start
@ec2.command(short_help="Start nodes")
@click.confirmation_option(prompt='Are you sure want to start the node(s) ?')
@click.option('--dry-run', is_flag=True, help='Show info without execute.')
@click.argument('nodes', required=True)
@click.pass_context
def start(ctx, nodes, dry_run):
    """Start nodes, split by comma."""
    click.echo('Starting {0} in {1} ...'.format(nodes, ctx.obj['name']), err=True)
    iaws.start(ctx.obj['name'], nodes, dry_run=dry_run)
    click.echo(click.style('Done', fg='green') + ' ... Done.', err=True)

# stop
@ec2.command(short_help="Stop nodes")
@click.confirmation_option(prompt='Are you sure want to stop the node(s) ?')
@click.option('--dry-run', is_flag=True, help='Show info without execute.')
@click.argument('nodes', required=True)
@click.pass_context
def stop(ctx, nodes, dry_run):
    """Stop nodes, split by comma."""
    click.echo('Stopping {0} in {1} ...'.format(nodes, ctx.obj['name']), err=True)
    iaws.stop(ctx.obj['name'], nodes, dry_run=dry_run)
    click.echo(click.style('Done', fg='green') + ' ... Done.', err=True)

# reboot
@ec2.command(short_help="Reboot nodes")
@click.confirmation_option(prompt='Are you sure want to reboot the node(s) ?')
@click.option('--dry-run', is_flag=True, help='Show info without execute.')
@click.argument('nodes', required=True)
@click.pass_context
def reboot(ctx, nodes, dry_run):
    """Reboot nodes, split by comma."""
    click.echo('Rebooting {0} in {1} ...'.format(nodes, ctx.obj['name']), err=True)
    iaws.reboot(ctx.obj['name'], nodes, dry_run=dry_run)
    click.echo(click.style('Done', fg='green') + ' ... Done.', err=True)

# status
@ec2.command(short_help="Show nodes status")
@click.argument('nodes', required=False, default='all')
@click.pass_context
def status(ctx, nodes):
    """Show nodes status, split by comma. [default: (all)]"""
    iaws.status(ctx.obj['name'], nodes)


#
# deploy playbook
#

# start
@cli.command()
@click.option('--gen-kp', is_flag=True, help='Generate keypair')
@click.argument('subset')
@click.pass_context
def init(ctx, gen_kp, subset):
    """Config and start a brand new cluster"""
    if gen_kp:
        gen_iserver_config(ctx.obj['name'], gen_kp=gen_kp)
    play_wrap(get_path(ctx.obj['name'], 'inventory'), 'init', subset)


# restart
@cli.command()
@click.argument('subset')
@click.pass_context
def restart(ctx, subset):
    """Restart iserver on nodes"""
    play_wrap(get_path(ctx.obj['name'], 'inventory'), 'restart', subset)


# reload
@cli.command()
@click.option('-s', '--static', is_flag=True, help='Using static config file instead of template')
@click.argument('subset')
@click.pass_context
def reload(ctx, static, subset):
    """Upload config to nodes and reload iserver"""
    play_wrap(get_path(ctx.obj['name'], 'inventory'), 'reload', subset, '{static: ' + str(static) + '}')


# deploy
@cli.command()
@click.option('--obo', is_flag=True, help='Mode one by one')
@click.option('--skip-build', help='Skip build and set image tag.\nTHIS OPTION WILL OVERRIDE SPEC !!')
@click.argument('subset')
@click.argument('spec')
@click.pass_context
def deploy(ctx, obo, skip_build, subset, spec):
    """Deploy code of spec to nodes"""
    args = ['commit=' + spec]
    if skip_build:
        args.append('image=' + skip_build)
        args.append('skip=true')
        args.append('use_builder=0')
    if obo:
        args.append('serial=1')

    play_wrap(get_path(ctx.obj['name'], 'inventory'), 'deploy', subset, *args)


# start
@cli.command()
@click.argument('subset')
@click.pass_context
def start(ctx, subset):
    """Start iserver on nodes"""
    play_wrap(get_path(ctx.obj['name'], 'inventory'), 'start', subset)


# stop
@cli.command()
@click.argument('subset')
@click.pass_context
def stop(ctx, subset):
    """Stop iserver on nodes"""
    play_wrap(get_path(ctx.obj['name'], 'inventory'), 'stop', subset)


# clean
@cli.command()
@click.argument('subset')
@click.pass_context
def clean(ctx, subset):
    """Clean data on nodes"""
    play_wrap(get_path(ctx.obj['name'], 'inventory'), 'clean', subset)


# backup
@cli.command()
@click.argument('subset')
@click.pass_context
def backup(ctx, subset):
    """Backup data on node"""
    play_wrap(get_path(ctx.obj['name'], 'inventory'), 'backup', subset)


# restore
@cli.command()
@click.option('--src', '-s', required=True, help='Src node')
@click.argument('node_dst')
@click.confirmation_option(prompt='This command will purge data on dest node, are you sure to continue?')
@click.pass_context
def restore(ctx, node_dst, src):
    """Restore data on node_dst with help of node_src"""
    node_src = src
    play_wrap(get_path(ctx.obj['name'], 'inventory'), 'restore', node_dst, 'from_node=' + node_src)


# genconfig
@cli.command()
@click.pass_context
def genconfig(ctx):
    """Generate iserver config statically."""
    play_wrap(get_path(ctx.obj['name'], 'inventory'), 'genconfig', 'all')
    click.secho('Done!', fg='green')
    click.echo('Check `genesis.yml` and `iserver.yml_*` at `' +
               get_path(ctx.obj['name'], 'config', expand_home=False) + '`.')
    click.secho('Then try `idevops reload <SUBSET> -s` to upload static config files.')


#
# ssh
#

# ssh
@cli.command(short_help="A wrapper around `ssh`", context_settings=CONTEXT_SETTINGS_WRAPPER)
@click.pass_context
def ssh(ctx):
    """A wrapper around `ssh`

    See `man ssh`
    """
    call(['ssh', '-F', get_path(ctx.obj['name'], 'ssh')]
         + ctx.args)


# scp
@cli.command(short_help="A wrapper around `scp`", context_settings=CONTEXT_SETTINGS_WRAPPER)
@click.pass_context
def scp(ctx):
    """A wrapper around `scp`

    See `man scp`
    """
    call(['scp', '-F', get_path(ctx.obj['name'], 'ssh')]
         + ctx.args)


# rsync
@cli.command(short_help="A wrapper around `rsync`", context_settings=CONTEXT_SETTINGS_WRAPPER)
@click.pass_context
def rsync(ctx):
    """A wrapper around `rsync`

    See `rsync -h`
    """
    call(['rsync', '-e', 'ssh -F ' + get_path(ctx.obj['name'], 'ssh')]
         + ctx.args)


#
# ansible
#

# run ansible
@cli.command(short_help="A wrapper around `ansible`", context_settings=CONTEXT_SETTINGS_WRAPPER)
@click.pass_context
def ansible(ctx):
    """Run ansible

    See `ansible -h`
    """
    call(['ansible', '-i', get_path(ctx.obj['name'], 'inventory')]
         + ctx.args, env=ENV)


# run ansible-playbook
@cli.command(short_help="A wrapper around `ansible-playbook`", context_settings=CONTEXT_SETTINGS_WRAPPER)
@click.option('--list', is_flag=True, callback=list_playbooks, expose_value=False,
              is_eager=True, help='List all available playbooks')
@click.argument('playbook')
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def playbook(ctx, playbook, args):
    """Run ansible-playbook

    See `ansible-playbook -h`
    """
    call([
             'ansible-playbook', '-b',
             '-i', get_path(ctx.obj['name'], 'inventory'),
         ] + list(args) + [find_playbook(playbook)], env=ENV
         )


# run ansible-console
@cli.command(short_help="A wrapper around `ansible-console`", context_settings=CONTEXT_SETTINGS_WRAPPER)
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def console(ctx, args):
    """Run ansible-console

    See `ansible-console -h`
    """
    call([
             'ansible-console', '-b',
             '-i', get_path(ctx.obj['name'], 'inventory'),
             '-l', 'all:!worker',
         ] + list(args), env=ENV
         )


#
# beta
#

# ec2 test
@cli.command(context_settings=CONTEXT_SETTINGS_WRAPPER)
@click.option('--bandwidth', '-b', is_flag=True, help='Bandwidth test.')
@click.option('--latency', '-l', is_flag=True, help='Latency test.')
@click.option('--io', '-i', is_flag=True, help='Disk IO test.')
@click.option('--debug', is_flag=True, help='Debug mode.')
@click.pass_context
def test(ctx, bandwidth, latency, io, debug):
    """Perform test"""
    click.echo('Performing test ...')
    iptest_fields = []
    if bandwidth:
        iptest_fields.append('bandwidth')
    if latency:
        iaws.open_icmp(ctx.obj['name'])
        iptest_fields.append('latency')
    if io:
        iptest_fields.append('io')
    if len(iptest_fields) > 0:
        t = __import__('idevops.ansible.run_test', fromlist=['run_test'])
        if t.run_test(ctx.obj['name'], fields=iptest_fields, debug=debug) != 0:
            click.secho('Run test(s) failed.', fg='red')

    # cleanup
    if latency:
        iaws.close_icmp(ctx.obj['name'])


# pumba wrapper
@cli.command(short_help="A wrapper around `pumba` container", context_settings=CONTEXT_SETTINGS_WRAPPER)
@click.option('--one-line', '-o', is_flag=True, help='Condense output.')
@click.option('--name', is_flag=True, help='Named container `pumba`.')
@click.option('--limit', '-l', help='Limit selected hosts to an additional pattern.',
              default='all', show_default='all')
@click.pass_context
def pumba(ctx, one_line, name, limit):
    """Run pumba command using docker

    See `pumba help`
    """
    _prefix = 'docker run ' + ('--name pumba ' if name else '') + '--rm -v /var/run/docker.sock:/var/run/docker.sock gaiaadm/pumba'
    call(['ansible', '-bo' if one_line else '-b', '-i', get_path(ctx.obj['name'], 'inventory'),
          '-a', ' '.join([_prefix] + ctx.args), limit], env=ENV)


# hook in setup.py
def main():
    try:
        cli(obj={})
    except (ConstructorError, ParserError) as e:
        click.secho(str(e), fg='red')
        click.echo('Config parsing failed.')
        return 1
    except AssertionError as e:
        if isinstance(e.args[0], ErrMsg):
            click.secho(e.args[0].msg, fg='red')
            click.echo(e.args[0].ctx.get_help())
        else:
            click.secho(str(e), fg='red')
        return 2
    except ClientError as e:
        click.secho(str(e), fg='red')
        click.echo('You might need to wait some minutes, or to delete the network, or have deleted it already.')
        return 3
    except NoCredentialsError as e:
        click.secho(str(e), fg='red')
        click.echo('Run `idevops configure`.')
        return 3
