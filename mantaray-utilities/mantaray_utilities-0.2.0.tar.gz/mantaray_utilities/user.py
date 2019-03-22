"""
The User() class, a helper class for simulating users of Ocean Protocol.
"""
import logging
import configparser
import logging
from .config import get_config_file_path, get_deployment_type, get_project_path
from squid_py.ocean.ocean import Ocean
from pathlib import Path
# assert PATH_CONFIG.exists(), "{} does not exist".format(PATH_CONFIG)
# PATH_CONFIG = get_config_file_path()
import csv
import os

from squid_py.accounts.account import Account
from squid_py.keeper import Keeper
from squid_py.keeper.web3_provider import Web3Provider

def get_account_from_config(config, config_account_key, config_account_password_key):
    address = config.get('keeper-contracts', config_account_key)
    address = Web3Provider.get_web3().toChecksumAddress(address)
    password = config.get('keeper-contracts', config_account_password_key)

    logging.info("Account:{}={} {}={} ".format(config_account_key, address,config_account_password_key, password))
    return Account(address, password)



def password_map(address, password_dict):
    if str.lower(address) in password_dict:
        password = password_dict[str.lower(address)]
        return password
        # logging.debug("Found password".format())
    else:
        return False

def load_passwords(path_passwords):
    # Get passwords from account, password CSV file
    assert os.path.exists(path_passwords)
    passwords = dict()
    with open(path_passwords) as f:
        for row in csv.reader(f):
            if row:
                passwords[row[0]] = row[1]

    passwords = {k.lower(): v for k, v in passwords.items()}
    logging.info("{} account-password pairs loaded".format(len(passwords)))
    return passwords

def get_password(path_passwords, account):
    passwords = load_passwords(path_passwords)

