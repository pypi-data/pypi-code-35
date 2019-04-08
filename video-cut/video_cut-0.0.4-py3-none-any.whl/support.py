import random
import subprocess
import os.path

def subprocess_call(cmd, verbose=True, errorprint=True):
    """ Executes the given subprocess command."""

    popen_params = {"stdout": subprocess.PIPE,
                    "stderr": subprocess.PIPE,
                    "stdin": subprocess.DEVNULL}
    pretty_cmd = ' '.join(cmd)
    # print(f'executing {pretty_cmd}')
    proc = subprocess.Popen(cmd, **popen_params)

    out, err = proc.communicate()
    # print(out)
    # proc.stderr.close()

    if proc.returncode:
        raise Exception(err.decode('utf8'))

    del proc
    return out.decode('utf8')


class temporary_write:
        def __init__(self,  data, path=str(random.random())[3:]):
                self.path = os.path.abspath(path)
                self.data = data
                f = open(self.path, 'w')
                f.write(self.data)
                f.close()

        __enter__ = lambda self: self.path
        __exit__ = lambda self, a, b, c: os.remove(self.path)

def name_and_ext(path):
    path, ext = os.path.splitext(path)
    name = os.path.basename(path)
    return name, ext
