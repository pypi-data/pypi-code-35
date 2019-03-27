# Copyright 2018, 2019 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from . import DeployStep
from ..run import run


class CreateStateroot(DeployStep):
    @property
    def title(self) -> str:
        return 'Creating stateroot: %s' % self.config.stateroot

    def run(self):
        if os.path.exists(self._stateroot_dir):
            print("already exists, skipping")
            return
        run([
            'ostree', 'admin', 'os-init',
            '--sysroot=%s' % self.config.sysroot,
            self.config.stateroot
        ], check=True)

    @property
    def _stateroot_dir(self):
        return os.path.join(self.config.sysroot, 'ostree', 'deploy', self.config.stateroot)
