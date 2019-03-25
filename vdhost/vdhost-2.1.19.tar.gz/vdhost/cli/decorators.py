from colored import fg, stylize, attr
import requests
import vdhost.cli.env as env
import os
import json
from requests.compat import urljoin


def ensure_vd_dir_exists():
    # ensures /var/vectordash exists with the proper directory structure

    # setting up /var/vectordash if it doesn't exist
    if not os.path.isdir(env.BASE_INSTALL_PATH):
        os.mkdir(env.BASE_INSTALL_PATH)
        paths = [
            os.path.join(env.BASE_INSTALL_PATH, 'config'),
            os.path.join(env.BASE_INSTALL_PATH, 'disks'),
            os.path.join(env.BASE_INSTALL_PATH, 'vms'),
            os.path.join(env.BASE_INSTALL_PATH, 'roms'),
            os.path.join(env.BASE_INSTALL_PATH, 'client'),
        ]

        # creating all the paths
        for path in paths:
            os.mkdir(path)


def auth_required(function):
    # A decorator used to ensure a vdhost command can only be run with authentication.
    ensure_vd_dir_exists()

    def auth_wrapper(*args, **kwargs):

        # first we attempt to read the email and machine secret from a JSON
        login_file = os.path.join(env.BASE_INSTALL_PATH, 'config/login.json')

        # if the login file does not exist
        if not os.path.isfile(login_file):
            print("You must be logged in to proceed. Please run " +
                  stylize("vdhost login", fg("blue")))
            return

        # opening the login file
        with open(login_file, 'r') as f:
            data = json.load(f)

        post_data = {
            'email': data['email'],
            'machine_secret': data['machine_secret']
        }

        # checking if these details are valid
        r = requests.post(
            url=urljoin(env.BASE_API_URL, 'api/hosting/get-auth-status/'),
            data=post_data
        )
        r.raise_for_status()

        # whether or not the login credentials are valid
        valid = r.json()['valid']

        if valid:
            # calling the function if the auth passed
            return function(*args, **kwargs)
        else:
            print("The provided login details were invalid. Please run " +
                  stylize("vdhost login", fg("blue")))
            return

    # returning the decorator
    return auth_wrapper


def install_required(function):
    # a decorator to wrap functions which can only be called after
    # a machine has successfully installed everything

    def wrapper(*args, **kwargs):

        # if the flag exists, the installation is complete
        flag = os.path.join(env.BASE_INSTALL_PATH, 'config/installation_complete_flag')
        if os.path.isfile(flag):
            return function(*args, **kwargs)

        # otherwise we need to prompt for installation
        else:
            print("Please complete the Vectordash installation before proceeding: " +
                  stylize("sudo vdhost install", fg("blue")))
            return

    # returning the decorator
    return wrapper
