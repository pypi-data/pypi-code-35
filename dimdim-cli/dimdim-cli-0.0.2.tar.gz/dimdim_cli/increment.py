import argparse
import json
import logging
import os
import re

import requests

LOG_LEVEL = os.environ.get('INCREMENT_LOG_LEVEL', 'WARNING')
LOG_FORMAT = "[%(asctime)s] %(levelname)-8s %(message)s"
REGEX = r'(\d)\.(\d{1,2})\.(\d{1,3})'
REGEX_REL = r'(\d)\.(\d{1,2})\.(\d{1,3})(a|b|c|rc)?(\d)?'
CI_PROJECT_ID = os.environ.get('CI_PROJECT_ID')

API_URL = os.environ.get('CI_API_V4_URL', 'https://gitlab.com/api/v4')

headers = {
    'PRIVATE-TOKEN': os.environ.get('CI_JOB_TOKEN')
}

class KeyNotSetError(AttributeError):
    def __str__(self):
        return 'The key "%s" was not set.' % self.args[0]


def get_project_ci_secret_key_url(project_id, name):
    if not name:
        raise KeyNotSetError(name)
    url = '%s/projects/%s/variables/%s' % (API_URL, project_id, name)
    logging.debug('%s: %s', name, url)
    return url


def get_old_version_from_repo(url):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    logging.debug('Get %s', json.dumps(data))
    return data.get('value')


def update_ci_env_key(url, version, method='update'):
    data = {'value': version}
    if method == 'update':
        r = requests.update(url, headers=headers, data=data)
    else:
        r = requests.post(url, headers=headers, data=data)
    r.raise_for_status()
    return version


def new_version_num(version, semantic='patch'):
    logging.info('old version %s', version)
    match = re.match(REGEX, version)
    version_list = match.groups()
    major = int(version_list[0])
    minor = int(version_list[1])
    patch = int(version_list[2])
    v = {'major': major, 'minor': minor, 'patch': patch}
    if semantic == 'major':
        v['minor'] = v['patch'] = 0
    elif semantic == 'minor':
        v['patch'] = 0
    v[semantic] += 1
    version = "%d.%d.%d" % (v['major'], v['minor'], v['patch'])
    logging.info('new version %s', version)
    return version


def main():
    parser = argparse.ArgumentParser(
        description="Util for CI semantic version operations variables"
    )
    parser.add_argument('-pk', '--pkey', help='project version key',
                        required=False)
    parser.add_argument(
        '-n', '--name',
        help='increment key name',
        required=False
    )
    parser.add_argument("--debug", action="store_true", help="debug mode")
    parser.add_argument("--dry-run", action="store_true",
                        help="not update actually")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="verbose mode")
    parser.add_argument('-s', '--semantic', default='patch',
                        choices=['major', 'minor', 'patch'])
    parser.add_argument('--method', default='get',
                        choices=['get', 'create', 'update'])
    parser.add_argument('--current', action="store_true",
                        help="Return current version")
    args = parser.parse_args()
    if not CI_PROJECT_ID:
        raise KeyNotSetError('CI_PROJECT_ID')
    method = args.method
    semantic = args.semantic
    current = args.current
    level = LOG_LEVEL
    key_name = args.name or os.environ.get('VERSION_KEY', 'PROJECT_VERSION')
    com = 'Set %s level\n[Current] %s [Method] %s' % (level, current, method)

    if args.debug:
        level = 'DEBUG'
    elif args.verbose:
        level = 'INFO'
        logging.getLogger("requests").setLevel(logging.WARNING)
    logging.basicConfig(level=logging.getLevelName(level), format=LOG_FORMAT)
    logging.debug(com)
    logging.debug('Semantic version: %s', semantic)
    if not key_name:
        logging.debug('Key name: %s', key_name)
        raise KeyNotSetError(key_name)
    else:
        logging.info('Key name: %s', key_name)
    url = get_project_ci_secret_key_url(CI_PROJECT_ID, key_name)
    _old_version = args.pkey or os.environ.get(key_name)
    old_version = _old_version or get_old_version_from_repo(url)
    if method == 'get':
        if args.current:
            print(old_version)
        else:
            new_version = new_version_num(old_version, semantic=semantic)
            print(new_version)
    elif method in ('create', 'update'):
        new_version = new_version_num(old_version, semantic=semantic)
        if args.dry_run:
            logging.info('Url is %s', url)
            logging.info('headers: %s', headers)
        else:
            version = update_ci_env_key(url=url, method=method,
                                        version=new_version, )
            if args.current:
                print(version)
            else:
                print(new_version_num(old_version))


if __name__ == '__main__':
    main()
