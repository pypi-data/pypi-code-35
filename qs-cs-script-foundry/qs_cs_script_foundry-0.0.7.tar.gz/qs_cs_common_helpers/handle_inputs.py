import click
from commands.config_command import ConfigCommandExecutor
from commands.update_script import script_updater
from commands.update_driver import driver_updater
from utilities import config_reader
from shellfoundry.models.install_config import InstallConfig, DEFAULT_HOST, DEFAULT_PORT, DEFAULT_USERNAME, \
    DEFAULT_PASSWORD, DEFAULT_DOMAIN, DEFAULT_AUTHOR, DEFAULT_ONLINE_MODE, DEFAULT_TEMPLATE_LOCATION

@click.group()
def cli():
    pass

@click.option('--type', default='', help='script or driver are supported')
@click.option('--name', help="custom name for the script (optional)")
@cli.command()
def update(type, name):
    if type:
        credentials = build_credentials()
        # print credentials
        # print type
        if type.lower() == 'driver':
            click.echo('uploading driver'.format(name))
            if name == '':
                name = None
            update_driver(credentials=credentials, custom_driver_name=name)
        elif type.lower() == 'script':
            click.echo('uploading script'.format(name))
            if name == '':
                name = None
            update_script(credentials=credentials, custom_script_name=name)
        else:
            print ('no type selected or unsupported type')
            exit(11)
    else:
        print ('no type selected or unsupported type')
        exit(12)

@cli.command()
def config():
    a = ConfigCommandExecutor(global_cfg=True)
    a.config()


def build_credentials():
    creader = config_reader.Configuration(config_reader.CloudShellConfigReader())
    config_data = creader.read()
    credentials = {
        'domain': config_data.domain,
        'server': config_data.host,
        'user': config_data.username,
        'password': config_data.password
    }
    return credentials

def update_script(credentials, custom_script_name=None):
    script_updater_instance = script_updater(credentials=credentials, custom_script_name=custom_script_name)
    script_updater_instance.load_to_cs()


def update_driver(credentials, custom_driver_name=None):
    driver_updater_instance = driver_updater(credentials=credentials, custom_driver_name=custom_driver_name)
    driver_updater_instance.load_to_cs()