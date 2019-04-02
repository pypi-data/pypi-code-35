import click
import vdhost.cli.commands as cmd


@click.group()
def cli():
    pass


# adding the commands to the click group

# setup commands
cli.add_command(cmd.login)
cli.add_command(cmd.install)
cli.add_command(cmd.run_tests)
cli.add_command(cmd.read_ram)

# client commands
cli.add_command(cmd.start_client)
cli.add_command(cmd.stop_client)
cli.add_command(cmd.status)
cli.add_command(cmd.set_vbios)
