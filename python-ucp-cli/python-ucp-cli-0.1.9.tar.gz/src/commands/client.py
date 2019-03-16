import click
import json
import sys
import requests
from urllib.request import urlopen, urlretrieve
from .config import Config
from apis import version as version_api
import platform
#from clint.textui import progress
from tempfile import NamedTemporaryFile
from shutil import copyfileobj, copyfile

pass_config = click.make_pass_decorator(Config, ensure=True)

def download_kube_client(k8sversion):
    linux_url = "https://storage.googleapis.com/kubernetes-release/release/{}/bin/linux/amd64/kubectl".format(k8sversion)
    macos_url = "https://storage.googleapis.com/kubernetes-release/release/{}/bin/darwin/amd64/kubectl".format(k8sversion)
    url = None
    current_platform = platform.system()

    if current_platform == 'Darwin':
        url = macos_url
    elif current_platform == 'Linux':
        url = linux_url
    else:
        raise Exception('Unexpected platform. Neither Darwin or Linux: {}'.format(current_platform))

    msg = ("Downloading client to \"/usr/local/bin/kubectl\" from {}".format(url))
    click.echo(msg)

    try:
        urlretrieve(url, "/usr/local/bin/kubectl")
    except EnvironmentError:
        click.echo("Error cannot save file to /usr/local/bin/kubectl")
    else:
        click.echo("Please ensure that /usr/local/bin is in your search PATH, so the `kubectl` command can be found.")
 

# install-cli command
@click.command('install-cli')
@pass_config
def install_cli(config):
    base_url = config.get_url()
    auth_token = config.get_authtoken()
    result = version_api.get_version(base_url, auth_token)
    
    componentsList = json.loads(result)['Components'] 
    kubeComponent = None
    for component in componentsList:
        if component['Name'] == "Kubernetes":
            ComponentDetails = component['Details']
            gitVersion = ComponentDetails['gitVersion']
            versionArray = gitVersion.split('-')
            k8sversion = versionArray[0]
            download_kube_client(k8sversion)
            break
