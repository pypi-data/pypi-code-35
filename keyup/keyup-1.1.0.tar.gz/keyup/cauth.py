"""
Summary.

        Centralized Authentication Module

Steps.
    - retrieve list of all profilenames
    - map each profile to an iam username; if cannot be mapped,
      discard as not associated with main iam username
    - find key expiration for each iam_username which match the aws account of primary profile given

"""

import os
import sys
import json
import asyncio
import datetime
import inspect
import pytz
import time
import unicodedata
from botocore.exceptions import ClientError

# 3rd party
from veryprettytable import VeryPrettyTable
from pyaws.session import boto3_session
from pyaws.utils import export_json_object, stdout_message
from pyaws.colors import Colors
from keyup.iam_operations import local_profilenames
from keyup.map import map_identity, map_iam_username
from keyup.list_ops import query_keyinfo, KEYAGE_MAX
from keyup.script_utils import convert_timedelta
from keyup.statics import local_config
from keyup import keyconfig, logger


try:
    from keyup.oscodes_unix import exit_codes
    os_type = 'Linux'
    splitchar = '/'                             # character for splitting paths (linux)
    text = Colors.BRIGHTCYAN
except Exception:
    from keyup.oscodes_win import exit_codes    # non-specific os-safe codes
    os_type = 'Windows'
    splitchar = '\\'                            # character for splitting paths (windows)
    text = Colors.CYAN


# universal colors
rd = Colors.RED + Colors.BOLD
yl = Colors.YELLOW + Colors.BOLD
fs = Colors.GOLD3
bd = Colors.BOLD
gn = Colors.BRIGHTGREEN
frame = text
btext = text + Colors.BOLD
bdwt = Colors.BOLD + Colors.BRIGHTWHITE
ub = Colors.UNBOLD
cmark = unicodedata.lookup('heavy check mark')
xmark = unicodedata.lookup('LIGHT SALTIRE')
rst = Colors.RESET


class authentication():
    def __init__(self, profile):
        self.profile_name = profile
        self.iam_user = None
        self.access_key = None
        self.secret_key = None

        if (self.access_key or self.secret_key) is None:
            self.generate_token(self.iam_user)

    def generate_token(self, user):
        pass


def convert(dt):
    """Convert days to hours"""
    expiration_date = dt + KEYAGE_MAX
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    if now < expiration_date and (expiration_date - now).days == 0:
        return (expiration_date - now).seconds / 3600


def discover_account_affiliations():
    """
    Summary.
        associates each profile name in local awscli configuration
        to an iam username and an AWS Account Number

    Returns:
        affiliation info, TYPE: dict

    .. code: javascript

        {
            profile_name: {
                "account": 104713565656,
                "iam_user": admin-sandbox2
            }
        }

    """
    affiliations = {}

    for profile in local_profilenames():
        try:
            iam_user, aws_account = map_identity(profile)
            affiliations[profile] = {'iam_user': iam_user, 'account': aws_account}
        except ClientError as e:
            fname = inspect.stack()[0][3]
            logger.info(
                '{}: Unable to locate aws account for profile {}'.format(fname, profile))
            continue
    return affiliations


def expired_keys(dt):
    """
    Summary.

        Convert datetime objects into human readable
    """
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    delta_td = now - dt
    if delta_td < KEYAGE_MAX:
        return False
    return True


def display_table(table, tabspaces=4):
    """Print Table Object offset from left by tabspaces"""
    indent = ('\t').expandtabs(tabspaces)
    table_str = table.get_string()
    for e in table_str.split('\n'):
        print(indent + frame + e)
    sys.stdout.write(Colors.RESET + '\n\n\n')
    return True


def print_header(title, indent=4, spacing=4):
    divbar = frame + '-'
    upbar = frame + '|' + rst
    ltab = '\t'.expandtabs(indent)              # lhs indentation of title bar
    spac = '\t'.expandtabs(7)             # rhs indentation of legend from divider bar
    tab4 = '\t'.expandtabs(4)                   # space between legend items
    tab5 = '\t'.expandtabs(5)                   # space between legend items
    tab6 = '\t'.expandtabs(6)                   # space between legend items
    tab2 = '\t'.expandtabs(2)
    valid = '{} valid{}'.format(gn + bd + 'o' + rst, tab5)
    near = '{} near expiration{}'.format(yl + bd + 'o' + rst, tab5)
    exp = '{} expired'.format(rd + bd + 'o' + rst)
    # output header
    print('\n\n\n')
    print(tab4, end='')
    print(divbar * 118, end='')
    print('\n' + tab4 + upbar + frame + '\t|'.expandtabs(59) + rst + frame + '\t|'.expandtabs(56) + rst)
    print('{}{}{}{}{}{}'.format(tab4 + upbar + ltab, title + spac, valid, near, exp, tab6 + upbar))
    print(tab4 + upbar + frame + '\t|'.expandtabs(59) + rst + frame + '\t|'.expandtabs(56) + rst)
    return True


def time_remaining(dt):
    """Calculate the days until expiration"""
    expiration_date = dt + KEYAGE_MAX
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    if now < expiration_date:
        return (expiration_date - now).days
    return rd + 'expired' + rst


