import bisect
import json
import math
from pathlib import Path

import jsonschema
import torch.optim

from .configs import LrMode, LrSchedulerConfig, Scheduler


class LrScheduler:
    with open(str(Path(__file__).parent / 'schema' / 'lr_scheduler_config.json')) as f:
        schema = json.load(f)

    def __init__(self, config: LrSchedulerConfig):
        self.lr = config.initial_lr
        self.initial_lr = config.initial_lr
        self.total_steps = config.total_steps

        initial_scheduler = Scheduler({
            'lr_mode': 'fixed',
            'target_lr': config.initial_lr,
            'milestone': 0.0
        })
        self.scheduler_list = [initial_scheduler] + sorted(config.scheduler_list, key=lambda x: x.milestone)
        self.milestones = [scheduler.milestone for scheduler in self.scheduler_list]
        if self.milestones[-1] != 1.0:
            last_scheduler = Scheduler({
                'lr_mode': 'fixed',
                'target_lr': self.scheduler_list[-1].target_lr,
                'milestone': 1.0
            })
            self.scheduler_list.append(last_scheduler)
            self.milestones.append(1.0)

    def update(self, optimizer: torch.optim.Optimizer, step: int):
        assert 0 <= step <= self.total_steps
        overall_ratio = step / self.total_steps
        count = bisect.bisect_left(self.milestones, overall_ratio)

        current = self.scheduler_list[count]
        lr_mode = current.lr_mode
        milestone = current.milestone
        target_lr = current.target_lr

        if lr_mode == LrMode('fixed'):
            self.lr = current.target_lr
        else:
            previous = self.scheduler_list[count - 1]
            ratio = (overall_ratio - previous.milestone) / (milestone - previous.milestone)
            mapper = {
                'linear': lambda r: r,
                'cos': lambda r: (1 - math.cos(r * math.pi)) / 2
            }
            ratio = mapper[lr_mode.value](ratio)
            self.lr = previous.target_lr + (target_lr - previous.target_lr) * ratio

        for param_group in optimizer.param_groups:
            param_group['lr'] = self.lr

    def __repr__(self):
        return '\n'.join([
            f'{self.__class__.__name__} (',
            *[
                f' {item.milestone * 100: 6.1f}%, {item.lr_mode.value} to {item.target_lr},' for item in
                self.scheduler_list
            ],
            f')'
        ])

    @classmethod
    def factory(cls, config: dict, **kwargs):
        config.update(kwargs)
        jsonschema.validate(config, cls.schema)
        return cls(config=LrSchedulerConfig(config))
