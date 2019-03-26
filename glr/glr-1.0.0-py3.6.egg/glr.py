#!/usr/bin/env python
"""Run Scripts from .gitlab-ci.yml file locally"""

import os
import subprocess
import sys

import yaml

DEFAULT_FILE = ".gitlab-ci.yml"

T_GREEN = '\033[32m'
T_RED = '\033[91m'
T_DIM = '\033[37m'
T_RESET = '\033[m'

def log(color, level, text):
    """Print text with pretty colors and indented to level"""
    prefix = ' '.ljust(level)
    return print("%s ↳ %s%s%s" % (prefix, color, text, T_RESET))

class GitLabCIFile:
    """Operations around reading and parsing the .gitlab-ci.yml file"""

    _obj = None
    targets = []

    def __init__(self, full_path):
        with open(full_path, 'r') as _yaml_file:
            self._obj = yaml.safe_load(_yaml_file.read())

    def _extract_targets(self):
        """Extract list of targets"""
        targets = self._obj.get('stages', [])
        for key, value in self._obj.items():
            if 'script' in value:
                full_key = key
                if 'stage' in value:
                    full_key = "%s:%s" % (value.get('stage'), key)
                targets.append(full_key)
        return targets

    # pylint: disable=no-self-use
    def _run_command(self, cmd):
        """Wrapper to run command and redirect output"""
        log(T_DIM, 12, "Running %s" % cmd)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output, _error = process.communicate()
        color = T_GREEN
        if process.returncode > 0:
            color = T_RED
        log(color, 12, "Output: '%s'" % output.decode('utf-8').rstrip("\n\r"))
        log(color, 12, "Exit code: %d" % process.returncode)
        return process.returncode

    # pylint: disable=no-self-use
    def _to_array(self, value):
        """Take value and make sure it's an array"""
        if not isinstance(value, list):
            return [value]
        return value

    def resolve_target_names(self, target):
        """Resolve stage and stage:target names into list of targets"""
        targets = []
        if ':' in target:
            _, target = target
        if target in self._obj['stages']:
            sub_targets = []
            for _target in self.targets:
                if _target.startswith('%s:' % target):
                    sub_targets.append(_target.split(':')[1])
            log(T_DIM, 4, 'Stage %s implicitly triggers %r' % (target, sub_targets))
            targets += sub_targets
        else:
            targets.append(target)
        return targets

    def run(self, target_name):
        """Run target command"""
        sub_stages = ['before_script', 'script', 'after_script']
        return_code = 0
        for sub_stage in sub_stages:
            if sub_stage in self._obj[target_name]:
                log(T_DIM, 8, "Sub-stage '%s'" % sub_stage)
                for command in self._to_array(self._obj[target_name][sub_stage]):
                    return_code += self._run_command(command)
        return return_code

    def parse(self):
        """Run all parsing logic"""
        self.targets = self._extract_targets()

def main():
    """Main Logic"""
    GITLAB_CI = GitLabCIFile(os.path.join(os.getcwd(), DEFAULT_FILE))
    GITLAB_CI.parse()
    if len(sys.argv) > 1:
        TARGETS_TO_RUN = [sys.argv[1]]
    else:
        if 'test' in GITLAB_CI.targets:
            TARGETS_TO_RUN = ['test']
            log(T_DIM, 0, 'Defaulted to %s' % TARGETS_TO_RUN)
        else:
            TARGETS_TO_RUN = GITLAB_CI.targets
    log(T_GREEN, 0, "Running %d target(s)" % len(TARGETS_TO_RUN))

    for target_to_run in TARGETS_TO_RUN:
        for target in GITLAB_CI.resolve_target_names(target_to_run):
            log(T_GREEN, 4, "Target '%s'" % target)
            GITLAB_CI.run(target)

if __name__ == '__main__':
    main()
