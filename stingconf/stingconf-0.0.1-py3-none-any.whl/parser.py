import os
import sys
import argparse
import json
import yaml
from .utils import str_to_type, to_upper_snake
from .config import Config


class Parser():
    def __init__(self, description='', definitions=None):
        self._argparser = argparse.ArgumentParser(description=description)
        self._args = None
        self._conf_file = None
        self._env_prefix = None
        self._order = ['env', 'arg', 'file', 'default']
        self._items = []

        if definitions is not None:
            self.conf_file(definitions.get('conf_file', None))
            self.env_prefix(definitions.get('env_prefix', None))
            self.order(*definitions.get('order', ['env', 'arg', 'file', 'default']))
            self._items = []
            for name, value in definitions.get('items', {}).items():
                if 'type' in value:
                    value['type'] = str_to_type(value['type'])
                value.update(value.get('arg', {}))
                self.add(name, **value)

    def add(self, name, short=None, type=str, default=None,
            no_prefix=False, long_prefix='--', short_prefix='-', help=None, **kwargs):
        item = {
            'name': name,
            'short': short,
            'type': type,
            'default': default,
            'no_prefix': no_prefix,
        }
        item.update(kwargs)
        self._items.append(item)

        arg_names = []
        arg_names.append(long_prefix + name)
        if short is not None:
            arg_names.append(short_prefix + short)
        self._argparser.add_argument(*arg_names, dest=to_upper_snake(name), type=type, help=help)

    def env_prefix(self, prefix):
        self._env_prefix = prefix

    def conf_file(self, path, type='yaml'):
        if path is None:
            return

        with open(path) as f:
            if type == 'yaml':
                self._conf_file = yaml.safe_load(f)
            elif type == 'json':
                self._conf_file = json.load(f)

    def order(self, *orders):
        for o in reversed(orders):
            self._order.remove(o)
            self._order.insert(0, o)

    def parse(self):
        config = Config()

        self._args = self._argparser.parse_args(sys.argv[1:])
        for item in self._items:
            for o in self._order:
                f = getattr(self, '_get_from_' + o)
                value = f(item)
                if value is None:
                    continue
                try:
                    value = item['type'](value)
                except ValueError:
                    # TODO: Add warning log
                    continue
                config.add(to_upper_snake(item['name']), value, item)
                break

        return config

    def _get_from_env(self, item):
        env_name = to_upper_snake(item['name'])
        if self._env_prefix is not None and not item.get('env', {}).get('no_prefix'):
            env_name = '{0}_{1}'.format(self._env_prefix, env_name)
        if item.get('env', {}).get('ignorecase'):
            for n in (env_name.upper(), env_name.lower()):
                if n in os.environ:
                    return os.environ[n]
            return None
        else:
            return os.environ.get(env_name)

    def _get_from_arg(self, item):
        return getattr(self._args, to_upper_snake(item['name']))

    def _get_from_file(self, item):
        if self._conf_file is None:
            return None
        else:
            return self._conf_file.get(item['name'].replace('-', '_'))

    def _get_from_default(self, item):
        return item['default']
