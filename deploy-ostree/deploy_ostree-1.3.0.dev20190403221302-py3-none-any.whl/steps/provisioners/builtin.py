# Copyright 2018, 2019 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from pathlib import Path
import deploy_ostree
from . import DeployStep
from ...config import Config, BuiltinProvisionerConfig
from ...run import run


PROVISIONER_DIR = Path(deploy_ostree.__file__).parent / 'builtin-provisioners'


def shell_provisioner(name):
    exe = PROVISIONER_DIR / name

    def provision(deployment_dir: Path, args):
        env = {'DEPLOY_OSTREE_%s' % key: value for key, value in args.items()}
        run([str(exe), str(deployment_dir)], check=True, env=env)

    return provision


class BuiltinProvisioner(DeployStep):
    PROVISIONERS = {
        'authorized-keys': shell_provisioner('authorized-keys'),
        'create-user': shell_provisioner('create-user'),
        'etc-fstab': shell_provisioner('etc-fstab'),
        'etc-network-interfaces': shell_provisioner('etc-network-interfaces'),
        'passwordless-sudo': shell_provisioner('passwordless-sudo'),
        'root-password': shell_provisioner('root-password'),
    }

    def __init__(self, config: Config, provisioner: BuiltinProvisionerConfig) -> None:
        self.config = config
        self.provisioner = provisioner

    @property
    def title(self) -> str:
        return 'Provisioning: %s' % self.provisioner.name

    def run(self):
        self.PROVISIONERS[self.provisioner.name](self.config.deployment_dir, self.provisioner.args)
