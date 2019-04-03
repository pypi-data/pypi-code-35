import os
import shutil
import sys
import subprocess

from oly.utils import Utils, Clr


class Service:

    def __init__(self):
        pass

    def git_service_has_changes(self, service_dir='./'):
        if self.git_service_get_changes(service_dir):
            return True
        return False

    def git_service_get_changes(self, service_dir='./'):
        git_command = self._git_command(service_dir=service_dir, command='status -s')
        git_process = subprocess.check_output(git_command, shell=True, stderr=subprocess.STDOUT).decode(sys.stdout.encoding)
        if git_process:
            return str(git_process).strip().split('\n')

        return

    def git_service_update(self, service_dir='./'):
        branch = self.git_get_service_working_branch(service_dir)
        git_command = self._git_command(service_dir, 'pull origin ' + str(branch))
        try:
            process = subprocess.check_output(git_command, shell=True, stderr=subprocess.STDOUT).decode(sys.stdout.encoding)
            print(process)
            return True
        except subprocess.CalledProcessError as err:
            Clr(err.output).error_banner()
            return


    def git_get_service_working_branch(self, service_dir='./'):
        git_command = self._git_command(service_dir, command=' rev-parse --abbrev-ref HEAD')
        try:
            git_process = subprocess.check_output(git_command, shell=True, stderr=subprocess.STDOUT).decode(
                sys.stdout.encoding).strip()
            return git_process
        except subprocess.CalledProcessError as err:
            print(err.output)

    def git_get_service_last_tag(self, service_dir='./'):
        git_command = self._git_command(service_dir, command='describe --abbrev=0 --tags')
        git_process = subprocess.check_output(git_command, shell=True, stderr=subprocess.STDOUT).decode(sys.stdout.encoding).strip()
        return git_process

    @staticmethod
    def _git_command(service_dir='./', command=''):
        git_dir = os.path.join(service_dir, '.git')
        return 'git --git-dir=' + git_dir + ' --work-tree=' + service_dir + ' ' + command

    @staticmethod
    def remove_service_folder(service_dir='./'):
        shutil.rmtree(service_dir)
        return True

    @staticmethod
    def service_folder_exists(service):
        return os.path.isdir(os.path.join(Utils.PROJECTS_DIR, service))