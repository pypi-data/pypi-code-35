import os
import yaml
from config_engine.settings import merge

BASE_DIR = os.path.dirname(__file__)

with open('{}/../../config_engine/default.yaml'.format(BASE_DIR)) as f:
    settings = yaml.load(f)

with open('{}/test_local.yaml'.format(BASE_DIR)) as f:
    merge(settings, yaml.load(f))

globals().update(settings)