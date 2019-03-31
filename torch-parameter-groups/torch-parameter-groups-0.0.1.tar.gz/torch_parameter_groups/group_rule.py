import json
from pathlib import Path

import jsonschema
import torch.nn as nn

from .configs import GroupRuleConfig


class GroupRule:
    with open(str(Path(__file__).parent / 'schema' / 'optimizer_wrapper_config.json')) as f:
        schema = json.load(f)['definitions']['group_rule_config']

    def __init__(self, config: GroupRuleConfig):
        self.module_type_set = set(config.module_type_list)
        self.param_name_set = set(config.param_name_list)
        self.prefix_list = config.prefix_list
        self.weight_decay = config.weight_decay
        self.refuse_if_match = config.refuse_if_match

    def match(self, module: nn.Module, param_name: str = None, prefix: str = None):
        module_type = module.__class__.__name__
        module_match = (not self.module_type_set or module_type in self.module_type_set)
        param_match = (not self.param_name_set or param_name in self.param_name_set)
        prefix_match = (not self.prefix_list or any(prefix.startswith(p) for p in self.prefix_list))
        return module_match and param_match and prefix_match

    @classmethod
    def factory(cls, config: dict = None):
        jsonschema.validate(config or {}, cls.schema)
        return cls(config=GroupRuleConfig(values=config))
