import yaml
from logging.config import fileConfig

config = yaml.safe_load(open("local.yml"))

length = 10
if 'length' in config['vivo'] and config['vivo']['length']:
    length = int(config['vivo']['length'])
    print (length)



