import click
import os
import subprocess

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
dir_path = os.path.dirname(os.path.realpath(__file__))

def get_script_path(script_name):
  script_path = os.path.join(dir_path, "scripts/%s" % script_name)
  return script_path


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Simple CLI for building akka http project
    """
    pass

@click.group(help="create project for yours")
def create():
    pass

@click.command(help="install dependency for hakka-cli")
def install():
    script_path = get_script_path("install.sh")
    subprocess.check_call([script_path], shell=True)

@click.group(help="choice your projects")
def projects():
    pass

@projects.command()
def akkaHttp():
    ## sbt로 scala project를 생성.
    subprocess.call("g8 https://github.com/heesuk-ahn/hakka-http-template")

def main():
    cli.add_command(create)
    cli.add_command(install)
    create.add_command(projects)
    cli()
    create()

if __name__ == "__main__":
    main()

