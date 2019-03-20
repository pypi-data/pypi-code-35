import os
import re
from pathlib import Path

from ruamel.yaml import YAML

DEFAULT_CFG_PATH = Path('.') / Path('.cde.yml')
yaml = YAML(typ='safe')
yaml.allow_duplicate_keys = False
yaml.default_flow_style = False


def validate(cfg):
    ok = True
    repo_name_re = '^[a-z][a-z0-9-]*$'
    repo_name = re.compile(repo_name_re)
    for name, repo in cfg.get('repos', {}).items():
        if not repo_name.match(name):
            msg = 'repo-keys must be {} but {} not'
            print(msg.format(repo_name_re[1:-1], repr(name)))
            ok = False

    return ok


def load(path=None):
    if path is None:
        path = DEFAULT_CFG_PATH

    if not os.path.exists(path):
        return {}

    data = yaml.load(open(path))
    data.setdefault('repos', {})
    return data


def store(cfg, path=None):
    if path is None:
        path = DEFAULT_CFG_PATH

    yaml.dump(cfg, path)
