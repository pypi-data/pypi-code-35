
import os
from os.path import expanduser
import logging
from logging.handlers import RotatingFileHandler
from msi_auth import MSIAuth
from aad_auth import AADAuth


# Specify files accessed by this script in guestshell
base_dir = expanduser('~') + '/cloud/authMgr/'
debug_file = base_dir + "token_svr.log"
aad_app_file = base_dir + "aad_app_file"

if not os.path.exists(base_dir):
    os.makedirs(base_dir)

default_msi_app = None
default_aad_app = None
aad_app_list = []


def find_aad_app(tenant_id, app_id, app_key):
    global aad_app_list
    for app in aad_app_list:
        if (app.app_id == app_id and
            app.tenant_id == tenant_id and
            app.app_key == app_key):
            # Found a match. Return this app.
            return app
    return None


def set_default_msi_app(logger):
    global default_msi_app
    msi_app = MSIAuth(logger)
    if msi_app is not None:
        default_msi_app = msi_app
        # Check if we got a token
        if msi_app.token == '':
            return 'ERR: Failed to obtain token using MSI application'
        else:
            return 'OK'
    else:
        return 'ERR: Failed to set default MSI application'


def set_default_aad_app(logger, cloud, tenant_id, app_id, app_key):
    global default_aad_app
    aad_app = AADAuth(logger, cloud, tenant_id, app_id, app_key)
    if aad_app is not None:
        default_aad_app = aad_app
        write_table_to_file()
        # Check if we got a token
        if aad_app.token == '':
            return 'ERR: Failed to obtain token for default AAD application'
        else:
            return 'OK'
    else:
        return 'ERR: Failed to set default AAD application'


def clear_default_aad_app():
    global default_aad_app
    default_aad_app = None
    if os.path.exists(aad_app_file):
        cmd = "rm %s" % aad_app_file
        os.system(cmd)
    return 'OK'


def clear_aad_app_list():
    global aad_app_list
    aad_app_list = []
    return 'OK'


def verify_aad_app(logger, cloud, tenant_id, app_id, app_key):
    # Try to find this application on the existing AAD app list
    app = find_aad_app(tenant_id, app_id, app_key)
    if app is not None:
        # Application is verified. Return the app
        return app

    # This is a new application.  Try to get a token using it.
    app = AADAuth(logger, cloud, tenant_id, app_id, app_key)
    token = app.get_token()
    if token != '':
        # New application is verified. Add it to the list.
        aad_app_list.append(app)
        return app
    else:
        # Get of the token failed
        logger.error("AAD application with app_id %s failed to obtain a token" % app_id)
        return None

def get_token(logger, app=None):
    global aad_app_list
    if app is not None:
        # Get the token using the specified application
        token = app.get_token()
        if token == '':
            # Check if this app is on the verified list and remove it
            for entry in aad_app_list:
                if (entry.cloud == app.cloud and
                    entry.app_id == app.app_id and
                    entry.tenant_id == app.tenant_id and
                    entry.app_key == app.app_key):
                    logger.error("AAD application with app_id %s has been invalidated" % app.app_id)
                    aad_app_list.remove(entry)
                    break
        return token

    # If no app was specified, try the default AAD app
    if default_aad_app is not None:
        token = default_aad_app.get_token()
        return token

    # If all else fails, try the default MSI app
    if default_msi_app is not None:
        token = default_msi_app.get_token()
        return token

    logger.error("No authentication application found for getting a token")
    return ''

def refresh_token(logger, app=None):
    global aad_app_list
    if app is not None:
        return app.refresh_token()

    # If no app was specified, try the default AAD app
    if default_aad_app is not None:
        return default_aad_app.refresh_token()

    # If all else fails, try the default MSI app
    if default_msi_app is not None:
        return default_msi_app.refresh_token()

    logger.error("No authentication application found for refreshing a token")
    return 'ERR: No authentication application found for refreshing a token'

def clear_token(logger, app=None):
    global aad_app_list
    if app is not None:
        return app.clear_token()

    # If no app was specified, try the default AAD app
    if default_aad_app is not None:
        return default_aad_app.clear_token()

    # If all else fails, try the default MSI app
    if default_msi_app is not None:
        return default_msi_app.clear_token()

    logger.error("No authentication application found for clearing a token")
    return 'ERR: No authentication application found for clearing a token'

def write_table_to_file():
    with open(aad_app_file, 'w') as write_fh:
        app_desc = "{cloud: %s, app_id: %s, tenant_id: %s, app_key: %s}" % (default_aad_app.cloud, default_aad_app.app_id, default_aad_app.tenant_id, default_aad_app.app_key)
        out_str = str(app_desc) + '\n'
        print "Writing app_desc to file"
        print "%s" % out_str
        write_fh.write(out_str)

def read_table_from_file(logger):
    if os.path.exists(aad_app_file):
        with open(aad_app_file, 'r') as read_fh:
            for line in read_fh:
                input_str = line.strip()
                print "Read table from file"
                print "%s" % input_str
                substr1 = input_str.replace('{', '')
                substr2 = substr1.replace('}', '')
                # Separate items into list of strings
                list_of_pairs = substr2.rsplit(',')
                # Create an empty dict
                out_var={}
                for list_entry in list_of_pairs:
                    # Split the entry into a key and value
                    key_value_pair = list_entry.rsplit(':')
                    key = key_value_pair[0].strip()
                    value = key_value_pair[1].strip()
                    out_var[key] = value
                set_default_aad_app(logger, out_var['cloud'], out_var['app_id'], out_var['tenant_id'], out_var['app_key'])


def show():
    global default_msi_app, default_aad_app, aad_app_list
    buf = ''
    if default_msi_app is not None:
        buf = buf + "\nDefault MSI application:"
        buf = buf + default_msi_app.show()
    else:
        buf = buf + "\nNo default MSI application is configured"

    if default_aad_app is not None:
        buf = buf + "\nDefault AAD application:"
        buf = buf + default_aad_app.show()
    else:
        buf = buf + "\nNo default AAD application is configured"

    if len(aad_app_list) > 0:
        buf = buf + "\nListing all node-based AAD applications:"
        for app in aad_app_list:
            buf = buf + app.show()
            buf = buf + "\n"
    else:
        buf = buf + "\nNo node-based AAD applications are configured"
    return buf
