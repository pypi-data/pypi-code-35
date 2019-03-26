import os
import yaml

BASE_DIR = os.path.dirname(__file__)


def merge(base, update):
    for k, v in update.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            merge(base[k], v)
        else:
            base[k] = v


settings = yaml.load(open('{}/default.yaml'.format(BASE_DIR)))
settings['APP_VERSION'] = open('{}/../version'.format(BASE_DIR)).read()

try:
    with open('{}/local.yaml'.format(BASE_DIR)) as f:
        merge(settings, yaml.load(f))
        if settings["STATICFILES_STORAGE"] == None:
            del settings["STATICFILES_STORAGE"]

except AttributeError:
    pass
except IOError:
    pass

globals().update(settings)
