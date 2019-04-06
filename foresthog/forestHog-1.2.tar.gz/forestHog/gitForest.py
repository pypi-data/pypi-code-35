import os
import git
import sys
import json
import stat
import shutil
import argparse
import subprocess

from .forestHog import bcolors


def get_params():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='defines foresthog operations.',
                        choices=['init', 'run', 'update', 'destroy'])

    parser.add_argument(
        '-trigger', help='runs forestHog for certain git event.',
        choices=['pre-push', 'post-commit'])
    parser.add_argument(
        '-custom-rules', default=dict(),
        help='custom rules files to check the git repo against.')

    parser.add_argument('-entropy-wc', default=0, type=int,
                        help='sets string length for calculating entropy.')
    parser.add_argument('-entropy-hex-thresh', default=0, type=float,
                        help='sets entropy threshold for hex strings.')
    parser.add_argument('-entropy-b64-thresh', default=0, type=float,
                        help='sets entropy threshold for base64 strings.')
    parser.add_argument('--no-regex', action='store_true',
                        help='disables regex checks for git repo.')
    parser.add_argument('--no-default-rules', action='store_true',
                        help='disables default rule checks for git repo.')
    parser.add_argument('--no-entropy', action='store_true',
                        help='disables entropy checks for git repo.')
    parser.add_argument('--no-pre-push', action='store_true',
                        help='disables pre-push hook to git repo.')
    parser.add_argument('--no-post-commit', action='store_true',
                        help='disables post-commit hook to git repo.')

    args = parser.parse_args()
    return args


def get_git_root():

    git_repo = git.Repo(os.getcwd(), search_parent_directories=True)
    git_root = git_repo.git.rev_parse('--show-toplevel')
    return git_root


def get_custom_rules(custom_rules):

    if isinstance(custom_rules, str):
        if not os.path.isfile(custom_rules):
            print('WARNING: could not read the file for '
                  'custom rules:', custom_rules)
            return custom_rules
        try:
            rules = json.load(open(custom_rules))
            if not isinstance(rules, dict):
                print('WARNING: expected custom rules file '
                      'to have a dict:', custom_rules)
                return custom_rules
            return rules
        except json.JSONDecodeError:
            print('WARNING: could not decode custom rules file:', custom_rules)
            return custom_rules

    if isinstance(custom_rules, dict):
        return custom_rules


def initialize(params):

    root = get_git_root()
    if not root:
        print('FATAL: not a git repo.')
        exit(1)

    hooks_dir = os.path.join(root, '.git', 'hooks')
    if not os.path.isdir(hooks_dir):
        print('FATAL: could not find hooks directory for git.')
        exit(1)

    forest_dir = os.path.join(root, '.forest')
    if not os.path.isdir(forest_dir):
        os.mkdir(forest_dir)

    data = {
        'custom_rules': get_custom_rules(params.custom_rules),
        'entropy_wc': params.entropy_wc or 20,
        'entropy_hex_thresh': params.entropy_hex_thresh or 3.0,
        'entropy_b64_thresh': params.entropy_b64_thresh or 4.5,
        'enable_default_rules': not params.no_default_rules,
        'enable_regex': not params.no_regex,
        'enable_entropy': not params.no_entropy,
        'pre_push': not params.no_pre_push,
        'post_commit': not params.no_post_commit
    }

    config_filename = os.path.join(forest_dir, 'config.json')
    json.dump(data, open(config_filename, 'w'), indent=2)
    print('git-forest has been initialized: %s' % (config_filename))
    print(json.dumps(data, indent=2), end='\n\n')

    triggers = ['pre-push', 'post-commit']
    for trigger in triggers:
        hookname = os.path.join(hooks_dir, trigger)
        if os.path.isfile(hookname):
            os.rename(hookname, os.path.join(hooks_dir, '%s.bkp' % (trigger)))

        f = open(hookname, 'w')
        f.write('%s run -trigger %s' % (os.path.join(os.path.dirname(
            sys.executable), 'git-forest'), trigger))
        f.close()

        print('Changing hook permissions. ', end='')
        fstat = os.stat(hookname)
        os.chmod(hookname, fstat.st_mode | stat.S_IXUSR |
                 stat.S_IXGRP | stat.S_IXOTH)
        print('Hook added: %s' % os.path.join(hooks_dir, trigger))


