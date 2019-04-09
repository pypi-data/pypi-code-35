"""
Summary.
    List iam keyset operations (read-only)

"""

import os
import sys
import datetime
import inspect
import pytz
from botocore.exceptions import ClientError
from pyaws.session import boto3_session
from pyaws.utils import stdout_message
from pyaws.colors import Colors
from keyup.colormap import ColorMap
from keyup.script_utils import convert_dt_time
from keyup.statics import local_config
from keyup import logger


try:
    from keyup.oscodes_unix import exit_codes
    os_type = 'Linux'
    splitchar = '/'                             # character for splitting paths (linux)
    text = Colors.BRIGHT_CYAN
except Exception:
    from keyup.oscodes_win import exit_codes    # non-specific os-safe codes
    os_type = 'Windows'
    splitchar = '\\'                            # character for splitting paths (windows)
    text = Colors.CYAN

# globals
cm = ColorMap()


# universal colors
rd = Colors.RED
act = Colors.ORANGE
yl = Colors.YELLOW
fs = Colors.GOLD3
bd = Colors.BOLD
frame = text
bdwt = cm.bdwt
rst = Colors.RESET


global KEYAGE_MIN
KEYAGE_MIN = datetime.timedelta(days=local_config['KEY_METADATA']['KEYAGE_MIN_DAYS'])

global KEYAGE_MAX
KEYAGE_MAX = datetime.timedelta(days=local_config['KEY_METADATA']['KEYAGE_MAX_DAYS'])


def key_age(create_dt):
    """
    Summary.
        Calculates Access key age from today given it's creation date

    Args:
        - **create_dt (datetime object)**: the STS CreateDate parameter returned
          with key key_metadata when an iam access key is created

    Returns:
        TYPE: str, age from today in human readable string format

    """
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    delta_td = now - create_dt
    readable_age = convert_dt_time(delta_td)
    return readable_age, delta_td


def list_keys(account, profile, iam_user, surrogate='', stage=None, quiet=False):
    """
    Summary.
        Displays available access keys for user to stdout

    Args:
        :account (str): AWS account number
        :profile (str): name of the iam user for which we are interrogating keys
        :iam_user (str): name of the iam user which corresponds to profile name
         from local awscli configuration
        :stage (str): stage of key rotation; ie, either BEFORE | AFTER rotation
        :quiet (bool): No output to stdout (True) | Show output (False)

    Returns:
        TYPE: list, AccessKeyIds listed for the IAM user

    """
    client = boto3_session(service='iam', profile=profile)
    mode = local_config['LOGGING']['LOG_MODE']

    try:
        if surrogate:
            r = client.list_access_keys(UserName=surrogate)
        else:
            r = client.list_access_keys()
    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDenied' and surrogate:
            stdout_message(
                ('User %s has inadequate permissions for key operations\n\t     on user %s - Exit [Code: %d]' %
                 (profile, surrogate, exit_codes['EX_NOPERM']['Code'])),
                prefix='PERM', severity='WARNING'
                )
            logger.warning(exit_codes['EX_NOPERM']['Reason'])
            sys.exit(exit_codes['EX_NOPERM']['Code'])
        elif e.response['Error']['Code'] == 'AccessDenied':
            stdout_message(
                ('%s: User %s has inadequate permissions to conduct key operations. Exit [Code: %d]'
                 % (inspect.stack()[0][3], profile, exit_codes['EX_NOPERM']['Code'])),
                prefix='AUTH', severity='WARNING')
            logger.warning(exit_codes['EX_NOPERM']['Reason'])
            sys.exit(exit_codes['EX_NOPERM']['Code'])
        elif e.response['Error']['Code'] == 'NoSuchEntity':
            tab = '\n\t'.expandtabs(12)
            user = rd + bd + (surrogate if surrogate else profile) + rst
            stdout_message(
                    ('User %s does not exist in local awscli profiles %s for AWS Account %s [Code: %d]'
                    % (user, tab, bdwt + account + rst, exit_codes['EX_AWSCLI']['Code'])),
                    prefix='USER',
                    severity='WARNING'
                )
            logger.warning(exit_codes['EX_AWSCLI']['Reason'])
            sys.exit(exit_codes['EX_AWSCLI']['Code'])
        else:
            logger.warning(
                '%s: Inadequate User permissions (Code: %s Message: %s)' %
                (inspect.stack()[0][3], e.response['Error']['Code'],
                 e.response['Error']['Message']))
            raise e

    if r['ResponseMetadata']['HTTPStatusCode'] == 200:
        # collect key metadata
        access_keys = [x['AccessKeyId'] for x in r['AccessKeyMetadata']]
        num_keys = len(access_keys)    # number keys assoc w/ iam user

        # display access keys for user
        account_stats = [
            ('AWS Account Id: %s' % account),
            ('IAM user id: %s' % (surrogate if surrogate else iam_user)),
            ('profile_name from local awscli config: %s' % profile)
        ]
        if quiet:
            for cmd in account_stats:
                logger.info(cmd)
        else:
            # print account metadata to stdout -- header
            if stage:   # active rotation
                stage = (
                        '\n\t'.expandtabs(4) + '________________________________\n\n' +
                        ('\t').expandtabs(12) + Colors.BOLD + stage +
                        '\n\t'.expandtabs(4) + '________________________________'
                    )
                stage_accent = Colors.YELLOW if 'BEFORE' in stage else Colors.GREEN
                title = (
                        bdwt + '\n\tAccess Key List'.expandtabs(12) +
                        stage_accent + stage +
                        '\n' + Colors.RESET
                    )
            else:
                # list operation only, no rotation
                title = (bdwt + '\n\t    Access Key List\n' + Colors.RESET)

            # print body
            print(
                title + '\n  AWS Account:\t\t' + account +
                '\n  ------------------------------------------'
                )
            print('  IAM User: \t\t%s' % (surrogate if surrogate else iam_user))
            print('  Profile Name: \t%s\n' % profile)
            # log record
            for cmd in account_stats:
                logger.info(cmd)

        # iterate thru keys, output to log + stdout
        for ct, key in enumerate(r['AccessKeyMetadata']):
            age, age_td = key_age(key['CreateDate'])

            if age_td > KEYAGE_MAX:
                age = Colors.RED + age + Colors.RESET
            # log metadata
            logger.info(
                'AccessKeyId (%s) found for user %s. ' %
                (key['AccessKeyId'], (surrogate if surrogate else iam_user))
                )
            logger.info(
                'Key CreateDate: %s. Key Age: %s' %
                (key['CreateDate'].strftime("%Y-%m-%dT%H:%M:%SZ"), age)
                )
            if quiet:
                logger.info('Quiet mode, suppress list_keys stdout')
            else:
                # print all key metadata to stdout
                if num_keys > 1:
                    ct = ct + 1
                    keyinfo_header = Colors.BOLD + Colors.ORANGE + '  AccessKeyId ' + str(ct) + ': '
                else:
                    keyinfo_header = Colors.BOLD + Colors.ORANGE + '  AccessKeyId: \t'
                print(
                    keyinfo_header +
                    '\t' + Colors.ORANGE + key['AccessKeyId'] + Colors.RESET + Colors.BOLD +
                    '\n  CreateDate:  ' + Colors.RESET + '\t\t' +
                    key['CreateDate'].strftime("%Y-%m-%d %H:%M UTC") + Colors.BOLD +
                    '\n  Age: \t\t\t' + Colors.RESET + age +
                    '\n  Status: ' + Colors.RESET + '\t\t' + key['Status'] + '\n'
                    )
    else:
        raise OSError(
             '%s: Problem retrieving access keys for user profile: %s' %
             (inspect.stack()[0][3], profile)
             )
    return access_keys, r['AccessKeyMetadata']


