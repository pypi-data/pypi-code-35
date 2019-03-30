import yaml
import os

def _default_path():
    home = os.environ['HOME']
    return os.path.join(home, '.shelli.yml')

class YAMLoader:
    _yaml = {}
    _path = ''

    def __init__(self, path=_default_path()):
        if not os.path.exists(path):
            print('Error: File not found', path)
            exit(1)
        self._path = path
        self._yaml = yaml.load(open(self._path))
        
    def __str__(self):
        return yaml.dump(self._yaml)

    def __getitem__(self, index):
        return self._yaml[index]

    def __setitem__(self, index, val):
        self._yaml[index] = val