def update(params):

    root = get_git_root()
    if not root:
        print('FATAL: not a git repo.')
        exit(1)

    hooks_dir = os.path.join(root, '.git', 'hooks')
    if not os.path.isdir(hooks_dir):
        print('FATAL: could not find hooks directory for git.')
        exit(1)

    forest_dir = os.path.join(root, '.forest')
    if not os.path.isdir(forest_dir):
        print('FATAL: could not find .forest directory at git root.')
        exit(1)

    config_filename = os.path.join(forest_dir, 'config.json')
    try:
        config = json.load(open(config_filename))
        for key, value in config.items():
            if not value and isinstance(value, bool):
                config[key] = True

        if params.no_default_rules:
            config['enable_default_rules'] = not params.no_default_rules
        if params.no_regex:
            config['enable_regex'] = not params.no_regex
        if params.no_entropy:
            config['enable_entropy'] = not params.no_entropy
        if params.no_pre_push:
            config['pre_push'] = not params.no_pre_push
        if params.no_post_commit:
            config['post_commit'] = not params.no_post_commit
        if params.custom_rules:
            config['custom_rules'] = get_custom_rules(params.custom_rules)
        if params.entropy_wc:
            config['entropy_wc'] = params.entropy_wc
        if params.entropy_hex_thresh:
            config['entropy_hex_thresh'] = params.entropy_hex_thresh
        if params.entropy_b64_thresh:
            config['entropy_b64_thresh'] = params.entropy_b64_thresh

        json.dump(config, open(config_filename, 'w'), indent=2)
        print('git-forest config has been updated: %s' % (config_filename))
        print(json.dumps(config, indent=2), end='\n\n')

    except json.JSONDecodeError:
        print('FATAL: could not decode JSON config.')
        exit(1)


def run(params):

    root = get_git_root()
    if not root:
        print('FATAL: not a git repo.')
        exit(1)

    forest_dir = os.path.join(root, '.forest')
    if not os.path.isdir(forest_dir):
        print('Could not detect .forest directory at git root.')
        exit(1)

    config_filename = os.path.join(forest_dir, 'config.json')
    try:
        config = json.load(open(config_filename))
    except json.JSONDecodeError:
        print('Could not decode config JSON: %s' % (config_filename))
        exit(1)

    args = list()
    if config.get('enable_regex'):
        args.append('--regex')

    if config.get('enable_entropy'):
        args.append('--entropy')

    if config.get('entropy_wc'):
        args.append('--entropy-wc')
        args.append(config['entropy_wc'])

    if config.get('entropy_hex_thresh'):
        args.append('--entropy-hex-thresh')
        args.append(config['entropy_hex_thresh'])

    if config.get('entropy_b64_thresh'):
        args.append('--entropy-b64-thresh')
        args.append(config['entropy_b64_thresh'])

    if config.get('custom_rules'):
        tmp_rules = os.path.join(forest_dir, '.tmp.rules')
        json.dump(config['custom_rules'], tmp_rules)

        if config.get('enable_default_rules'):
            args.append('--add-rules')
            args.append(tmp_rules)
        elif not config.get('enable_default_rules'):
            args.append('--rules')
            args.append(tmp_rules)

    args.append(root)
    args = [str(x) for x in args]
    if (config.get('pre_push') and params.trigger == 'pre-push') or \
            (config.get('post_commit') and params.trigger == 'post-commit'):

        print('Running `foresthog` to analyze code...\nargs:', *args)
        command = os.path.join(os.path.dirname(sys.executable), 'foresthog')
        proc = subprocess.Popen(
            [command, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = proc.communicate()
        rcode = proc.returncode
        out = out.decode('utf8').strip('\n')
        if out:
            print(out)
        if rcode is 0:
            message = '-'*10 + ' [Code analysis PASSED.] ' + '-'*10
            message = bcolors.OKGREEN + message + bcolors.ENDC
        else:
            message = '>'*10 + ' [Code analysis FAILED.] ' + '<'*10
            message = bcolors.FAIL + message + bcolors.ENDC

        print(message, end='\n\n')
        exit(rcode)


def destroy(params):

    root = get_git_root()
    if not root:
        print('FATAL: not a git repo.')
        exit(1)

    hooks_dir = os.path.join(root, '.git', 'hooks')
    if not os.path.isdir(hooks_dir):
        print('FATAL: could not find hooks directory for git.')
        exit(1)

    forest_dir = os.path.join(root, '.forest')
    if not os.path.isdir(forest_dir):
        print('WARNING: could not find .forest directory at git root.')
    else:
        shutil.rmtree(forest_dir)
        print('Removed .forest folder from git root.')

    for trigger in ['pre-push', 'post-commit']:
        hookname = os.path.join(hooks_dir, trigger)
        if os.path.isfile(hookname):
            os.rename(hookname, hookname + '.bkp')
            print('Hook disconnected and changed to:', hookname + '.bkp')


def main():

    params = get_params()
    if params.command == 'init':
        initialize(params)
    elif params.command == 'run':
        run(params)
    elif params.command == 'update':
        update(params)
    elif params.command == 'destroy':
        destroy(params)


if __name__ == "__main__":
    main()