def query_keyinfo(account, profile, surrogate='', quiet=False):
    """
    Summary:
        Retrieves available access keys for profile user

    Args:
        :account (str): AWS account number
        :profile (str): name of the iam user for which we are interrogating keys
        :iam_user (str): name of the iam user which corresponds to profile name
         from local awscli configuration
        :stage (str): stage of key rotation; ie, either BEFORE | AFTER rotation
        :quiet (bool): No output to stdout (True) | Show output (False)

    Returns:
        TYPE: list, AccessKeyIds listed for the IAM user

    """
    client = boto3_session(service='iam', profile=profile)

    try:
        if surrogate:
            r = client.list_access_keys(UserName=surrogate)
        else:
            r = client.list_access_keys()

    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDenied' and surrogate:
            stdout_message(
                ('User %s has inadequate permissions for key operations\n\t     on user %s - Exit [Code: %d]' %
                 (profile, surrogate, exit_codes['EX_NOPERM']['Code'])),
                prefix='PERM', severity='WARNING'
                )
            logger.warning(exit_codes['EX_NOPERM']['Reason'])
            sys.exit(exit_codes['EX_NOPERM']['Code'])

        elif e.response['Error']['Code'] == 'AccessDenied':
            stdout_message(
                ('%s: User %s has inadequate permissions to conduct key operations. Exit [Code: %d]'
                 % (inspect.stack()[0][3], profile, exit_codes['EX_NOPERM']['Code'])),
                prefix='AUTH', severity='WARNING')
            logger.warning(exit_codes['EX_NOPERM']['Reason'])
            sys.exit(exit_codes['EX_NOPERM']['Code'])

        elif e.response['Error']['Code'] == 'NoSuchEntity':
            tab = '\n\t'.expandtabs(12)
            user = rd + bd + (surrogate if surrogate else profile) + rst
            stdout_message(
                    ('User %s does not exist in local awscli profiles %s for AWS Account %s [Code: %d]'
                    % (user, tab, bdwt + account + rst, exit_codes['EX_AWSCLI']['Code'])),
                    prefix='USER',
                    severity='WARNING')
            logger.warning(exit_codes['EX_AWSCLI']['Reason'])
            sys.exit(exit_codes['EX_AWSCLI']['Code'])

        else:
            logger.warning(
                '%s: Inadequate User permissions (Code: %s Message: %s)' %
                (inspect.stack()[0][3], e.response['Error']['Code'],
                 e.response['Error']['Message']))
            raise e
        return r['AccessKeyMetadata']
