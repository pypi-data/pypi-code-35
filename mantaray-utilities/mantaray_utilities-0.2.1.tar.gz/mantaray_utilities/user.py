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
import random

from squid_py.accounts.account import Account
from squid_py.keeper import Keeper
from squid_py.keeper.web3_provider import Web3Provider


# os.environ['PASSWORD_PATH']


def get_account_from_config(config, config_account_key, config_account_password_key):
    """ Get the account as specified in the config file

    :param config:
    :param config_account_key:
    :param config_account_password_key:
    :return:
    """
    address = config.get('keeper-contracts', config_account_key)
    address = Web3Provider.get_web3().toChecksumAddress(address)
    password = config.get('keeper-contracts', config_account_password_key)

    logging.info("Account:{}={} {}={} ".format(config_account_key, address,config_account_password_key, password))
    return Account(address, password)


def password_map(address, password_dict):
    """Simple utility to match lowercase addresses to the password dictionary

    :param address:
    :param password_dict:
    :return:
    """
    lower_case_pw_dict = {k.lower(): v for k, v in password_dict.items()}
    if str.lower(address) in lower_case_pw_dict:
        password = lower_case_pw_dict[str.lower(address)]
        return password
    else:
        return False


def load_passwords_environ():
    assert 'PASSWORD_PATH' in os.environ
    return load_passwords(os.environ['PASSWORD_PATH'])

def load_passwords(path_passwords):
    """Load password file into an address:password dictionary

    :param path_passwords:
    :return: dict
    """

    assert os.path.exists(path_passwords), "Password file not found: {}".format(path_passwords)
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


def get_account(ocn):
    """Utility to get a random account
    Account exists in the environment variable for the passwords filej
    Account must have a password
    Account must have positive ETH balance

    :param ocn:
    :return:
    """
    password_dict = load_passwords_environ()

    addresses = [str.lower(addr) for addr in password_dict.keys()]

    possible_accounts = list()
    for acct in ocn.accounts.list():
        # Only select the allowed accounts
        if str.lower(acct.address) not in addresses:
            continue
        # Only select accounts with positive ETH balance
        if ocn.accounts.balance(acct).eth/10**18 < 1:
            continue
        possible_accounts.append(acct)

    this_account = random.choice(possible_accounts)
    this_account.password = password_map(this_account.address, password_dict)
    assert this_account.password, "No password loaded for {}".format(this_account.address)
    return this_account

def get_account_by_index(ocn, acct_number):
    """Utility to get one of the available accounts by index (as listed in the password file)
    Account exists in the environment variable for the passwords file
    Account must have password

    :param ocn:
    :param acct_number:
    :return:
    """
    password_dict = load_passwords_environ()

    addresses = [str.lower(addr) for addr in password_dict.keys()]

    possible_accounts = list()
    for acct in ocn.accounts.list():
        # Only select the allowed accounts
        if str.lower(acct.address) not in addresses:
            continue
        possible_accounts.append(acct)

    this_account = possible_accounts[acct_number]
    this_account.password = password_map(this_account.address, password_dict)
    assert this_account.password, "No password loaded for {}".format(this_account.address)
    return this_account


