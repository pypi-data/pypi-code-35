from typing import List

import torch.nn as nn

from .group_rule import GroupRule


def group_parameters(model: nn.Module, rules: List[GroupRule]) -> List[List[nn.Parameter]]:
    results: List[list] = [[] for _ in rules]

    def dfs(module: nn.Module, prefix: str = '', match_level: int = None):
        new_match_level = None
        for i, rule in enumerate(rules[:match_level]):
            if rule.match(module):
                new_match_level = i + 1
                break
        if new_match_level is None:
            new_match_level = match_level

        for name, child in module.named_children():
            dfs(child, prefix=f'{prefix}.{name}' if prefix else name, match_level=new_match_level)

        for name, param in module.named_parameters(recurse=False):
            new_prefix = f'{prefix}.{name}' if prefix else name
            for i, rule in enumerate(rules[:match_level]):
                if rule.match(module, param_name=name, prefix=new_prefix):
                    results[i].append(param)
                    break
            else:
                if new_match_level is not None:
                    results[new_match_level - 1].append(param)

    dfs(model)
    return results
