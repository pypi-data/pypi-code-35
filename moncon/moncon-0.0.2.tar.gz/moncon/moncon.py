import os
import sys
import argparse
import configparser
from pprint import pprint
import requests

_VALUES_BOOL = ('enable', 'disable')
_VALUES_LONG_RUNNING = ('notify', 'kill', 'notifyandkill')

_ACTIONS = {
    'alerts': _VALUES_BOOL,
    'datacollection': _VALUES_BOOL,
    'sniffer': _VALUES_BOOL,
    'longrunningqueries': _VALUES_BOOL,
    'lockedqueries': _VALUES_BOOL,
    'longrunningqueryaction': _VALUES_LONG_RUNNING
}


def get_actions(d=_ACTIONS):
    return d.keys()


def get_values(a, d=_ACTIONS):
    return d[a]


def check_action_value(a, v, d=_ACTIONS):
    if a in get_actions(d):
        if v in get_values(a, d):
            return True
        else:
            return False
    else:
        drama("Unknown action: {}".format(a))


def drama(msg, x=1):
    print(msg)
    sys.exit(x)


def cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', default=5555)
    parser.add_argument('--user')
    parser.add_argument('--password')
    parser.add_argument('--server')
    parser.add_argument('--tags')
    parser.add_argument('--action', required=True)
    parser.add_argument('--value', required=True)
    parser.add_argument('--dry-run', action='store_true', default=False)
    args = parser.parse_args()

    cfg = {
        'host': str(args.host),
        'port': str(args.port),
        'dry_run': args.dry_run}

    cfg['object'] = 'MONyogAPI'

    if check_action_value(args.action, args.value, _ACTIONS):
        cfg['action'] = args.action
        cfg['value'] = args.value

    if args.server and args.tags:
        drama("Choose only one of --server or --tags")

    if args.server:
        cfg['target'] = '_server={}'.format(args.server)
    elif args.tags:
        cfg['target'] = '_tags={}'.format(args.tags)
    else:
        drama("Need at least one of --server or --tags")

    if args.password:
        cfg['password'] = str(args.password)
    if args.user:
        cfg['user'] = str(args.user)

    return cfg


def my_cnf():
    cnf_path = os.path.expanduser('~/.my.cnf')
    if os.path.isfile(cnf_path):
        return cnf_path
    else:
        return False


def system_cnf():
    paths = ('/usr/local/MONyog/MONyog.ini',
             '/etc/my.cnf',
             '/etc/my.cnf.d/mariadb.cnf')
    found_files = []
    for i in paths:
        if os.path.isfile(i) and os.access(i, os.W_OK):
            found_files.append(i)
            break
    if found_files:
        return found_files
    else:
        return False


def read_config(cnf_path, section='monyog'):
    cfg = configparser.ConfigParser(allow_no_value=True)
    cfg.read(cnf_path)
    if section in cfg.sections():
        return dict(cfg[section])
    else:
        return False


def read_configs(section='monyog'):
    my_cnf_file = my_cnf()
    system_cnf_files = system_cnf()
    if my_cnf_file:
        cfg = read_config(my_cnf_file, section)
    elif system_cnf_files:
        #  Read files in paths in a linear order.
        #  Break as soon as we find valid monyog details.
        for i in system_cnf_files:
            if read_config(i, section):
                cfg = i
                break
    else:
        sys_paths = ', '.join(system_cnf_files)
        sys.exit("No {s} found in {m} or any of: {c}".format(
            s=section,
            m=my_cnf_file,
            c=sys_paths))

    return cfg


def monyog_cfg(cfg: dict = cli_args()):
    file_cfg = read_configs()
    cli_cfg = cfg.copy()
    cfg = dict()

    if file_cfg:
        cfg.update(file_cfg)

    if cli_cfg:
        cfg.update(cli_cfg)

    url_template = (
        "http://{host}:{port}/"
        "?_object={object}"
        "&_action={action}"
        "&_value={value}"
        "&_user={user}"
        "&_password={password}"
        "&{target}")

    fmt_url = url_template.format(**cfg)
    cfg['url'] = fmt_url
    return cfg


def monyog_cmd(cfg: dict = monyog_cfg()):
    if cfg['dry_run']:
        pprint(cfg)
        return
    else:
        r = requests.get(cfg['url'])
        check_status(r.json())
        return


def check_status(status):
    if status['STATUS'] == 'FALIURE':
        drama(status['RESPONSE'])
    else:
        drama(status['RESPONSE'], 0)


def main():
    monyog_cmd()
