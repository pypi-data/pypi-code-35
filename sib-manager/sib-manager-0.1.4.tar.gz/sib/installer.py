import venv
import subprocess
from os import mkdir, path, environ
from pkg_resources import resource_filename


class Installer(object):

    """
    This class initialize a new SIB project by installing the required components and configuring the project
    """

    def __init__(self, project_name, project_folder=None, venv=False, modules=[]):

        """Init"""

        # set project name
        self.project_name = project_name

        # define project folder
        if project_folder:
            self.project_folder = path.abspath(project_folder)
        else:
            self.project_folder = path.abspath(self.project_name)

        # set venv if used
        if venv:
            self.venv_path = path.join(self.project_folder, 'env')
        else:
            self.venv_path = None

        # store packages (python module or packages)
        self.packages = [m[0] for m in modules]
        self.packages.append('djangoldp')  # add required packages

        # store distribution (pip distributions)
        self.dists = [m[1] for m in modules]
        self.dists.append('djangoldp')  # add required distribution
        self.dists.append('requests')  # fix lacking dependency in some ldp modules

    def get_env(self):

        """Return environment"""

        env = environ.copy()

        # override the PATH with virtualenv property if any
        if self.venv_path:
            env['PATH'] = path.join(self.venv_path, 'bin') + ":" + env['PATH']

        return env

    def get_template(self):

        """Return the path of django project template from package resouces"""

        return resource_filename(__name__, 'template')

    def create_project(self):

        """Create the SIB project"""

        try:
            # create project folder
            mkdir(self.project_folder)

            # create virtualenv
            if self.venv_path:
                venv.EnvBuilder(with_pip=True).create(self.venv_path)
                # upgrade pip
                cmd = ['pip', 'install', '-U', 'pip']
                subprocess.run(cmd, env=self.get_env())

            # install modules including required ones
            cmd = ['pip', 'install', '-U']
            cmd.extend(self.dists)
            subprocess.run(cmd, env=self.get_env()).check_returncode()

            # init django
            cmd = [
                'django-admin',
                'startproject',
                '--template=' + self.get_template(),
                self.project_name,
                self.project_folder
            ]
            subprocess.run(cmd, env=self.get_env()).check_returncode()

            # configure LDP modules overring package.py file
            try:
                with open(path.join(self.project_folder, self.project_name, 'packages.py'), 'w') as f:
                    f.write("DJANGOLDP_PACKAGES=[\n'")
                    f.write("',\n'".join(self.packages))
                    f.write("'\n]")
            except IOError:
                print('Error locating packages.py')
                pass

            # migrate
            cmd = ['python', 'manage.py', 'migrate']
            subprocess.run(cmd, env=self.get_env(), cwd=self.project_folder).check_returncode()

            # create admin
            cmd = ['python', 'manage.py', 'createsuperuser']
            subprocess.run(cmd, env=self.get_env(), cwd=self.project_folder).check_returncode()

        except FileExistsError:
            print('Folder already exists')
            return False

        except subprocess.CalledProcessError as e:
            print('Installation failed: {}'.format(e))
            return False

        return True
