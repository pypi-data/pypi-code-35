import re
import sys
import time
from argparse import ArgumentParser

import boto3.session

from .deploy import DeploymentWatcher
from .logs import find_log_groups


def main():
    argp = ArgumentParser(description='Observe Codedeploy deployments')
    argp.add_argument(
        '--deployment-id', required=True,
        help='ID of the Codedeploy deployment to watch')
    argp.add_argument(
        '--log-group-prefix',
        help='Prefix of the Cloudwatch log group names to follow')
    argp.add_argument(
        '--log-group-pattern', type=re.compile,
        help='Regular expression for matching the Cloudwatch log group names '
             'to follow. Use it only for selections that can\'t be done with '
             'just the prefix, as this will require loading all the groups and'
             'filtering locally.')
    args = argp.parse_args()

    session = boto3.session.Session()
    log_group_names = list(find_log_groups(session, args.log_group_prefix,
                                           args.log_group_pattern))

    print('log_group_names:', log_group_names)

    watcher = DeploymentWatcher(
        session, args.deployment_id, log_group_names, out_file=sys.stderr)

    watcher.update()
    if watcher.is_finished():
        watcher.display()
    else:
        while True:
            watcher.follow()
            if watcher.is_finished():
                break

            time.sleep(5)

    if watcher.status != 'Succeeded':
        sys.exit(1)
