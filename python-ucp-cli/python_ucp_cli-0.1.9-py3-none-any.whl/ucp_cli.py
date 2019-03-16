import click

import commands.config as Config
import commands.auth as auth
import commands.subjects as subjects
import commands.client as client

pass_config = click.make_pass_decorator(Config.Config, ensure=True)

@click.group()
def cli():
    pass

cli.add_command(auth.login)
cli.add_command(auth.env)
cli.add_command(subjects.org)
cli.add_command(subjects.team)
cli.add_command(subjects.user)
cli.add_command(client.install_cli)

if __name__ == '__main__':
    cli()