def report_complete():
    return True


def setup_table(user_data):
    # setup table
    x = VeryPrettyTable(border=True, header=True, padding_width=2)
    field_max_width = 70

    x.field_names = [
        bdwt + 'ProfileName' + frame,
        bdwt + 'IAM User' + frame,
        bdwt + 'AWS AccountId' + frame,
        bdwt + 'CreateDate' + frame,
        bdwt + 'Time Remaining' + frame,
        bdwt + 'Status' + frame,
    ]

    # cell alignment
    x.align[bdwt + 'ProfileName' + frame] = 'l'
    x.align[bdwt + 'IAM User' + frame] = 'l'
    x.align[bdwt + 'AWS AccountId' + frame] = 'l'
    x.align[bdwt + 'CreateDate' + frame] = 'c'
    x.align[bdwt + 'Time Remaining' + frame] = 'c'
    x.align[bdwt + 'Status' + frame] = 'c'

    # populate table
    for k, v in user_data.items():

            dt = v['CreateDate']
            expired = expired_keys(v['CreateDate'])
            _days = time_remaining(dt)

            if not expired and (0 <= _days < KEYAGE_WARNING):
                # close to expiration, warning
                profilename = yl + k + rst
                user = yl + v['iam_user'] + rst
                accountId = yl + v['account'] + rst
                createdate = yl + dt.strftime('%b %d, %Y %H:%M UTC') + rst
                remaining = yl + str(_days) + ' days' + rst if _days > 1 else yl + str(_days) + ' day' + rst
                status = yl + cmark + rst

                # < 1 day remains; calculate hours remaining
                if _days == 0:
                    remaining = yl + str(int(round(convert(dt)))) + ' hours' + rst

            else:
                #  key credentials are either expired (age > KEYAGE_MAX) or valid
                profilename = rd + k + rst if expired else k
                user = rd + v['iam_user'] + rst if expired else v['iam_user']
                accountId = rd + v['account'] + rst if expired else v['account']
                createdate = rd + dt.strftime('%b %d, %Y %H:%M UTC') + rst if expired else dt.strftime('%b %d, %Y %H:%M UTC')
                remaining = str(_days) + ' days' if type(_days) is int else rd + '-' + rst
                status = (rd + xmark + rst if expired else gn + bd + cmark + rst)

                if _days == 1:
                    remaining = str(_days) + ' day'

            x.add_row(
                [
                    rst + profilename + frame,
                    rst + user + frame,
                    rst + accountId + frame,
                    rst + createdate + frame,
                    rst + remaining + frame,
                    rst + status + frame
                ]
            )

    # Table
    vtab_int = 8
    vtab = '\t'.expandtabs(vtab_int)
    msg = '{}AWS Identity Access Key Expiration Report{}{}|{}'.format(btext, ub, vtab, rst)
    print_header(title=msg, indent=10, spacing=vtab_int)
    display_table(x, tabspaces=4)
    return report_complete()


def source_globals():
    """
    global environment variable definitions
    """
    global KEYAGE_WARNING
    KEYAGE_WARNING = local_config['KEY_METADATA']['KEYAGE_WARNING']


async def prepare_report(debug=False):
    """
    Summary.

        Prints out key expiration info for all profilenames associated with
        the primary profilename given to access the account information

    """
    try:

        source_globals()

    except KeyError:
        # remove offending configuration file, then recreate
        if os.path.exists(local_config['PROJECT']['CONFIG_PATH']):
            os.remove(local_config['PROJECT']['CONFIG_PATH'])
        return keyconfig.option_configure(False, local_config['PROJECT']['CONFIG_PATH'])

    data, aliases = {}, {}
    exceptions = []
    affiliations = discover_account_affiliations()

    if debug:
        export_json_object(affiliations)

    for k, v in affiliations.items():

        account = v['account']

        try:
            r = None
            client = boto3_session(service='iam', profile=k)
            r = client.list_access_keys()
            key_metadata = r['AccessKeyMetadata']

            await asyncio.sleep(0.001)

            if debug:
                stdout_message(
                    message='Key information received for profile {}'.format(bd + k + rst),
                    prefix='OK'
                )

        except ClientError as e:
            fname = inspect.stack()[0][3]
            logger.exception('{}: Unable to list key info for profile {}'.format(fname, k))
            exceptions.append(k)
            continue

        try:

            if aliases.get(account):
                alias = aliases[account]
            else:
                # human readable name of the account
                alias = client.list_account_aliases()['AccountAliases'][0]

                # store identified aliases
                aliases[account] = alias

        except ClientError:
            alias = ''

        accountId = alias or account
        iam_user = key_metadata[0]['UserName']
        status = key_metadata[0]['Status']
        metadata = key_metadata[0]['CreateDate']

        data[k] = {
            'account': accountId,
            'iam_user': iam_user,
            'status': status,
            'CreateDate': metadata
        }
        logger.info('IAM User {} key info found for AWS account {}'.format(iam_user, accountId))
    return setup_table(data)
