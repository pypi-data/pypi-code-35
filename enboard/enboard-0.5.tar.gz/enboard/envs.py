import os
import subprocess
from pathlib import Path
import shutil

_PKGDIR = Path(__file__).parent.resolve()

CONDA_ROOT = os.environ.get('CONDA_ROOT_DIR', '~/miniconda3')
DEFAULT_SHELL = 'sh'

class MenuItem:
    def __init__(self, display, *, data=None):
        self.display = display
        self.data = data

    def __repr__(self):
        p = [type(self).__name__, '(', repr(self.display)]
        if self.data is not None:
            p += [', data=', repr(self.data)]
        p += [')']
        return ''.join(p)

class CondaEnv:
    def __init__(self, path):
        self.path = path
        self.display = path.name
        self.shell = os.environ.get('SHELL', DEFAULT_SHELL)

    def __repr__(self):
        return 'CondaEnv(%r)' % self.path

    def delete(self):
        # MinGW (like gitbash on windows)
        # this is needed since windows tends to deny access
        # when deleting the folder with rmtree
        if os.path.basename(self.shell) == 'bash.exe':
            subprocess.call(['rm', "-rf", str(self.path)], shell=True)
        else:
            shutil.rmtree(str(self.path))

    def activate(self):
        e = os.environ
        e['PATH'] = str(self.path / 'bin') + ':' + e['PATH']
        e['CONDA_DEFAULT_ENV'] = self.path.name
        e['CONDA_PREFIX'] = str(self.path)

        print("\nLaunching {} with conda environment: {}".format(
              self.shell, self.path.name))
        print("Exit the shell to leave the environment.", flush=True)

        # MinGW (like gitbash on windows)
        if os.path.basename(self.shell) == 'bash.exe':
            rcfile_path = os.path.abspath(os.path.join(_PKGDIR, 'conda-bashrc-mingw.sh'))
            subprocess.call([self.shell, '--rcfile', rcfile_path])
            return 0

        if os.path.basename(self.shell) == 'bash':
            os.execvp(self.shell,
                      [self.shell, '--rcfile', str(_PKGDIR / 'conda-bashrc.sh')])

        # Generic shell
        activate_d = os.path.join(os.environ['CONDA_PREFIX'],
                                  'etc', 'conda', 'activate.d')
        if os.path.isdir(activate_d):
            print('Files in activate.d will not be run (unknown shell):')
            print(os.listdir(activate_d), flush=True)
        os.execvp(self.shell, [self.shell])

def find_conda_envs():
    conda_dir = Path(CONDA_ROOT).expanduser()
    if not conda_dir.is_dir():
        raise Exception(("No directory at {}. "
                         "Set $CONDA_ROOT_DIR to point to your conda install.")
                        .format(conda_dir))
    env_dir =  conda_dir / 'envs'
    env_dir.mkdir(exist_ok=True)
    for f in env_dir.iterdir():
        if f.is_dir():
            yield CondaEnv(f)


def find_envs():
    envs = list(find_conda_envs())
    return sorted(envs, key=lambda x: x.display.lower())
