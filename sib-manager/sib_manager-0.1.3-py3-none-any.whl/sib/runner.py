import subprocess
from os import path, environ, getcwd


class Runner(object):

    """
    This class manage an existing SIB project
    """

    def __init__(self, project_folder=None):

        """Init"""

        if project_folder:
            self.project_folder = path.abspath(project_folder)
        else:
            self.project_folder = getcwd()

    def get_env(self):

        """Return environment"""

        env = environ.copy()

        # override path if venv is found in project folder
        venv_path = path.join(self.project_folder, 'env', 'bin')
        if path.isdir(venv_path):
            env['PATH'] = venv_path + ":" + env['PATH']

        return env


    def start_project(self):

        """Start the SIB project"""

        try:
            # wrap the django runverver command
            cmd = ['python', 'manage.py', 'runserver']
            subprocess.run(cmd, env=self.get_env(), cwd=self.project_folder)

        except subprocess.CalledProcessError as e:
            print('Start server failed: {}'.format(e))

