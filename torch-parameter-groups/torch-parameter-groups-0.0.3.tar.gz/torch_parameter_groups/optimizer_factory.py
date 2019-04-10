import json
from pathlib import Path

import jsonschema
import torch.nn
import torch.optim

from .configs import OptimizerConfig
from .group_parameters import group_parameters
from .group_rule import GroupRule

with open(str(Path(__file__).parent / 'schema' / 'optimizer_config.json')) as f:
    schema = json.load(f)


def optimizer_factory(model: torch.nn.Module, config: dict = None) -> torch.optim.Optimizer:
    jsonschema.validate(config or {}, schema)
    config = OptimizerConfig(config)

    rules = list(map(GroupRule.factory, config.rules))
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
    return getattr(torch.optim, config.type)(params=params, lr=config.lr, **kwargs)
