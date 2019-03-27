# Copyright 2018, 2019 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os
from typing import Set
from . import DeployStep, DeployError
from ..config import Config
from ..run import run


class Deploy(DeployStep):
    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg

    @property
    def title(self) -> str:
        return 'Deploying %s:%s' % (self.cfg.remote, self.cfg.ref)

    @property
    def deployments_dir(self) -> str:
        return os.path.join(self.cfg.sysroot, 'ostree', 'deploy', self.cfg.stateroot, 'deploy')

    def run(self):
        items_diff = NewItemsHelper(self.deployments_dir)
        args = [
            'ostree', 'admin', 'deploy',
            '--sysroot=%s' % self.cfg.sysroot,
            '--os=%s' % self.cfg.stateroot,
            '%s:%s' % (self.cfg.remote, self.cfg.ref),
            '--karg=root=%s' % self.cfg.root_filesystem,
        ]
        for additional_argument in self.cfg.kernel_args:
            args.append('--karg-append=%s' % additional_argument)
        run(args, check=True)
        new_items = items_diff.get_new_items()

        if len(new_items) != 1:
            raise DeployError('could not determine new deployment directory')
        deployment_name = new_items.pop()

        self.cfg.set_deployment_name(deployment_name)
        print('==> New deployment:', deployment_name)


class NewItemsHelper:
    def __init__(self, path, exclude_suffix: str = '.origin') -> None:
        self.path = path
        self.exclude_suffix = exclude_suffix
        self.initial_items = self.get_current_items()

    def get_new_items(self) -> Set[str]:
        current_items = self.get_current_items()
        return current_items - self.initial_items

    def get_current_items(self) -> Set[str]:
        try:
            return set(filter(self.item_is_relevant, os.listdir(self.path)))
        except OSError:
            return set()

    def item_is_relevant(self, item: str) -> bool:
        return not item.endswith(self.exclude_suffix)
