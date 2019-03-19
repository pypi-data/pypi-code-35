from yaml import load, SafeLoader

with open('config.yml') as c:
    config = load(c, Loader=SafeLoader)
