import os
from yaml import load, SafeLoader

with open(os.path.dirname(os.path.realpath(__file__)) + '/config.yml') as c:
    config = load(c, Loader=SafeLoader)
