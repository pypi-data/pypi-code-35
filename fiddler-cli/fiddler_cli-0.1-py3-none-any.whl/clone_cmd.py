import logging
import os
import subprocess


class CloneCmd:

    def __init__(self, org, auth):
        self.org = org
        self.auth = auth

    def run(self):
        logging.info('Cloning into repo: {}'.format(self.org))
        if not self.which('git'):
            logging.info('git not found. Please install git')
            return 'git-not-found'
        if os.path.exists(self.org):
            logging.info('org exists locally, cannot clone')
            return 'org-exists'
        subprocess.call(['git', 'config', '--global', '--unset-all',
                         'http.http://repo.fiddler.ai.extraheader'])
        subprocess.call(['git', 'config', '--global', '--add',
                         'http.http://repo.fiddler.ai.extraheader',
                         'Authorization: Bearer {}'.format(self.auth)])
        logging.info('Done configuring git')
        subprocess.call(['git', 'clone',
                         'http://repo.fiddler.ai/{}.git'.format(self.org)])
        logging.info('Done cloning git repo')


    @staticmethod
    def which(program):

        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ['PATH'].split(os.pathsep):
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file

        return None
