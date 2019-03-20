# -*- coding: utf-8 -*-
import os
from collections import Mapping

import yaml

from soniclib import util, config

CONTEXT_FILE_NAME = "context.yml"

yaml.SafeLoader.add_multi_constructor('!', lambda loader, suffix, node: None)
yaml.SafeLoader.add_multi_constructor('tag:', lambda loader, suffix, node: None)
yaml.SafeLoader.add_constructor("tag:yaml.org,2002:python/unicode", lambda loader, node: node.value)

_mock_load_in_unittest = True


class Context(Mapping):
    __shared_state = {}
    __loaded = {
        'timestamp': 0.0
    }

    def __init__(self, force_load=False):
        self.refresh(force_load)
        self.__dict__ = self.__shared_state

    def load(self, force=False):
        if _mock_load_in_unittest and util.in_unittest():
            raise Exception("this method should be mocked in unit tests")
        data = None
        context_file_path = os.path.join(config.SONIC_PATH, CONTEXT_FILE_NAME)
        if os.path.isfile(context_file_path):
            timestamp = os.path.getmtime(context_file_path)
            if force or timestamp > self.__loaded["timestamp"]:
                if not util.in_unittest():
                    util.message("Loading context from %s" % context_file_path)
                with open(context_file_path, 'r') as f:
                    data = yaml.safe_load(f)
                    self.__loaded["timestamp"] = timestamp
        return data

    def refresh(self, force=False):
        data = self.load(force)
        if isinstance(data, dict):
            self.__shared_state.update(data)

    def save(self):
        util.ensure_path(config.SONIC_PATH)
        with open(config.SONIC_PATH + CONTEXT_FILE_NAME, 'w') as f:
            yaml.safe_dump(self.__dict__, f, default_flow_style=False, indent=4)
            self.__loaded["timestamp"] = os.path.getmtime(config.SONIC_PATH + CONTEXT_FILE_NAME)

    def clear(self):
        self.__dict__.clear()
        self.save()

    def __getitem__(self, key):
        return self.__dict__.__getitem__(key)

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        return iter(self.__dict__)

    def setdefault(self, key, default=None):
        self.__dict__.setdefault(key, default)

    def set(self, key, value):
        self.__dict__[key] = value

    def update(self, dict):
        self.__dict__.update(dict)
