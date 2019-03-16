import logging
import typing
from copy import deepcopy
from pathlib import Path
from typing import Iterator

from ktdk.config import ConfigPaths, ConfigPropMixin
from ktdk.runtime.tags import TagsEvaluator
from ktdk.utils.basic import BasicObject

log = logging.getLogger(__name__)


def deep_merge(source, destination):
    """Deep merge
    Examples:
    >>> a = { 'first' : { 'all_rows': { 'pass': 'dog', 'number': '1' } } }
    >>> b = { 'first' : { 'all_rows': { 'fail': 'cat', 'number': '5' } } }
    >>> deep_merge(b, a) == {'first':{'all_rows':{'pass': 'dog', 'fail': 'cat', 'number': '5'}}}
    True
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            deep_merge(value, node)
        else:
            destination[key] = value

    return destination


def _get_subdir(where: Path, sub_path, create=False):
    full_path = where / Path(sub_path)
    if create and not full_path.exists():
        full_path.mkdir(parents=True)
    return full_path


class ContextConfig(ConfigPropMixin, typing.MutableMapping):
    @property
    def __props__(self) -> dict:
        return self.all

    def __init__(self, suite_config=None, test_config=None, task_config=None):
        self._suite = suite_config if suite_config is not None else {}
        self._test = test_config if test_config is not None else {}
        self._task = task_config if task_config is not None else {}

    @property
    def suite(self):
        return self._suite

    @property
    def test(self):
        return self._test

    @property
    def task(self):
        return self._task

    @property
    def submission(self) -> dict:
        return self.get('submission_config')

    @property
    def all(self):
        cfg = {}
        cfg = deep_merge(self.suite, cfg)
        cfg = deep_merge(self.test, cfg)
        cfg = deep_merge(self.task, cfg)
        return cfg

    def __set_any(self, which, name, value):
        collection = getattr(self, which)
        if name in collection:
            log.debug(f"[CTX] Overriding {which}['{name}']: ({collection[name]}) by ({value})!")
        else:
            log.trace(f"[CTX] SET: {which}['{name}'] = {value}")
        collection[name] = value

    def __add_any(self, which, name, value):
        collection = getattr(self, which)
        old_value = collection.get(name, None)
        new_value = deepcopy(value)

        if isinstance(value, list):
            new_value = old_value + value if old_value else deepcopy(value)

        if isinstance(value, dict):
            new_value = deep_merge(old_value or {}, new_value)

        log.trace(f"[CTX] Adding ({which}['{name}']): {old_value} + {value} -> {new_value}")
        collection[name] = new_value

    def add_suite(self, name, value):
        self.__add_any('suite', name, value)

    def add_test(self, name, value):
        self.__add_any('test', name, value)

    def add_task(self, name, value):
        self.__add_any('task', name, value)

    def set_suite(self, name, value):
        self.__set_any('suite', name, value)

    def set_test(self, name, value):
        self.__set_any('test', name, value)

    def set_task(self, name, value):
        self.__set_any('task', name, value)

    def clone(self, clone_test=False):
        test_config = deepcopy(self.test) if clone_test else self.test
        task_config = deepcopy(self.task)
        config = ContextConfig(suite_config=self.suite,
                               test_config=test_config,
                               task_config=task_config)
        return config

    def __getitem__(self, item):
        return self.all.get(item)

    def get(self, name):
        return self.all.get(name)

    def __str__(self):
        return str(self.all)

    def __repr__(self):
        return str(self.all)

    def __delitem__(self, v) -> None:
        # Todo implement for any collection
        del self.all[v]

    def __len__(self) -> int:
        return len(self.all)

    def __iter__(self) -> Iterator:
        return self.all.__iter__()

    def __setitem__(self, k, v) -> None:
        self.all[k] = v


class Context(BasicObject, typing.MutableMapping):
    def __init__(self, suite_config=None, test_config=None, task_config=None, config=None):
        super().__init__()
        self._config = config or ContextConfig(suite_config=suite_config,
                                               test_config=test_config,
                                               task_config=task_config)
        self._tags_evaluator = TagsEvaluator(self.config['tags'], self.config['registered_tags'])
        self._paths = ConfigPaths(self.config)

    @property
    def tags(self):
        return self._tags_evaluator

    @property
    def devel(self):
        return self.config.all.get('devel', False)

    @property
    def paths(self) -> ConfigPaths:
        return self._paths

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    def clone(self, clone_test=False):
        return Context(config=self.config.clone(clone_test=clone_test))

    def to_dict(self):
        return self.config

    def __getitem__(self, item):
        """Gets an item form the context
        """
        return self.config[item]

    def __setitem__(self, k, v) -> None:
        self.config[k] = v

    def __delitem__(self, v) -> None:
        del self.config[v]

    def __len__(self) -> int:
        return len(self.config)

    def __iter__(self) -> Iterator:
        return self.config.__iter__()
