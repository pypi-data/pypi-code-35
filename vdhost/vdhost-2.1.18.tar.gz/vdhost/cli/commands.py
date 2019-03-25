import click
import subprocess
import os
import requests
from requests.compat import urljoin
import json
from colored import fg, stylize, attr
from vdhost.cli.decorators import auth_required, install_required
import vdhost.cli.env as env

"""
Contains the vdhost command line commands.
"""

# stylized strings used for different prompts
SUDO_PROMPT = stylize("You must run this command with sudo.", fg("red"))
NO_STOP_PROMPT = stylize("You cannot stop vdhost when an instance is being actively hosted.", fg("red"))
INVALID_LOGIN_PROMPT = stylize("The provided login details were invalid.", fg("red"))

# the installation prompt
INSTALLATION_PROMPT = "This command will begin the Vectordash host installation process.\n" \
                      "Please note that this can take upwards of an hour to complete.\n" \
                      "If prompted with any selections, please select ENTER to pick the default values.\n" \
                      "Would you like to begin the host installation process now? " + \
                      '%s%s[yes/no]%s ' % (fg('orchid'), attr('bold'), attr('reset'))

# the path to login.json
LOGIN_FILE = os.path.join(env.BASE_INSTALL_PATH, 'config/login.json')
INSTALLATION_FILE = os.path.join(env.BASE_INSTALL_PATH, 'client/install.sh')
CLIENT_CONFIG_FILE = LOGIN_FILE = os.path.join(env.BASE_INSTALL_PATH, 'config/client_config.json')


@click.command(name='install')
@auth_required
def install():
    # Installs the Vectordash hosting client.

    # getting the credentials
    with open(LOGIN_FILE, 'r') as f:
        data = json.load(f)

    post_data = {
        'email': data['email'],
        'machine_secret': data['machine_secret']
    }
    # getting the hosting package
    r = requests.post(
        url=urljoin(env.BASE_API_URL, 'api/hosting/get-hosting-package/'),
        data=post_data
    )
    r.raise_for_status()

    # writing out the contents we received to a tarball
    open('/tmp/vectordash-host.tar.gz', 'wb').write(r.content)

    # unzipping the tarball
    command = ['sudo', 'tar', '-C', os.path.join(env.BASE_INSTALL_PATH),
               '-xvf', '/tmp/vectordash-host.tar.gz', '--strip-components=1']

    # calling the unzip command
    subprocess.call(command, stdout=subprocess.PIPE)

    # delete the tarball once the unzip has been completed
    os.remove('/tmp/vectordash-host.tar.gz')

    # displaying the prompt and asking the user if they want to continue with the installation process
    response = input(INSTALLATION_PROMPT)

    if "y" not in response:
        return

    # Running the installation script
    args = ['bash', '/var/vectordash/client/install.sh']

    try:
        subprocess.check_call(args)
    except OSError:
        print(SUDO_PROMPT)


@click.command(name='login')
def login():
    # Prompts the user for their login credentials and saves them if valid.

    # prompting the user for their details
    email = input(stylize("Email: ", fg("blue"))).strip()
    machine_secret = input(stylize("Machine secret: ", fg("blue"))).strip()

    # creating a request to validate the credentials
    data = {'email': email, 'machine_secret': machine_secret}
    url = urljoin(env.BASE_API_URL, 'api/hosting/get-auth-status/')

    # making the request
    r = requests.post(url, data)
    r.raise_for_status()
    valid = r.json()['valid']

    if not valid:
        print(INVALID_LOGIN_PROMPT)
        return

    # if valid, we save the values to login.json
    try:
        with open(LOGIN_FILE, 'w') as f:
            data = {'email': email, 'machine_secret': machine_secret}
            json.dump(data, f)
    except OSError:
        print(SUDO_PROMPT)
        return

    print(stylize("Login information saved.", fg("green")))
    return


@click.command(name='set-vbios')
@click.argument('addresses', nargs=-1)
@auth_required
@install_required
def set_vbios(addresses):
    """
    Download VBIOS's for all the GPUs
    """

    cmd = 'python3.7 /var/vectordash/client/rom_utils.pyc '

    # add the arguments (pci addresses) to the
    for addr in addresses:
        # strip the addr
        addr = addr.strip()

        # if it's an actual argument, add it to the command
        if addr != '':
            cmd += addr + ' '

    cmd = cmd.strip()

    # execute the command
    subprocess.call(cmd, shell=True)


@click.command(name='run-tests')
@click.option('--no-reset', is_flag=True, help="Will print verbose messages.")
@click.option('--no-games', is_flag=True, help="Will print verbose messages.")
@auth_required
@install_required
def run_tests(no_reset, no_games):
    """
    Runs the host tests post-installation.
    This is simply a wrapper around host_tests.pyc.
    """

    cmd = "python3.7 /var/vectordash/client/host_tests.pyc "
    if no_reset:
        cmd += "--no-reset "
    if no_games:
        cmd += "--no-games "

    cmd = cmd.strip()

    # execute the command
    subprocess.call(cmd, shell=True)


@click.command(name='read-ram')
@auth_required
@install_required
def read_ram():
    """
    Runs the host tests post-installation.
    This is simply a wrapper around host_tests.pyc.
    """
    subprocess.call("python3.7 /var/vectordash/client/installation_utils.pyc", shell=True)


@click.command(name='start')
@click.option('--no-games', is_flag=True, help="Will print verbose messages.")
@auth_required
@install_required
def start_client(no_games):

    # client arg dict
    client_arg_dict = {}
    client_arg_dict['no_games'] = False
    if no_games:
        client_arg_dict['no_games'] = True
    with open(CLIENT_CONFIG_FILE, 'w') as f:
        json.dump(client_arg_dict, CLIENT_CONFIG_FILE)

    # starts the Vectordash client
    try:
        subprocess.call("sudo supervisorctl start vdhost", shell=True)
    except OSError:  # if we get a permissions error
        print(SUDO_PROMPT)


@click.command(name='stop')
@auth_required
@install_required
def stop_client():
    # stops the Vectordash client

    # checking if we are allowed to stop
    with open(LOGIN_FILE, 'r') as f:
        data = json.load(f)

    post_data = {
        'email': data['email'],
        'machine_secret': data['machine_secret']
    }
    # checking if these details are valid
    r = requests.post(
        url=urljoin(env.BASE_API_URL, 'api/hosting/can-stop/'),
        data=post_data
    )
    r.raise_for_status()

    # whether or not we can stop
    can_stop = r.json()['can_stop']

    if can_stop:
        try:
            subprocess.call("sudo supervisorctl stop vdhost", shell=True)
        except OSError:  # if we get a permissions error
            print(SUDO_PROMPT)
    else:
        print(NO_STOP_PROMPT)


@click.command(name='status')
@install_required
def status():
    # Returns the status of the Vectordash client via supervisor
    try:
        subprocess.call("sudo supervisorctl status vdhost", shell=True)
    except OSError:  # if we get a permissions error
        print(SUDO_PROMPT)

