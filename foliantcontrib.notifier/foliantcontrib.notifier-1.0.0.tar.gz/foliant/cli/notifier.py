'''GitLab notifier configurator.'''

import os
import yaml

from pathlib import Path, PosixPath

from cliar import set_help, set_arg_map, set_metavars

from foliant.cli.base import BaseCli
from foliant.config import Parser


class Cli(BaseCli):
    config_section = 'notifier'
    defaults = {
        'repo_url': 'https://gitlab.com/ddddsa/gitlab_notifier.git',
        'config': 'notifier_config.yml',
        'stage': 'notify',
        'job': 'notifier',
        'image': 'python:latest',
        # 'mail_config': 'default',
        'branches': ['develop'],
        'python': 3
    }
    py3 = {
        'pip': 'pip3',
        'python': 'python3'
    }
    py2 = {
        'pip': 'pip',
        'python': 'python'
    }

    def _get_config(self, config: dict):
        result = self.defaults
        result.update(config)
        return result

    def _gen_job(self, config):
        python = self.py3 if config['python'] == 3 else self.py2

        result = {'stage': config['stage'],
                  'allow_failure': True,
                  'script': [f'git clone {config["repo_url"]}',
                             f'{python["pip"]} install -r ./gitlab_notifier/requirements.txt',
                             f'{python["python"]} ./gitlab_notifier/gitlab_notifier.py -c {config["config"]}'],
                  'only': config['branches'],
                  'tags': ['lowcapacity'],
                  'variables': {'GIT_STRATEGY': 'fetch'}}
        if config['image']:
            result['image'] = config['image']
        return result

    def _gen_ci_config(self, config):
        result = {'image': 'python:latest',
                  'stages': [config['stage']],
                  config['job']: self._gen_job(config)}
        return result

    def _update_ci_config(self, ci_config: PosixPath, config: dict):
        with open(ci_config, 'r') as f:
            result = yaml.load(f.read())
        if config['stage'] not in result['stages']:
            result['stages'].append(config['stage'])
        if config['job'] in result:
            print(f'Job {config["job"]} is already present in .gitlab-ci.yml. Overwriting!')
        result[config['job']] = self._gen_job(config)
        return result

    def _gen_notifier_config(self, config: dict):
        result = dict(projects=config.get('projects', {}))
        if 'mail_config' in config:
            result['mail_config'] = config['mail_config']
        return result

    def _setup_ci_config(self, config: dict, ci_config: PosixPath):
        conf = self._get_config(config)

        notifier_config = ci_config.parent / conf['config']
        with open(notifier_config, 'w') as f:
            print(f'Generating GitLab notifier conig into {notifier_config}...')
            f.write(yaml.dump(self._gen_notifier_config(conf),
                              default_flow_style=False))

        if ci_config.exists():
            print('Found existing .gitlab-ci.yml, updating...')
            new_ci_config = self._update_ci_config(ci_config, conf)
        else:
            print('Generating new .gitlab-ci.yml...')
            new_ci_config = self._gen_ci_config(conf)
        with open(ci_config, 'w') as f:
            f.write(yaml.dump(new_ci_config, default_flow_style=False))

    def _cleanup_gitlab_ci(self, config: dict, ci_config: PosixPath):
        RESERVED = ['image', 'services', 'stages', 'types', 'before_script',
                    'after_script', 'variables', 'cache']
        with open(ci_config, 'r') as f:
            result = yaml.load(f.read())
        if config['job'] in result:
            result.pop(config['job'])
        jobs_left = set(result.keys()).difference(RESERVED)
        if jobs_left:
            for job in jobs_left:
                if result[job].get('stage', 'test') == config['stage']:
                    break
            else:
                if config['stage'] in result['stages']:
                    i = result['stages'].index(config['stage'])
                    result['stages'].pop(i)
            print('Rewriting .gitlab-ci.yml')
            with open(ci_config, 'w') as f:
                f.write(yaml.dump(result, default_flow_style=False))
        else:  # no jobs left
            print('Notifier was the only job. Removing .gitlab-ci.yml')
            os.remove(ci_config)

    def _disable_notifications(self, config: dict, ci_config: PosixPath):
        conf = self._get_config(config)
        notifier_config = ci_config.parent / conf['config']
        if notifier_config.exists():
            print(f'Deleting {notifier_config}')
            os.remove(notifier_config)
        print('Cleaning up .gitlab-ci.yml')
        self._cleanup_gitlab_ci(conf, ci_config)

    @set_arg_map({'project_path': 'path',
                  'config_file_name': 'config',
                  'gitlab_ci_yaml_path': 'gitlabci'})
    @set_metavars({'mode': 'MODE', 'gitlab_ci_yaml_path': 'PATH', 'config_file_name': 'PATH'})
    @set_help(
        {
            'mode': 'command mode:\n"setup" — set up (update) notifications;\n"disable" — disable notifications.',
            'project_path': 'Path to the directory with the config file (default: ".").',
            'config_file_name': 'Name of the Foliant config file (default: "foliant.yml").',
            'gitlab_ci_yaml_path': 'Path to .gitlab-ci.yml file (default: ".gitlab-ci.yml").',
        }
    )
    def notifier(self,
                 mode: str,
                 project_path=Path('.'),
                 config_file_name='foliant.yml',
                 gitlab_ci_yaml_path='.gitlab-ci.yml'):
        '''notifier

        This command allows to set up GitLab notifier configuration
        (notifier setup) or disable notifications (notifier disable).
        '''
        config = project_path / config_file_name
        if not config.exists():
            quit(f'Foliant config doesn"t exist: {config}.')
        config = Parser(project_path, config_file_name, self.logger).parse()
        if self.config_section not in config:
            quit(f'Section {self.config_section} not found in foliant config')
        config = config[self.config_section]

        ci_config = Path(gitlab_ci_yaml_path)
        if not ci_config.exists():
            new_suffix = '.yaml' if ci_config.suffix == '.yml' else '.yml'
            if ci_config.with_suffix(new_suffix).exists():
                ci_config = ci_config.with_suffix(new_suffix)
        if mode.lower() == 'setup':
            print('Setting up notifications')
            self._setup_ci_config(config, ci_config)
            print(f'Notifications are set successfully.')
        elif mode.lower() == 'disable':
            print('Disabling notifications')
            self._disable_notifications(config, ci_config)
            print('Notifications are disabled')
