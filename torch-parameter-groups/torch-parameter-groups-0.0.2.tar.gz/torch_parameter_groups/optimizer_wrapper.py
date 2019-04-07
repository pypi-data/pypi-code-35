import json
from pathlib import Path

import jsonschema
import torch.nn
import torch.optim

from .configs import OptimizerWrapperConfig
from .group_parameters import group_parameters
from .group_rule import GroupRule


class OptimizerWrapper:
    with open(str(Path(__file__).parent / 'schema' / 'optimizer_wrapper_config.json')) as f:
        schema = json.load(f)

    def __init__(self, model: torch.nn.Module, config: OptimizerWrapperConfig):
        rules = list(map(GroupRule, config.rules))
        param_groups = group_parameters(model=model, rules=rules)

        params = []
        for param_group, rule in zip(param_groups, rules):
            if rule.refuse_if_match is False:
                kwargs = {'weight_decay': rule.weight_decay} if rule.weight_decay is not None else {}
                params.append({
                    'params': param_group,
                    **kwargs
                })

        kwargs = {
            'weight_decay': config.weight_decay
        }
        if config.momentum is not None:
            kwargs['momentum'] = config.momentum
        if config.nesterov is not None:
            kwargs['nesterov'] = config.nesterov
        self.core: torch.optim.Optimizer = getattr(torch.optim, config.type)(
            params=params,
            lr=config.lr,
            **kwargs
        )

    def step(self, closure: callable = None):
        self.core.step(closure=closure)

    @property
    def param_groups(self):
        return self.core.param_groups

    def __repr__(self):
        return repr(self.core)

    @classmethod
    def factory(cls, model: torch.nn.Module, config: dict = None):
        jsonschema.validate(config or {}, cls.schema)
        return cls(model=model, config=OptimizerWrapperConfig(config))
