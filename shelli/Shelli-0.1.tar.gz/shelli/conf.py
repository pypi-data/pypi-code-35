"""
Defines helper methods for loading YAML files
to configure other classes and whatnot
"""

import os
import yaml

def _default_path():
    home = os.environ['HOME']
    return os.path.join(home, '.shelli.yml')

class YAMLoader:
    """Loads yaml from file, and acts as the YAML object itself"""

    _yaml = {}
    _path = ''

    def __init__(self, path=_default_path()):
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            print('Error: File not found', path)
            exit(1)
        self._path = path
        with open(self._path) as yamlfile:
            # Could use yaml.SafeLoader to load yaml safely
            self._yaml = yaml.load(yamlfile, Loader=yaml.FullLoader)

    def __str__(self):
        return yaml.dump(self._yaml)

    def __getitem__(self, index):
        return self._yaml[index]

    def __setitem__(self, index, val):
        self._yaml[index] = val
